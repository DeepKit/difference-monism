import os
import sqlite3
import hashlib
import logging
from datetime import datetime
from typing import List, Optional, Tuple
from pathlib import Path


class DBMigrationError(Exception):
    """数据库迁移异常"""
    pass


class DBMigration:
    """数据库迁移管理类"""
    
    def __init__(self, db_path: str, migrations_dir: str = "migrations"):
        """
        初始化数据库迁移管理器
        
        Args:
            db_path: 数据库文件路径
            migrations_dir: 迁移文件目录
        """
        self.db_path = db_path
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
        
        self._init_migrations_table()
    
    def _get_connection(self) -> sqlite3.Connection:
        """获取数据库连接"""
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            return conn
        except sqlite3.Error as e:
            raise DBMigrationError(f"数据库连接失败: {e}")
    
    def _init_migrations_table(self):
        """初始化迁移记录表"""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS schema_migrations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        version TEXT NOT NULL UNIQUE,
                        name TEXT NOT NULL,
                        checksum TEXT NOT NULL,
                        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        execution_time_ms INTEGER
                    )
                """)
                conn.commit()
                self.logger.info("迁移表初始化成功")
        except sqlite3.Error as e:
            raise DBMigrationError(f"初始化迁移表失败: {e}")
    
    def create_migration(self, name: str) -> str:
        """
        创建新的迁移文件
        
        Args:
            name: 迁移名称
            
        Returns:
            创建的迁移文件路径
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        version = f"{timestamp}_{name}"
        
        up_file = self.migrations_dir / f"{version}.up.sql"
        down_file = self.migrations_dir / f"{version}.down.sql"
        
        try:
            up_file.write_text(f"-- Migration: {name}\n-- Created: {datetime.now()}\n\n")
            down_file.write_text(f"-- Rollback: {name}\n-- Created: {datetime.now()}\n\n")
            
            self.logger.info(f"创建迁移文件: {version}")
            return version
        except IOError as e:
            raise DBMigrationError(f"创建迁移文件失败: {e}")
    
    def _calculate_checksum(self, content: str) -> str:
        """计算文件内容的校验和"""
        return hashlib.sha256(content.encode()).hexdigest()
    
    def _get_migration_files(self) -> List[Tuple[str, Path, Path]]:
        """
        获取所有迁移文件
        
        Returns:
            [(version, up_file, down_file), ...]
        """
        migrations = {}
        
        for file in sorted(self.migrations_dir.glob("*.up.sql")):
            version = file.stem.replace(".up", "")
            down_file = self.migrations_dir / f"{version}.down.sql"
            
            if down_file.exists():
                migrations[version] = (version, file, down_file)
        
        return sorted(migrations.values(), key=lambda x: x[0])
    
    def _is_migration_applied(self, version: str) -> bool:
        """检查迁移是否已应用"""
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT 1 FROM schema_migrations WHERE version = ?",
                    (version,)
                )
                return cursor.fetchone() is not None
        except sqlite3.Error as e:
            raise DBMigrationError(f"检查迁移状态失败: {e}")
    
    def _record_migration(self, version: str, name: str, checksum: str, 
                         execution_time_ms: int):
        """记录已应用的迁移"""
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT INTO schema_migrations 
                    (version, name, checksum, execution_time_ms)
                    VALUES (?, ?, ?, ?)
                """, (version, name, checksum, execution_time_ms))
                conn.commit()
        except sqlite3.Error as e:
            raise DBMigrationError(f"记录迁移失败: {e}")
    
    def _remove_migration_record(self, version: str):
        """删除迁移记录"""
        try:
            with self._get_connection() as conn:
                conn.execute(
                    "DELETE FROM schema_migrations WHERE version = ?",
                    (version,)
                )
                conn.commit()
        except sqlite3.Error as e:
            raise DBMigrationError(f"删除迁移记录失败: {e}")
    
    def migrate(self, target_version: Optional[str] = None) -> int:
        """
        执行数据库迁移
        
        Args:
            target_version: 目标版本，None表示迁移到最新版本
            
        Returns:
            应用的迁移数量
        """
        migrations = self._get_migration_files()
        applied_count = 0
        
        for version, up_file, _ in migrations:
            if target_version and version > target_version:
                break
            
            if self._is_migration_applied(version):
                continue
            
            try:
                sql_content = up_file.read_text()
                checksum = self._calculate_checksum(sql_content)
                
                self.logger.info(f"应用迁移: {version}")
                start_time = datetime.now()
                
                with self._get_connection() as conn:
                    conn.executescript(sql_content)
                    conn.commit()
                
                execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
                self._record_migration(version, up_file.stem, checksum, execution_time)
                
                applied_count += 1
                self.logger.info(f"迁移成功: {version} ({execution_time}ms)")
                
            except Exception as e:
                self.logger.error(f"迁移失败: {version} - {e}")
                raise DBMigrationError(f"应用迁移 {version} 失败: {e}")
        
        self.logger.info(f"迁移完成，共应用 {applied_count} 个迁移")
        return applied_count
    
    def rollback(self, steps: int = 1) -> int:
        """
        回滚数据库迁移
        
        Args:
            steps: 回滚步数
            
        Returns:
            回滚的迁移数量
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute("""
                    SELECT version, name FROM schema_migrations
                    ORDER BY applied_at DESC
                    LIMIT ?
                """, (steps,))
                migrations_to_rollback = cursor.fetchall()
        except sqlite3.Error as e:
            raise DBMigrationError(f"获取回滚列表失败: {e}")
        
        rollback_count = 0
        
        for row in migrations_to_rollback:
            version = row['version']
            down_file = self.migrations_dir / f"{version}.down.sql"
            
            if not down_file.exists():
                raise DBMigrationError(f"回滚文件不存在: {down_file}")
            
            try:
                sql_content = down_file.read_text()
                
                self.logger.info(f"回滚迁移: {version}")
                
                with self._get_connection() as conn:
                    conn.executescript(sql_content)
                    conn.commit()
                
                self._remove_migration_record(version)
                rollback_count += 1
                self.logger.info(f"回滚成功: {version}")
                
            except Exception as e:
                self.logger.error(f"回滚失败: {version} - {e}")
                raise DBMigrationError(f"回滚迁移 {version} 失败: {e}")
        
        self.logger.info(f"回滚完成，共回滚 {rollback_count} 个迁移")
        return rollback_count
    
    def status(self) -> List[dict]:
        """
        获取迁移状态
        
        Returns:
            迁移状态列表
        """
        migrations = self._get_migration_files()
        status_list = []
        
        for version, up_file, _ in migrations:
            is_applied = self._is_migration_applied(version)
            
            applied_info = None
            if is_applied:
                try:
                    with self._get_connection() as conn:
                        cursor = conn.execute("""
                            SELECT applied_at, execution_time_ms 
                            FROM schema_migrations 
                            WHERE version = ?
                        """, (version,))
                        row = cursor.fetchone()
                        if row:
                            applied_info = {
                                'applied_at': row['applied_at'],
                                'execution_time_ms': row['execution_time_ms']
                            }
                except sqlite3.Error:
                    pass
            
            status_list.append({
                'version': version,
                'name': up_file.stem.replace('.up', ''),
                'applied': is_applied,
                'applied_info': applied_info
            })
        
        return status_list
    
    def validate(self) -> bool:
        """
        验证已应用迁移的完整性
        
        Returns:
            验证是否通过
        """
        try:
            with self._get_connection() as conn:
                cursor = conn.execute(
                    "SELECT version, checksum FROM schema_migrations ORDER BY version"
                )
                applied_migrations = cursor.fetchall()
        except sqlite3.Error as e:
            raise DBMigrationError(f"获取迁移记录失败: {e}")
        
        all_valid = True
        
        for row in applied_migrations:
            version = row['version']
            stored_checksum = row['checksum']
            
            up_file = self.migrations_dir / f"{version}.up.sql"
            
            if not up_file.exists():
                self.logger.error(f"迁移文件缺失: {version}")
                all_valid = False
                continue
            
            current_checksum = self._calculate_checksum(up_file.read_text())
            
            if current_checksum != stored_checksum:
                self.logger.error(f"迁移文件已被修改: {version}")
                all_valid = False
        
        if all_valid:
            self.logger.info("所有迁移验证通过")
        else:
            self.logger.warning("部分迁移验证失败")
        
        return all_valid


# 使用示例
if __name__ == "__main__":
    # 初始化迁移管理器
    migration = DBMigration("database.db", "migrations")
    
    # 创建新迁移
    version = migration.create_migration("create_users_table")
    
    # 编辑迁移文件后执行迁移
    # migration.migrate()
    
    # 查看状态
    # status = migration.status()
    # for s in status:
    #     print(f"{s['version']}: {'已应用' if s['applied'] else '未应用'}")
    
    # 回滚
    # migration.rollback(steps=1)
    
    # 验证完整性
    # migration.validate()
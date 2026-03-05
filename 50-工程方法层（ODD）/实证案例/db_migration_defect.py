import sqlite3
from pathlib import Path
from datetime import datetime
from typing import List, Callable


class DBMigration:
    def __init__(self, db_path: str, migrations_dir: str = "migrations"):
        self.db_path = db_path
        self.migrations_dir = Path(migrations_dir)
        self.migrations_dir.mkdir(exist_ok=True)
        self._init_migration_table()
    
    def _init_migration_table(self):
        """初始化迁移历史表"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version TEXT PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
    
    def _get_applied_versions(self) -> List[str]:
        """获取已应用的迁移版本"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT version FROM schema_migrations ORDER BY version")
            return [row[0] for row in cursor.fetchall()]
    
    def create_migration(self, name: str) -> str:
        """创建新的迁移文件"""
        version = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{version}_{name}.py"
        filepath = self.migrations_dir / filename
        
        template = f'''"""Migration: {name}"""

def up(conn):
    """应用迁移"""
    # 在这里编写迁移SQL
    conn.execute("""
        -- 你的SQL语句
    """)

def down(conn):
    """回滚迁移"""
    # 在这里编写回滚SQL
    conn.execute("""
        -- 你的回滚SQL语句
    """)
'''
        filepath.write_text(template, encoding='utf-8')
        return str(filepath)
    
    def _load_migration(self, filepath: Path):
        """加载迁移文件"""
        import importlib.util
        spec = importlib.util.spec_from_file_location("migration", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.up, module.down
    
    def migrate(self):
        """执行所有待应用的迁移"""
        applied = set(self._get_applied_versions())
        migration_files = sorted(self.migrations_dir.glob("*.py"))
        
        with sqlite3.connect(self.db_path) as conn:
            for filepath in migration_files:
                version = filepath.stem.split('_')[0]
                
                if version in applied:
                    continue
                
                print(f"应用迁移: {filepath.name}")
                up, _ = self._load_migration(filepath)
                up(conn)
                
                conn.execute(
                    "INSERT INTO schema_migrations (version) VALUES (?)",
                    (version,)
                )
                conn.commit()
                print(f"✓ 完成: {filepath.name}")
    
    def rollback(self, steps: int = 1):
        """回滚指定数量的迁移"""
        applied = self._get_applied_versions()
        
        if not applied:
            print("没有可回滚的迁移")
            return
        
        to_rollback = applied[-steps:]
        
        with sqlite3.connect(self.db_path) as conn:
            for version in reversed(to_rollback):
                migration_file = next(self.migrations_dir.glob(f"{version}_*.py"))
                print(f"回滚迁移: {migration_file.name}")
                
                _, down = self._load_migration(migration_file)
                down(conn)
                
                conn.execute("DELETE FROM schema_migrations WHERE version = ?", (version,))
                conn.commit()
                print(f"✓ 回滚完成: {migration_file.name}")
    
    def status(self):
        """显示迁移状态"""
        applied = set(self._get_applied_versions())
        all_migrations = sorted(self.migrations_dir.glob("*.py"))
        
        print("\n迁移状态:")
        print("-" * 60)
        for filepath in all_migrations:
            version = filepath.stem.split('_')[0]
            status = "✓ 已应用" if version in applied else "✗ 待应用"
            print(f"{status} | {filepath.name}")
        print("-" * 60)


# 使用示例
if __name__ == "__main__":
    migrator = DBMigration("app.db")
    
    # 创建迁移
    # migrator.create_migration("create_users_table")
    
    # 执行迁移
    migrator.migrate()
    
    # 查看状态
    migrator.status()
    
    # 回滚
    # migrator.rollback(steps=1)
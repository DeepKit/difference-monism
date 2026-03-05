import os
import re

base_dir = r"D:\_Progs\01Center\ASTO\小说故事\《未尽之算》\卷01_代价的计算"

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    new_lines = []
    
    # 状态标记
    in_header = False
    
    for line in lines:
        # 1. 统一日志格式
        if "*系统日志：" in line or "*[SYSTEM_LOG]:" in line:
            # 提取原始内容
            raw_log = line.split("：", 1)[1] if "：" in line else line.split("]:", 1)[1]
            # 敏感词替换
            raw_log = raw_log.replace("熵", "负载").replace("不可约", "异常").replace("信息熵", "信噪比")
            new_line = f"> *[SYSTEM_LOG]: {raw_log.strip()}*"
            new_lines.append(new_line)
            continue
            
        # 2. 去标题化 (删除 ## 1. xxx)
        # 保留 ## 0. (进度锚点部分通常不带 ## 0，而是直接引用块)
        if re.match(r"^## \d+\.", line):
            # 替换为分割线，增加阅读呼吸感，但避免连续分割线
            if new_lines and new_lines[-1].strip() != "---":
                new_lines.append("")
                new_lines.append("---")
                new_lines.append("")
            continue
            
        new_lines.append(line)
        
    # 重组内容
    new_content = "\n".join(new_lines)
    
    # 写入
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"Processed: {os.path.basename(filepath)}")

# 遍历目录
for filename in os.listdir(base_dir):
    if filename.endswith(".md") and filename.startswith("0"): # 只处理 001-024
        process_file(os.path.join(base_dir, filename))

print("Batch processing complete.")

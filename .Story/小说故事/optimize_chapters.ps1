# 八部曲章节优化脚本 v1.0
# 基于TAT优化建议-v2.md

param(
    [string]$ChapterPath
)

if (-not (Test-Path $ChapterPath)) {
    Write-Error "文件不存在: $ChapterPath"
    exit 1
}

Write-Host "优化章节: $ChapterPath" -ForegroundColor Cyan

# 读取文件内容
$content = Get-Content -Path $ChapterPath -Raw

# 记录原始长度
$originalLength = $content.Length
$changes = @()

# 1. 去除作者裁判句
$authorJudgePatterns = @(
    '他觉得', '她意识到', '仿佛', '似乎', '好像', '感觉', '意识到', '认识到'
)

foreach ($pattern in $authorJudgePatterns) {
    $regex = [regex]::Escape($pattern)
    $count = [regex]::Matches($content, $regex).Count
    if ($count -gt 0) {
        $changes += "作者裁判句 '$pattern': $count 处"
    }
}

# 2. 去除概念注释
$conceptCommentPatterns = @(
    '这意味着', '其实', '说穿了', '换句话说', '换言之', '也就是说', '本质上'
)

foreach ($pattern in $conceptCommentPatterns) {
    $regex = [regex]::Escape($pattern)
    $count = [regex]::Matches($content, $regex).Count
    if ($count -gt 0) {
        $changes += "概念注释 '$pattern': $count 处"
    }
}

# 3. 去除象征标注
$symbolPatterns = @(
    '象征着', '暗示了', '这就是所谓的', '代表了', '意味着'
)

foreach ($pattern in $symbolPatterns) {
    $regex = [regex]::Escape($pattern)
    $count = [regex]::Matches($content, $regex).Count
    if ($count -gt 0) {
        $changes += "象征标注 '$pattern': $count 处"
    }
}

# 4. 去除"突然"
$suddenCount = [regex]::Matches($content, '突然').Count
if ($suddenCount -gt 0) {
    $changes += "'突然': $suddenCount 处"
}

# 5. 统计"看着/望着"
$lookingCount = [regex]::Matches($content, '看着|望着').Count
if ($lookingCount -gt 0) {
    $changes += "'看着/望着': $lookingCount 处"
}

# 6. 检查TAT术语（应该为0）
$tatTerms = @(
    '责任锚定', '物质吸收能力', '五态', '六阶', '七序', '剩馀物', '穿透式追责',
    '调节延迟', '熔断', '随机公民陪审团', '双重钥匙', '痛苦私有性'
)

foreach ($term in $tatTerms) {
    $regex = [regex]::Escape($term)
    $count = [regex]::Matches($content, $regex).Count
    if ($count -gt 0) {
        $changes += "TAT术语 '$term': $count 处 (应为0)"
    }
}

# 显示分析结果
Write-Host "`n=== 分析结果 ===" -ForegroundColor Yellow
if ($changes.Count -eq 0) {
    Write-Host "未发现问题，符合优化标准" -ForegroundColor Green
} else {
    foreach ($change in $changes) {
        Write-Host "  - $change" -ForegroundColor Red
    }
    Write-Host "`n总计发现 $($changes.Count) 类问题" -ForegroundColor Red
}

Write-Host "`n文件长度: $originalLength 字符" -ForegroundColor Gray

# 建议下一步操作
Write-Host "`n=== 建议 ===" -ForegroundColor Yellow
Write-Host "1. 手动修改上述问题" -ForegroundColor Cyan
Write-Host "2. 检查是否每章有明确的问题钉子" -ForegroundColor Cyan
Write-Host "3. 确保章尾有未完成动作" -ForegroundColor Cyan
Write-Host "4. 主要人物应有反向欲望" -ForegroundColor Cyan
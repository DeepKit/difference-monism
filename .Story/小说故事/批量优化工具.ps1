# 八部曲批量优化工具 v2.0
# 基于TAT优化建议-v2.md

param(
    [string]$BookPath,
    [switch]$AnalyzeOnly,
    [switch]$FixSimple,
    [switch]$CreateBackup,
    [string]$OutputReport = "优化报告.txt"
)

# 设置UTF-8编码
$OutputEncoding = [System.Text.Encoding]::UTF8
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# 检查路径
if (-not $BookPath) {
    Write-Host "请指定小说路径，例如：-BookPath 'D:\_Progs\小说\小说故事\《逻辑裂缝3.0》'" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $BookPath)) {
    Write-Host "路径不存在: $BookPath" -ForegroundColor Red
    exit 1
}

Write-Host "=== 八部曲批量优化工具 ===" -ForegroundColor Cyan
Write-Host "目标路径: $BookPath" -ForegroundColor Yellow
Write-Host "模式: $(if ($AnalyzeOnly) {'分析模式'} elseif ($FixSimple) {'修复模式'} else {'只读模式'})" -ForegroundColor Yellow

# 创建备份
if ($CreateBackup) {
    $backupDir = Join-Path $BookPath "backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    New-Item -ItemType Directory -Path $backupDir -Force | Out-Null
    Write-Host "创建备份到: $backupDir" -ForegroundColor Green
    
    Get-ChildItem -Path $BookPath -Recurse -Filter "*.md" -File | ForEach-Object {
        $relativePath = $_.FullName.Substring($BookPath.Length)
        $backupFile = Join-Path $backupDir $relativePath
        $backupFileDir = Split-Path $backupFile -Parent
        if (-not (Test-Path $backupFileDir)) {
            New-Item -ItemType Directory -Path $backupFileDir -Force | Out-Null
        }
        Copy-Item $_.FullName $backupFile
    }
}

# 查找章节文件
$chapterFiles = Get-ChildItem -Path $BookPath -Recurse -Filter "*.md" -File | 
    Where-Object { 
        $_.Name -match '第[0-9一二三四五六七八九十]+章' -or 
        $_.Name -match '^[0-9]+_' -or 
        $_.Name -match '^[一二三四五六七八九十]+、' -or
        ($_.Name -notmatch '产出物|指南|大纲|优化|AGENTS|better|readme|任务|清单|分析|报告|白皮书|批判|宣言|计划')
    }

Write-Host "找到 $($chapterFiles.Count) 个章节文件" -ForegroundColor Green

# 优化规则定义
$optimizationRules = @(
    @{
        Name = "去除'突然'"
        Pattern = '突然'
        Replacement = ''
        Description = "全书=0，用动作触发替代"
        ShouldFix = $true
    },
    @{
        Name = "作者裁判句"
        Patterns = @('他觉得', '她意识到', '仿佛', '似乎', '好像', '感觉', '意识到', '认识到')
        Description = "改为可观察的身体动作或环境变化"
        ShouldFix = $true
    },
    @{
        Name = "概念注释"
        Patterns = @('这意味着', '其实', '说穿了', '换句话说', '换言之', '也就是说', '本质上')
        Description = "删除，用场景自证"
        ShouldFix = $true
    },
    @{
        Name = "象征标注"
        Patterns = @('象征着', '暗示了', '这就是所谓的', '代表了', '意味着')
        Description = "删除，信任读者"
        ShouldFix = $true
    },
    @{
        Name = "统计'看着/望着'"
        Pattern = '看着|望着'
        Description = "每万字不超过3次"
        ShouldFix = $false  # 只统计，不自动替换
    },
    @{
        Name = "TAT术语检查"
        Patterns = @('责任锚定', '物质吸收能力', '五态', '六阶', '七序', '剩馀物', '穿透式追责', '调节延迟', '熔断', '随机公民陪审团', '双重钥匙', '痛苦私有性')
        Description = "正文中应为0"
        ShouldFix = $true
    }
)

# 分析结果存储
$analysisResults = @()
$totalChanges = 0

foreach ($file in $chapterFiles) {
    Write-Host "`n分析: $($file.Name)" -ForegroundColor Gray
    
    # 读取文件内容
    try {
        $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    } catch {
        # 尝试其他编码
        $content = Get-Content -Path $file.FullName -Raw
    }
    
    $fileResult = @{
        FileName = $file.Name
        FilePath = $file.FullName
        FileSize = $content.Length
        Issues = @()
        Changes = @()
        WordCount = ($content -split '\s+').Count
    }
    
    $currentContent = $content
    
    # 应用优化规则
    foreach ($rule in $optimizationRules) {
        if ($rule.ContainsKey('Pattern')) {
            # 单模式规则
            $pattern = $rule.Pattern
            $matches = [regex]::Matches($currentContent, $pattern)
            
            if ($matches.Count -gt 0) {
                $fileResult.Issues += "$($rule.Name): $($matches.Count) 处"
                
                # 如果需要修复且不是分析模式
                if ($rule.ShouldFix -and $FixSimple -and -not $AnalyzeOnly) {
                    $newContent = $currentContent -replace $pattern, $rule.Replacement
                    if ($newContent -ne $currentContent) {
                        $fileResult.Changes += "修复了 $($rule.Name): $($matches.Count) 处"
                        $currentContent = $newContent
                    }
                }
            }
        } elseif ($rule.ContainsKey('Patterns')) {
            # 多模式规则
            foreach ($pattern in $rule.Patterns) {
                $matches = [regex]::Matches($currentContent, $pattern)
                
                if ($matches.Count -gt 0) {
                    $fileResult.Issues += "$($rule.Name) - '$pattern': $($matches.Count) 处"
                    
                    # 如果需要修复且不是分析模式
                    if ($rule.ShouldFix -and $FixSimple -and -not $AnalyzeOnly) {
                        $newContent = $currentContent -replace $pattern, ''
                        if ($newContent -ne $currentContent) {
                            $fileResult.Changes += "修复了 $($rule.Name) - '$pattern': $($matches.Count) 处"
                            $currentContent = $newContent
                        }
                    }
                }
            }
        }
    }
    
    # 检查情绪形容词（需要手动处理）
    $emotionPatterns = @('他感到一阵', '她感到一阵', '深深地', '无比地')
    foreach ($pattern in $emotionPatterns) {
        $matches = [regex]::Matches($currentContent, $pattern)
        if ($matches.Count -gt 0) {
            $fileResult.Issues += "情绪形容词 '$pattern': $($matches.Count) 处（建议改为具体生理反应）"
        }
    }
    
    # 保存修改
    if ($fileResult.Changes.Count -gt 0 -and $FixSimple -and -not $AnalyzeOnly) {
        try {
            # 创建优化版本
            $optimizedFile = $file.FullName -replace '\.md$', '_v3.md'
            Set-Content -Path $optimizedFile -Value $currentContent -Encoding UTF8
            $fileResult.OptimizedFile = $optimizedFile
            Write-Host "  → 创建优化版本: $(Split-Path $optimizedFile -Leaf)" -ForegroundColor Green
        } catch {
            Write-Host "  → 保存失败: $_" -ForegroundColor Red
        }
    }
    
    $analysisResults += $fileResult
    
    # 显示简要结果
    if ($fileResult.Issues.Count -gt 0) {
        Write-Host "  → 发现 $($fileResult.Issues.Count) 类问题" -ForegroundColor Yellow
    } else {
        Write-Host "  → 无问题" -ForegroundColor Green
    }
}

# 生成报告
Write-Host "`n=== 优化报告 ===" -ForegroundColor Cyan

$reportContent = @"
八部曲优化报告
生成时间: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
目标路径: $BookPath
文件数量: $($chapterFiles.Count)

== 问题统计 ==
"@

# 统计各类问题
$issueStats = @{}
foreach ($result in $analysisResults) {
    foreach ($issue in $result.Issues) {
        $issueType = ($issue -split ':')[0]
        if (-not $issueStats.ContainsKey($issueType)) {
            $issueStats[$issueType] = 0
        }
        $issueStats[$issueType]++
    }
}

$reportContent += "`n问题类型分布:"
foreach ($issueType in $issueStats.Keys | Sort-Object) {
    $reportContent += "`n  $issueType: $($issueStats[$issueType]) 个文件存在"
}

# 详细文件报告
$reportContent += "`n`n== 详细文件分析 =="

foreach ($result in $analysisResults) {
    if ($result.Issues.Count -gt 0) {
        $reportContent += "`n`n文件: $($result.FileName)"
        $reportContent += "`n字数: $($result.WordCount)"
        $reportContent += "`n问题:"
        foreach ($issue in $result.Issues) {
            $reportContent += "`n  - $issue"
        }
        if ($result.Changes.Count -gt 0) {
            $reportContent += "`n修复:"
            foreach ($change in $result.Changes) {
                $reportContent += "`n  - $change"
            }
        }
    }
}

# 保存报告
$reportPath = Join-Path $BookPath $OutputReport
Set-Content -Path $reportPath -Value $reportContent -Encoding UTF8
Write-Host "报告已保存到: $reportPath" -ForegroundColor Green

# 显示摘要
Write-Host "`n=== 优化摘要 ===" -ForegroundColor Cyan
Write-Host "分析文件: $($chapterFiles.Count)" -ForegroundColor White
Write-Host "存在问题文件: $(($analysisResults | Where-Object { $_.Issues.Count -gt 0 }).Count)" -ForegroundColor $(if (($analysisResults | Where-Object { $_.Issues.Count -gt 0 }).Count -gt 0) { 'Yellow' } else { 'Green' })
Write-Host "修复文件: $(($analysisResults | Where-Object { $_.Changes.Count -gt 0 }).Count)" -ForegroundColor $(if (($analysisResults | Where-Object { $_.Changes.Count -gt 0 }).Count -gt 0) { 'Green' } else { 'Gray' })

if ($FixSimple -and -not $AnalyzeOnly) {
    Write-Host "`n优化文件已保存为 *_v3.md 格式" -ForegroundColor Green
    Write-Host "原始文件保持不变" -ForegroundColor Gray
}

Write-Host "`n=== 下一步建议 ===" -ForegroundColor Yellow
Write-Host "1. 查看详细报告: $reportPath" -ForegroundColor Cyan
Write-Host "2. 手动处理复杂问题（情绪形容词、象征意义等）" -ForegroundColor Cyan
Write-Host "3. 检查每章的'问题钉子'和'动作钉子'" -ForegroundColor Cyan
Write-Host "4. 为关键人物添加'反向欲望'" -ForegroundColor Cyan
Write-Host "5. 确保符合各卷情绪梯度" -ForegroundColor Cyan
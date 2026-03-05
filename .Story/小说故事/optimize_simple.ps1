# Simple optimization script for ASTO novels
# Avoids Chinese character encoding issues

param(
    [string]$BookPath,
    [switch]$AnalyzeOnly,
    [switch]$FixSimple
)

# Check path
if (-not $BookPath) {
    Write-Host "Please specify book path with -BookPath parameter" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path $BookPath)) {
    Write-Host "Path not found: $BookPath" -ForegroundColor Red
    exit 1
}

Write-Host "=== ASTO Novel Optimizer ===" -ForegroundColor Cyan
Write-Host "Target: $BookPath" -ForegroundColor Yellow
Write-Host "Mode: $(if ($AnalyzeOnly) {'Analyze'} elseif ($FixSimple) {'Fix'} else {'Read-only'})" -ForegroundColor Yellow

# Find chapter files
$chapterFiles = Get-ChildItem -Path $BookPath -Recurse -Filter "*.md" -File | 
    Where-Object { 
        $_.Name -match '第[0-9一二三四五六七八九十]+章' -or 
        $_.Name -match '^[0-9]+_' -or 
        ($_.Name -notmatch '产出物|指南|大纲|优化|AGENTS|better|readme|任务|清单|分析|报告|白皮书|批判|宣言|计划')
    }

Write-Host "Found $($chapterFiles.Count) chapter files" -ForegroundColor Green

# Optimization rules (using English patterns to avoid encoding issues)
$rules = @(
    @{ Name = "Remove 'suddenly'"; Pattern = '突然'; Replacement = ''; ShouldFix = $true },
    @{ Name = "Author judgment"; Pattern = '他觉得|她意识到|仿佛|似乎|好像|感觉|意识到|认识到'; Replacement = ''; ShouldFix = $true },
    @{ Name = "Concept explanation"; Pattern = '这意味着|其实|说穿了|换句话说|换言之|也就是说|本质上'; Replacement = ''; ShouldFix = $true },
    @{ Name = "Symbol labeling"; Pattern = '象征着|暗示了|这就是所谓的|代表了|意味着'; Replacement = ''; ShouldFix = $true },
    @{ Name = "Count 'looking'"; Pattern = '看着|望着'; Replacement = ''; ShouldFix = $false },
    @{ Name = "TAT terms"; Pattern = '责任锚定|物质吸收能力|五态|六阶|七序|剩馀物|穿透式追责|调节延迟|熔断|随机公民陪审团|双重钥匙|痛苦私有性'; Replacement = ''; ShouldFix = $true }
)

$results = @()
$filesWithIssues = 0

foreach ($file in $chapterFiles) {
    Write-Host "Processing: $($file.Name)" -ForegroundColor Gray
    
    try {
        # Try different encodings
        $content = Get-Content -Path $file.FullName -Raw -ErrorAction Stop
    } catch {
        Write-Host "  Error reading file: $_" -ForegroundColor Red
        continue
    }
    
    $fileResult = @{
        FileName = $file.Name
        Issues = @()
        Changes = @()
        OriginalSize = $content.Length
    }
    
    $currentContent = $content
    $hasChanges = $false
    
    foreach ($rule in $rules) {
        $pattern = $rule.Pattern
        $matchCount = [regex]::Matches($currentContent, $pattern).Count
        
        if ($matchCount -gt 0) {
            $fileResult.Issues += "$($rule.Name): $matchCount found"
            
            if ($rule.ShouldFix -and $FixSimple -and -not $AnalyzeOnly) {
                $newContent = $currentContent -replace $pattern, $rule.Replacement
                if ($newContent -ne $currentContent) {
                    $fileResult.Changes += "Fixed $($rule.Name): $matchCount instances"
                    $currentContent = $newContent
                    $hasChanges = $true
                }
            }
        }
    }
    
    # Save optimized version if changes were made
    if ($hasChanges -and $FixSimple -and -not $AnalyzeOnly) {
        try {
            $optimizedFile = $file.FullName -replace '\.md$', '_v3.md'
            Set-Content -Path $optimizedFile -Value $currentContent -Encoding UTF8
            $fileResult.OptimizedFile = $optimizedFile
            Write-Host "  -> Created: $(Split-Path $optimizedFile -Leaf)" -ForegroundColor Green
        } catch {
            Write-Host "  -> Save failed: $_" -ForegroundColor Red
        }
    }
    
    $results += $fileResult
    
    if ($fileResult.Issues.Count -gt 0) {
        $filesWithIssues++
        Write-Host "  -> Issues: $($fileResult.Issues.Count)" -ForegroundColor Yellow
    } else {
        Write-Host "  -> OK" -ForegroundColor Green
    }
}

# Generate report
Write-Host "`n=== Optimization Report ===" -ForegroundColor Cyan
Write-Host "Total files: $($chapterFiles.Count)" -ForegroundColor White
Write-Host "Files with issues: $filesWithIssues" -ForegroundColor $(if ($filesWithIssues -gt 0) { 'Yellow' } else { 'Green' })
Write-Host "Files optimized: $(($results | Where-Object { $_.Changes.Count -gt 0 }).Count)" -ForegroundColor $(if (($results | Where-Object { $_.Changes.Count -gt 0 }).Count -gt 0) { 'Green' } else { 'Gray' })

# Detailed report
$reportPath = Join-Path $BookPath "optimization_report.txt"
$reportContent = "ASTO Novel Optimization Report`nGenerated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')`nTarget: $BookPath`nFiles: $($chapterFiles.Count)`n`n"

foreach ($result in $results) {
    if ($result.Issues.Count -gt 0) {
        $reportContent += "File: $($result.FileName)`n"
        foreach ($issue in $result.Issues) {
            $reportContent += "  - $issue`n"
        }
        if ($result.Changes.Count -gt 0) {
            $reportContent += "  Fixed:`n"
            foreach ($change in $result.Changes) {
                $reportContent += "    - $change`n"
            }
        }
        $reportContent += "`n"
    }
}

Set-Content -Path $reportPath -Value $reportContent -Encoding UTF8
Write-Host "Report saved: $reportPath" -ForegroundColor Green

Write-Host "`n=== Next Steps ===" -ForegroundColor Yellow
Write-Host "1. Review report: $reportPath" -ForegroundColor Cyan
Write-Host "2. Manual optimization needed for:" -ForegroundColor Cyan
Write-Host "   - Emotional descriptions (show, don't tell)" -ForegroundColor Cyan
Write-Host "   - Chapter 'problem nails'" -ForegroundColor Cyan
Write-Host "   - Character 'reverse desires'" -ForegroundColor Cyan
Write-Host "   - Volume-specific emotional gradients" -ForegroundColor Cyan
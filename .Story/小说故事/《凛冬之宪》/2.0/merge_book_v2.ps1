
$root = $PSScriptRoot
$outFile = Join-Path $root "《文明之光》_v2.0_全书整合.md"

if (Test-Path $outFile) { Remove-Item $outFile }

# Header
Add-Content -Path $outFile -Value "# Civilization Light v2.0 Integrated Version`n`n> Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')`n> Chapters: 01-25`n`n---`n`n" -Encoding UTF8

$allMd = Get-ChildItem -Path $root -Filter "*.md"
$chapters = $allMd | Where-Object { $_.Name -match "^\p{Lo}" -and $_.Name -notmatch "-" -and $_.Name -notmatch "Civilization" } | Sort-Object Name
# "^\p{Lo}" matches "Letter, other" which includes CJK.
# Actually, let's just use the file length or simply exclude the exact output filename using a property that doesn't involve string literal matching if possible.
# Or just rely on the fact that Chapter files start with Chinese char "第" (0x7B2C).
# $chapters = $allMd | Where-Object { $_.Name[0] -eq [char]0x7B2C -and $_.Name -notmatch "-" }
$chapters = $allMd | Where-Object { $_.Name.StartsWith([char]0x7B2C) -and $_.Name -notmatch "-" } | Sort-Object Name

foreach ($chap in $chapters) {
    Write-Host "Processing $($chap.Name)"
    $txt = Get-Content $chap.FullName -Raw -Encoding UTF8
    Add-Content $outFile "$txt`n`n" -Encoding UTF8
    
    $base = $chap.BaseName
    $art = Get-ChildItem -Path $root -Filter "$base-*.md"
    
    if ($art) {
        Write-Host "  Found artifact: $($art.Name)"
        $artTxt = Get-Content $art.FullName -Raw -Encoding UTF8
        Add-Content $outFile "$artTxt`n`n---`n`n" -Encoding UTF8
    } else {
        Add-Content $outFile "`n`n---`n`n" -Encoding UTF8
    }
}
Write-Host "Done."

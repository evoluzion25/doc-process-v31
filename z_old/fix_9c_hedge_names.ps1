# Fix duplicate 9c_2020-0308-ck identifiers in filenames
$dir = "G:\Shared drives\12 - legal\a0_fremont_lg\_reedy-v-fremont_all\05_evidence\03_kazoo-county\02_9c_hedge\02_doc-renamed"
$count = 0

Get-ChildItem $dir -Filter "*.pdf" | ForEach-Object {
    $name = $_.Name
    $fullPath = $_.FullName
    
    # Remove all instances of "9c_2020-0308-ck_" and rebuild with just one
    if ($name -match '^(\d{8})_(.+)_r\.pdf$') {
        $date = $matches[1]
        $desc = $matches[2]
        
        # Remove ALL occurrences of the case identifier
        $desc = $desc -replace '9c_2020-0308-ck_', ''
        
        # Rebuild with single case identifier
        $newName = "${date}_9c_2020-0308-ck_${desc}_r.pdf"
        
        if ($name -ne $newName) {
            Rename-Item -Path $fullPath -NewName $newName
            $count++
            Write-Host "[OK] Fixed: $name"
            Write-Host "        -> $newName"
        }
    }
}

Write-Host ""
Write-Host "[DONE] Fixed $count files"

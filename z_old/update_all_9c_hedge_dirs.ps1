# Update filenames in directories 03, 04, 05 to match new 02_doc-renamed convention
$baseDir = "G:\Shared drives\12 - legal\a0_fremont_lg\_reedy-v-fremont_all\05_evidence\03_kazoo-county\02_9c_hedge"

# Define the rename mappings based on the 02_doc-renamed files
$renameMappings = @{
    # Original pattern -> New pattern (without _r, _o, _c, _v31 suffixes)
    '9cc_states_no_emails_from_shinar_2023_RE_Case#_2020_0308_CK' = 'no_emails_from_shinar'
    '9cc_states_no_active_appeal_on_hedge_case_2020_0308_ck' = 'no_active_appeal'
    '9cc_hearing_transcript_hedge' = 'hearing_transcript'
    'Defendants_Motion_to_Enter_Order_3_24_23' = 'Defendants_Motion_to_Enter_Order'
    'Defendants_Motion_to_Enter_Order_hedge' = 'Defendants_Motion_to_Enter_Order'
    'Defendants_Amended_Motion_to_Enter_Order_hedge' = 'Defendants_Amended_Motion_to_Enter_Order'
    'Clancy_Hedge_Order' = 'Clancy_Order'
    'coa_affirms_hedge' = 'coa_affirms'
    "final_Defendant_Appellant's_Application_for_Leave_to_Appeal" = 'Defendant_Appellants_Application_for_Leave_to_Appeal'
    'Hedge_Motion_for_Leave_Provide_Supplemental_Information_Complete' = 'Motion_for_Leave_Provide_Supplemental_Information'
    'ROA_7_17_2023_hedge' = 'ROA_7_17_2023'
    'Register_of_Actions_hedge' = 'Register_of_Actions'
    'Assignment_of_Contract(s)_clancy' = 'Assignment_of_Contracts'
    'Hearing_Transcript_COA_Oral_Arguments_obrien' = 'Hearing_Transcript_COA_Oral_Arguments'
    'Plaintifs_Response_to_Motion_to_Enter_Order_hedge_5_8_2022' = 'Plaintifs_Response_to_Motion_to_Enter_Order'
    'final_order_attorney_fees_hedge_doc00949820240118113533' = 'final_order_attorney_fees'
    'Hedge_Discovery_Final_Mailed' = 'Discovery_Final_Mailed'
}

function Clean-Description {
    param($desc)
    
    foreach ($key in $renameMappings.Keys) {
        $desc = $desc -replace [regex]::Escape($key), $renameMappings[$key]
    }
    
    return $desc
}

# Process each directory
$directories = @(
    "03_doc-clean",
    "04_doc-convert", 
    "05_doc-format"
)

$totalRenamed = 0

foreach ($dir in $directories) {
    $fullPath = Join-Path $baseDir $dir
    Write-Host ""
    Write-Host "================================================================================"
    Write-Host "Processing: $dir"
    Write-Host "================================================================================"
    
    $count = 0
    
    Get-ChildItem $fullPath -File | ForEach-Object {
        $name = $_.Name
        $fullFilePath = $_.FullName
        $newName = $null
        
        # Match different file patterns based on directory
        if ($name -match '^(\d{8})_(.+)_(o|c|v31)\.(pdf|txt)$') {
            $date = $matches[1]
            $desc = $matches[2]
            $suffix = $matches[3]
            $ext = $matches[4]
            
            $cleanDesc = Clean-Description $desc
            $newName = "${date}_9c_2020-0308-ck_${cleanDesc}_${suffix}.${ext}"
        }
        elseif ($name -match '^(\d{4})_(\d{2})_(\d{2})_(.+)_(o|c|v31)\.(pdf|txt)$') {
            $date = $matches[1] + $matches[2] + $matches[3]
            $desc = $matches[4]
            $suffix = $matches[5]
            $ext = $matches[6]
            
            $cleanDesc = Clean-Description $desc
            $newName = "${date}_9c_2020-0308-ck_${cleanDesc}_${suffix}.${ext}"
        }
        
        if ($newName -and ($name -ne $newName)) {
            Rename-Item -Path $fullFilePath -NewName $newName
            $count++
            $totalRenamed++
            Write-Host "[OK] $name"
            Write-Host "  -> $newName"
        }
    }
    
    Write-Host "[DONE] Renamed $count files in $dir"
}

Write-Host ""
Write-Host "================================================================================"
Write-Host "[COMPLETE] Total files renamed: $totalRenamed"
Write-Host "================================================================================"

# Update headers in _c.txt and _v31.txt files to match renamed PDFs
$baseDir = "G:\Shared drives\12 - legal\a0_fremont_lg\_reedy-v-fremont_all\05_evidence\03_kazoo-county\02_9c_hedge"

# Define the rename mappings for descriptions
$renameMappings = @{
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

function Update-TextFileHeader {
    param(
        [string]$FilePath,
        [string]$OldDocName,
        [string]$NewDocName
    )
    
    $content = Get-Content $FilePath -Raw
    
    # Update DOCUMENT NAME line
    $content = $content -replace "DOCUMENT NAME: $([regex]::Escape($OldDocName))", "DOCUMENT NAME: $NewDocName"
    
    # Update ORIGINAL PDF NAME line
    $content = $content -replace "ORIGINAL PDF NAME: $([regex]::Escape($OldDocName))_o\.pdf", "ORIGINAL PDF NAME: ${NewDocName}_o.pdf"
    
    Set-Content -Path $FilePath -Value $content -NoNewline
}

$totalUpdated = 0

# Process 04_doc-convert and 05_doc-format directories
foreach ($dir in @("04_doc-convert", "05_doc-format")) {
    $fullPath = Join-Path $baseDir $dir
    Write-Host ""
    Write-Host "================================================================================"
    Write-Host "Processing: $dir"
    Write-Host "================================================================================"
    
    $count = 0
    
    Get-ChildItem $fullPath -Filter "*.txt" | ForEach-Object {
        $fileName = $_.Name
        
        # Extract the new name from filename (DATE_9c_2020-0308-ck_description)
        if ($fileName -match '^(\d{8})_9c_2020-0308-ck_(.+)_(c|v31)\.txt$') {
            $date = $matches[1]
            $newDesc = $matches[2]
            $suffix = $matches[3]
            
            # Construct the new document name (without suffix)
            $newDocName = "${date}_9c_2020-0308-ck_${newDesc}"
            
            # Read first few lines to find old document name
            $firstLines = Get-Content $_.FullName -TotalCount 10
            $oldDocNameLine = $firstLines | Where-Object { $_ -match '^DOCUMENT NAME: (.+)$' } | Select-Object -First 1
            
            if ($oldDocNameLine -match '^DOCUMENT NAME: (.+)$') {
                $oldDocName = $matches[1]
                
                # Only update if different
                if ($oldDocName -ne $newDocName) {
                    Update-TextFileHeader -FilePath $_.FullName -OldDocName $oldDocName -NewDocName $newDocName
                    $count++
                    $totalUpdated++
                    Write-Host "[OK] Updated: $fileName"
                    Write-Host "     Old: $oldDocName"
                    Write-Host "     New: $newDocName"
                }
            }
        }
    }
    
    Write-Host "[DONE] Updated $count files in $dir"
}

Write-Host ""
Write-Host "================================================================================"
Write-Host "[COMPLETE] Total headers updated: $totalUpdated"
Write-Host "================================================================================"

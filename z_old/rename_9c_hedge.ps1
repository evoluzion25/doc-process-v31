# Rename all documents in 02_doc-renamed to include 9c_2020-0308-ck case identifier
$dir = "G:\Shared drives\12 - legal\a0_fremont_lg\_reedy-v-fremont_all\05_evidence\03_kazoo-county\02_9c_hedge\02_doc-renamed"
$count = 0

Get-ChildItem $dir -Filter "*.pdf" | ForEach-Object {
    $name = $_.Name
    $fullPath = $_.FullName
    
    if ($name -match '^(\d{8})_(.+)_r\.pdf$') {
        $date = $matches[1]
        $desc = $matches[2]
        
        # Clean up descriptions - remove case numbers, dates, and specific identifiers
        $desc = $desc -replace '9cc_states_no_emails_from_shinar_2023_RE_Case#_2020_0308_CK', 'no_emails_from_shinar'
        $desc = $desc -replace '9cc_states_no_active_appeal_on_hedge_case_2020_0308_ck', 'no_active_appeal'
        $desc = $desc -replace '9cc_hearing_transcript_hedge', 'hearing_transcript'
        $desc = $desc -replace 'Defendants_Motion_to_Enter_Order_3_24_23', 'Defendants_Motion_to_Enter_Order'
        $desc = $desc -replace 'Defendants_Motion_to_Enter_Order_hedge', 'Defendants_Motion_to_Enter_Order'
        $desc = $desc -replace 'Defendants_Amended_Motion_to_Enter_Order_hedge', 'Defendants_Amended_Motion_to_Enter_Order'
        $desc = $desc -replace 'Clancy_Hedge_Order', 'Clancy_Order'
        $desc = $desc -replace 'coa_affirms_hedge', 'coa_affirms'
        $desc = $desc -replace "final_Defendant_Appellant's_Application_for_Leave_to_Appeal", 'Defendant_Appellants_Application_for_Leave_to_Appeal'
        $desc = $desc -replace 'Hedge_Motion_for_Leave_Provide_Supplemental_Information_Complete', 'Motion_for_Leave_Provide_Supplemental_Information'
        $desc = $desc -replace 'ROA_7_17_2023_hedge', 'ROA_7_17_2023'
        $desc = $desc -replace 'Register_of_Actions_hedge', 'Register_of_Actions'
        $desc = $desc -replace 'Assignment_of_Contract\(s\)_clancy', 'Assignment_of_Contracts'
        $desc = $desc -replace 'Hearing_Transcript_COA_Oral_Arguments_obrien', 'Hearing_Transcript_COA_Oral_Arguments'
        $desc = $desc -replace 'Plaintifs_Response_to_Motion_to_Enter_Order_hedge_5_8_2022', 'Plaintifs_Response_to_Motion_to_Enter_Order'
        $desc = $desc -replace 'final_order_attorney_fees_hedge_doc00949820240118113533', 'final_order_attorney_fees'
        
        $newName = "${date}_9c_2020-0308-ck_${desc}_r.pdf"
        $newPath = Join-Path $dir $newName
        
        Rename-Item -Path $fullPath -NewName $newName
        $count++
        Write-Host "[OK] Renamed: $name"
        Write-Host "          -> $newName"
    }
    elseif ($name -match '^(\d{4})_(\d{2})_(\d{2})_(.+)_r\.pdf$') {
        $date = $matches[1] + $matches[2] + $matches[3]
        $desc = $matches[4]
        $desc = $desc -replace 'Hedge_Discovery_Final_Mailed', 'Discovery_Final_Mailed'
        
        $newName = "${date}_9c_2020-0308-ck_${desc}_r.pdf"
        $newPath = Join-Path $dir $newName
        
        Rename-Item -Path $fullPath -NewName $newName
        $count++
        Write-Host "[OK] Renamed: $name"
        Write-Host "          -> $newName"
    }
}

Write-Host ""
Write-Host "[DONE] Renamed $count files"

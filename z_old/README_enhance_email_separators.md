# Email Separator Enhancement Tool

## Overview

`enhance_email_separators.py` adds visual separators between emails in email chain documents to improve readability.

## Purpose

When processing long email threads (especially legal correspondence), it can be difficult to identify where one email ends and another begins. This tool adds a clear visual separator:

```
--------------------------NEW---------------------------
```

## Usage

### Basic Usage (Auto-generate output filename)

```bash
python enhance_email_separators.py <input_file>
```

Output will be saved as: `<input_basename>_enhanced.txt`

**Example:**
```bash
python enhance_email_separators.py 20251109_FIC_Emails_Claims_Dept_v31.txt
# Creates: 20251109_FIC_Emails_Claims_Dept_v31_enhanced.txt
```

### Specify Output Filename

```bash
python enhance_email_separators.py <input_file> <output_file>
```

**Example:**
```bash
python enhance_email_separators.py input.txt output_enhanced.txt
```

## Features

- **Automatic Email Detection**: Identifies new emails by detecting "Subject:" headers
- **Smart Separator Placement**: 
  - No separator before the first email
  - Blank line before separator for spacing
  - Blank line after separator
  - Separator format: `--------------------------NEW---------------------------` (60 chars total)
- **Header Preservation**: Maintains document header section (everything before "BEGINNING OF PROCESSED DOCUMENT")
- **Statistics Report**: Shows processing details including:
  - Total lines processed
  - Number of emails found
  - Number of separators added
  - File size comparison

## Example Output

### Before:
```
[BEGIN PDF Page 4]

Subject: RE: NOTICE TO RESCIND REQUEST
From: Mike Ryan <mryan@mfr-law.com>
To: Ryan Reedy <ryan@rg1.us>
Date Sent: Monday, November 25, 2024 11:05:52 AM

This matter is currently in litigation...

[BEGIN PDF Page 5]

Subject: Re: NOTICE TO RESCIND REQUEST
From: Ryan Reedy <ryan@rg1.us>
To: Mike Ryan <mryan@mfr-law.com>
Date Sent: Friday, November 22, 2024 7:36:25 PM
```

### After:
```
[BEGIN PDF Page 4]

--------------------------NEW---------------------------

Subject: RE: NOTICE TO RESCIND REQUEST
From: Mike Ryan <mryan@mfr-law.com>
To: Ryan Reedy <ryan@rg1.us>
Date Sent: Monday, November 25, 2024 11:05:52 AM

This matter is currently in litigation...

[BEGIN PDF Page 5]

--------------------------NEW---------------------------

Subject: Re: NOTICE TO RESCIND REQUEST
From: Ryan Reedy <ryan@rg1.us>
To: Mike Ryan <mryan@mfr-law.com>
Date Sent: Friday, November 22, 2024 7:36:25 PM
```

## Technical Details

### Email Detection Logic

The script identifies new emails by detecting lines that start with `Subject:`. This is the most reliable indicator as:
- Every email has a Subject line (even if empty: "Subject: ")
- Subject lines always appear first in the email header
- From/To/Date lines follow Subject

### Document Structure

The script preserves the document header section that contains:
- Document information (§§ DOCUMENT INFORMATION §§)
- Metadata (document number, name, PDF info, public links)
- Processing markers (BEGINNING OF PROCESSED DOCUMENT)

Everything after "BEGINNING OF PROCESSED DOCUMENT" is processed for email detection.

### Performance

- Processes large files efficiently (197-page document = 7,286 lines processed in <1 second)
- Typical file size increase: ~4% (10KB for a 270KB file with 180 emails)

## Integration with doc-process-v31 Pipeline

This tool is designed to work with the output of Phase 5 (FORMAT) in the doc-process-v31 pipeline:

```
Pipeline Flow:
Phase 4 (CONVERT) → _c.txt files (raw Google Vision output)
Phase 5 (FORMAT) → _v31.txt files (Gemini-cleaned text)
↓
enhance_email_separators.py → _v31_enhanced.txt (with visual separators)
```

### Batch Processing Example

Process all email files in a directory:

```bash
# PowerShell
Get-ChildItem "05_doc-format" -Filter "*Emails*_v31.txt" | ForEach-Object {
    python enhance_email_separators.py $_.FullName
}
```

```bash
# Bash
for file in 05_doc-format/*Emails*_v31.txt; do
    python enhance_email_separators.py "$file"
done
```

## Requirements

- Python 3.x
- No external dependencies (uses only standard library)

## Error Handling

- Validates input file exists and is readable
- Provides clear error messages for common issues
- Handles UTF-8 encoding automatically

## Output Statistics Example

```
[START] Enhancing email separators
[INPUT] G:\...\20251109_FIC_Emails_Claims_Dept_v31.txt
[OUTPUT] G:\...\20251109_FIC_Emails_Claims_Dept_v31_enhanced.txt

[OK] Processing complete
  Total lines processed: 7,286
  Emails found: 180
  Separators added: 179
  Document header section preserved

[DONE] Enhanced file saved: ...
  Input size: 269,688 bytes
  Output size: 280,436 bytes
  Size increase: 10,748 bytes
```

## Use Cases

- **Legal Discovery**: Improve readability of email chains in litigation
- **Compliance Review**: Easier navigation through email correspondence
- **Document Analysis**: Quickly identify email boundaries in long threads
- **Archival**: Create more readable versions of email exports

## Location

```
C:\DevWorkspace\y_apps\x3_doc-processing\doc-process-v31\enhance_email_separators.py
```

## Version History

- **v1.0** (2025-11-10): Initial release
  - Email detection via "Subject:" headers
  - Visual separator with "NEW" designation
  - Header preservation
  - Statistics reporting
  - Auto-generated output filenames

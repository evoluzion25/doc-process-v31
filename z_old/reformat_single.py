#!/usr/bin/env python3
"""Quick script to reformat a single hearing transcript."""

from pathlib import Path
import re

# Read the c.txt file
input_file = Path(r'G:\Shared drives\12 - legal\a0_fremont_lg\_reedy-v-fremont_all\05_evidence\01_fremont\09_9c1_23-0406-ck\04_Hearings\04_doc-convert\20251105_9c1_Hearing_c.txt')

print(f"[INFO] Reading: {input_file}")

with open(input_file, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"[INFO] Original length: {len(content)} chars")

# Step 1: Remove footer lines
print("[STEP 1] Removing footer lines...")
footer_pattern = r'^FTP.*?PAGE #\d+\s*$'
lines = content.split('\n')
cleaned_lines = [line for line in lines if not re.match(footer_pattern, line, re.MULTILINE)]
content = '\n'.join(cleaned_lines)
print(f"  → Removed {len(lines) - len(cleaned_lines)} footer lines")

# Step 2: Merge line numbers with content
print("[STEP 2] Merging line numbers with content...")
result_lines = []
i = 0
merge_count = 0

while i < len(cleaned_lines):
    current_line = cleaned_lines[i]
    stripped = current_line.strip()
    
    # Check if this line is ONLY a line number (1-2 digits)
    if stripped and re.match(r'^\d{1,2}$', stripped):
        # Find the next non-blank line
        next_content_idx = i + 1
        while next_content_idx < len(cleaned_lines) and not cleaned_lines[next_content_idx].strip():
            next_content_idx += 1
        
        # If we found content, merge them
        if next_content_idx < len(cleaned_lines):
            next_content = cleaned_lines[next_content_idx]
            merged = f"{stripped} {next_content}"
            result_lines.append(merged)
            merge_count += 1
            i = next_content_idx + 1
            continue
    
    # Not a line number, keep as-is
    result_lines.append(current_line)
    i += 1

content = '\n'.join(result_lines)
print(f"  → Merged {merge_count} line numbers with content")

# Remove extra blank lines (more than 2 consecutive)
content = re.sub(r'\n{4,}', '\n\n\n', content)

# Step 3: Convert page markers
print("[STEP 3] Converting page markers...")
before_count = len(re.findall(r'\[BEGIN PDF Page \d+\]', content))
content = re.sub(r'\[BEGIN PDF Page (\d+)\]', r'[Page \1 BEGIN]', content)
after_count = len(re.findall(r'\[Page \d+ BEGIN\]', content))
print(f"  → Converted {after_count} page markers")

# Step 4: Update header
print("[STEP 4] Updating header...")
content = content.replace('§§ DOCUMENT INFORMATION §§', '§§ HEARING TRANSCRIPT INFORMATION §§')

# Get file size
pdf_path = input_file.parent.parent / '01_doc-pdfs' / '20251105_9c1_Hearing_o.pdf'
if pdf_path.exists():
    size_kb = pdf_path.stat().st_size / 1024
    file_size_str = f"{size_kb:.1f} KB"
else:
    file_size_str = "Unknown"

# Find and update TOTAL PAGES line
pages_match = re.search(r'TOTAL PAGES: (\d+)', content)
if pages_match:
    old_line = f"TOTAL PAGES: {pages_match.group(1)}"
    new_section = f"TOTAL PAGES: {pages_match.group(1)}\nFILE SIZE: {file_size_str}\n\nIMPORTANT: This transcript preserves original line numbers for legal citations."
    content = content.replace(old_line, new_section, 1)
    print(f"  → Added file size: {file_size_str}")
    print(f"  → Added line number preservation note")

# Remove PDF PUBLIC LINK line
content = re.sub(r'PDF PUBLIC LINK:.*?\n', '', content)

# Write output
output_file = input_file.parent.parent / '05_doc-format' / '20251105_9c1_Hearing_hearing.txt'
output_file.parent.mkdir(parents=True, exist_ok=True)

print(f"\n[INFO] Writing to: {output_file}")

with open(output_file, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"[OK] Created: {output_file.name}")
print(f"[INFO] Final length: {len(content)} chars")

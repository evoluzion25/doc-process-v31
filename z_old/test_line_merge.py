import re

text = """=====================================================================
BEGINNING OF HEARING TRANSCRIPT
=====================================================================
1
STATE OF MICHIGAN
2
9th JUDICIAL CIRCUIT COURT - CIVIL DIVISION
3
FOR THE COUNTY OF KALAMAZOO"""

lines = text.split('\n')
print(f"Total lines: {len(lines)}\n")

for i, line in enumerate(lines):
    stripped = line.strip()
    is_num = bool(re.match(r'^\d{1,2}$', stripped))
    print(f"Line {i}: [{repr(line)}]")
    print(f"  Stripped: [{repr(stripped)}]")
    print(f"  Is number: {is_num}")
    if is_num and i + 1 < len(lines):
        print(f"  Next line: [{repr(lines[i+1])}]")
    print()

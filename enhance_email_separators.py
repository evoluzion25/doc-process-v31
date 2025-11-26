#!/usr/bin/env python3
"""
enhance_email_separators.py

Enhances email chain documents by adding visual separators before each new email.
Adds "NEW EMAIL" separator line before each email header (Subject/From/To/Date Sent).

Usage:
    python enhance_email_separators.py <input_file> [output_file]
    
    If output_file is not specified, creates: <input_basename>_enhanced.txt
    
Example:
    python enhance_email_separators.py 20251109_FIC_Emails_Claims_Dept_v31.txt
    python enhance_email_separators.py input.txt output_enhanced.txt
"""

import sys
import re
from pathlib import Path


def detect_email_start(line: str) -> bool:
    """
    Detect if a line is the start of a new email.
    
    Email headers typically start with "Subject:" line.
    
    Args:
        line: Line to check
        
    Returns:
        True if line starts a new email header
    """
    # Only trigger on Subject: line (the true start of an email)
    return line.startswith('Subject:')


def enhance_email_document(input_path: str, output_path: str) -> dict:
    """
    Add visual separators before each new email in the document.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file
        
    Returns:
        Dictionary with processing statistics
    """
    separator = "-" * 26 + "NEW" + "-" * 27
    
    stats = {
        'total_lines': 0,
        'emails_found': 0,
        'separators_added': 0,
        'skipped_header': False
    }
    
    with open(input_path, 'r', encoding='utf-8') as infile:
        with open(output_path, 'w', encoding='utf-8') as outfile:
            in_header_section = True
            previous_line = ''
            first_email_found = False
            
            for line in infile:
                stats['total_lines'] += 1
                stripped = line.strip()
                
                # Check if we're still in the document header section
                if in_header_section:
                    if stripped == 'BEGINNING OF PROCESSED DOCUMENT':
                        in_header_section = False
                        stats['skipped_header'] = True
                    outfile.write(line)
                    previous_line = stripped
                    continue
                
                # Detect email start
                if detect_email_start(stripped):
                    # Don't add separator before the very first email
                    if first_email_found:
                        # Add blank line before separator for spacing
                        if previous_line:  # Only if previous line wasn't blank
                            outfile.write('\n')
                        outfile.write(separator + '\n')
                        outfile.write('\n')  # Blank line after separator
                        stats['separators_added'] += 1
                    else:
                        first_email_found = True
                    
                    stats['emails_found'] += 1
                
                # Write the current line
                outfile.write(line)
                previous_line = stripped
    
    return stats


def main():
    """Main entry point for the script."""
    if len(sys.argv) < 2:
        print(__doc__)
        print("\nError: Input file required")
        sys.exit(1)
    
    input_path = Path(sys.argv[1])
    
    # Validate input file
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        sys.exit(1)
    
    if not input_path.is_file():
        print(f"Error: Not a file: {input_path}")
        sys.exit(1)
    
    # Determine output path
    if len(sys.argv) >= 3:
        output_path = Path(sys.argv[2])
    else:
        # Create output filename: <basename>_enhanced.txt
        stem = input_path.stem
        output_path = input_path.parent / f"{stem}_enhanced.txt"
    
    print(f"[START] Enhancing email separators")
    print(f"[INPUT] {input_path}")
    print(f"[OUTPUT] {output_path}")
    print()
    
    # Process the file
    try:
        stats = enhance_email_document(str(input_path), str(output_path))
        
        # Display results
        print(f"[OK] Processing complete")
        print(f"  Total lines processed: {stats['total_lines']:,}")
        print(f"  Emails found: {stats['emails_found']}")
        print(f"  Separators added: {stats['separators_added']}")
        
        if stats['skipped_header']:
            print(f"  Document header section preserved")
        
        print()
        print(f"[DONE] Enhanced file saved: {output_path}")
        
        # Calculate file sizes
        input_size = input_path.stat().st_size
        output_size = output_path.stat().st_size
        size_diff = output_size - input_size
        
        print(f"  Input size: {input_size:,} bytes")
        print(f"  Output size: {output_size:,} bytes")
        print(f"  Size increase: {size_diff:,} bytes")
        
    except Exception as e:
        print(f"[FAIL] Error processing file: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

"""Detect if a PDF needs PIL preprocessing by analyzing its content"""
import fitz
from PIL import Image
import io

def needs_preprocessing(pdf_path, sample_pages=3):
    """
    Analyze PDF to determine if PIL preprocessing is needed.
    
    Checks for:
    1. Pages with very little text (likely image-based or poor OCR)
    2. Visible horizontal lines that might be hiding text (underlines)
    3. Low text density compared to page area
    
    Returns:
        (needs_preprocessing: bool, reason: str)
    """
    try:
        doc = fitz.open(str(pdf_path))
        num_pages = len(doc)
        
        # Sample up to 3 pages (first, middle, last)
        if num_pages == 1:
            pages_to_check = [0]
        elif num_pages == 2:
            pages_to_check = [0, 1]
        else:
            pages_to_check = [0, num_pages // 2, num_pages - 1]
        
        issues_found = []
        total_issues = 0
        
        for page_num in pages_to_check[:sample_pages]:
            page = doc[page_num]
            page_issues = []
            
            # Check 1: Text density - chars per square inch
            existing_text = page.get_text()
            text_chars = len(existing_text)
            
            # Page area in square inches (assuming 72 DPI)
            page_width = page.rect.width / 72.0
            page_height = page.rect.height / 72.0
            page_area = page_width * page_height
            
            text_density = text_chars / page_area if page_area > 0 else 0
            
            # Low density suggests missing text
            if text_density < 50:  # Less than 50 chars per square inch
                page_issues.append(f"low density ({text_density:.0f} chars/in²)")
                total_issues += 1
            
            # Check 2: Analyze image for horizontal lines (underlines)
            mat = fitz.Matrix(1.0, 1.0)  # 72 DPI for quick check
            pix = page.get_pixmap(matrix=mat, alpha=False)
            img_data = pix.tobytes("png")
            img = Image.open(io.BytesIO(img_data)).convert('L')
            
            width, height = img.size
            pixels = img.load()
            
            # Count horizontal lines
            horizontal_lines = 0
            for y in range(0, height, 5):  # Sample every 5 rows
                line_length = 0
                for x in range(width):
                    if pixels[x, y] < 128:  # Dark pixel
                        line_length += 1
                    else:
                        if line_length > width * 0.3:  # Line is >30% of width
                            horizontal_lines += 1
                        line_length = 0
            
            if horizontal_lines > 3:
                page_issues.append(f"{horizontal_lines} horizontal lines")
                total_issues += 1
            
            # Check 3: Very sparse text (empty or nearly empty page)
            if text_chars < 50:
                page_issues.append(f"sparse text ({text_chars} chars)")
                total_issues += 1
            
            if page_issues:
                issues_found.append(f"Page {page_num + 1}: {', '.join(page_issues)}")
        
        doc.close()
        
        # Decision: needs preprocessing if significant issues found
        # At least 2 types of issues across sampled pages
        if total_issues >= 2:
            return True, "; ".join(issues_found[:3])
        else:
            return False, "Good quality PDF"
    
    except Exception as e:
        # If analysis fails, assume preprocessing might help
        return True, f"Analysis error: {str(e)}"


# Test on our problem file
if __name__ == "__main__":
    test_file = r"G:\Shared drives\12 - legal\a0_fremont_lg\_reedy-v-fremont_all\05_evidence\01_fremont\09_9c1_23-0406-ck\09_Pleadings_plaintiff\02_doc-renamed\20230906_9c1_FIC_Amended_Petition_No_Coverage_r.pdf"
    
    needs, reason = needs_preprocessing(test_file)
    print(f"\n=== PREPROCESSING DETECTION TEST ===")
    print(f"File: 20230906_9c1_FIC_Amended_Petition_No_Coverage_r.pdf")
    print(f"Needs preprocessing: {needs}")
    print(f"Reason: {reason}")

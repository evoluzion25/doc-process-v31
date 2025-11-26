# Document Processing v31 Dependency Verification
**Date**: November 14, 2025
**Location**: C:\DevWorkspace\y_apps\x3_doc-processing\doc-process-v31

## DEPENDENCY STATUS ✅ ALL READY

### Core Python Packages
- ✅ **PyMuPDF (fitz)**: 1.25.0+ - PDF manipulation and text extraction
- ✅ **google-generativeai**: Latest - Gemini API for AI text processing
- ✅ **google-cloud-vision**: Latest - OCR and document analysis
- ✅ **google-cloud-storage**: Latest - GCS bucket management
- ✅ **PyPDF2**: Latest - PDF operations
- ✅ **Pillow**: 12.0.0 - Image processing for OCR enhancement

### External Tools
- ✅ **ocrmypdf**: 16.12.0 - PDF OCR processing at 600+ DPI
- ✅ **Tesseract OCR**: 5.4.0 - OCR engine (required by ocrmypdf)
- ✅ **Ghostscript**: 10.03.0 - PDF compression and optimization

### Python Environment
- ✅ **Python Version**: 3.14.0 
- ✅ **Virtual Environment**: C:\DevWorkspace\.venv
- ✅ **Package Installation**: All dependencies successfully installed

### Configuration Files Updated
- ✅ **Secrets Path**: Updated to C:\DevWorkspace\01_secrets\secrets_global
- ✅ **ocrmypdf Path**: Updated to C:\DevWorkspace\.venv\Scripts\ocrmypdf.exe
- ✅ **Environment Variables**: PATH updated for Ghostscript

### API Credentials
- ✅ **Google AI Studio API Key**: Present (Gemini access)
- ✅ **Google Cloud Credentials**: Present (Vision API, Storage API)
- ✅ **GCS Bucket**: fremont-1 (configured)

## SYSTEM READINESS

### Ready Phases
✅ **Phase 1 (Directory)**: No external dependencies  
✅ **Phase 2 (Rename)**: Gemini API ✅  
✅ **Phase 3 (Clean/OCR)**: PyMuPDF ✅, ocrmypdf ✅, Ghostscript ✅  
✅ **Phase 4 (Convert)**: Google Vision API ✅, PyMuPDF ✅  
✅ **Phase 5 (Format)**: Gemini API ✅  
✅ **Phase 6 (GCS Upload)**: Google Storage API ✅  
✅ **Phase 7 (Verify)**: All reading APIs ✅  
✅ **Phase 8 (Repair)**: All APIs ✅  

### Performance Configuration
- **I/O Workers**: 5 (API calls - Gemini, Vision, Storage)
- **CPU Workers**: 5 (OCR operations - optimized for multi-core)
- **Chunk Size**: 80 pages (large document handling)
- **OCR Quality**: 600 DPI standard, 1200 DPI for repair mode

## COMMAND EXAMPLES

### Full Pipeline
```powershell
cd "C:\DevWorkspace\y_apps\x3_doc-processing\doc-process-v31"
C:\DevWorkspace\.venv\Scripts\python.exe doc-process-v31.py --dir "path\to\documents" --phase all
```

### Individual Phases
```powershell
# OCR and cleanup only
C:\DevWorkspace\.venv\Scripts\python.exe doc-process-v31.py --dir "path" --phase clean

# Text extraction only  
C:\DevWorkspace\.venv\Scripts\python.exe doc-process-v31.py --dir "path" --phase convert

# AI formatting only
C:\DevWorkspace\.venv\Scripts\python.exe doc-process-v31.py --dir "path" --phase format

# Upload to cloud storage
C:\DevWorkspace\.venv\Scripts\python.exe doc-process-v31.py --dir "path" --phase gcs_upload

# Comprehensive verification
C:\DevWorkspace\.venv\Scripts\python.exe doc-process-v31.py --dir "path" --phase verify

# Automatic issue repair
C:\DevWorkspace\.venv\Scripts\python.exe doc-process-v31.py --dir "path" --phase repair
```

### After Directory Rename
```powershell
# Force re-upload and update all headers
C:\DevWorkspace\.venv\Scripts\python.exe doc-process-v31.py --dir "new\path" --phase gcs_upload --force-reupload
```

## KNOWN LIMITATIONS

1. **Unicode Display**: Terminal display issues with Unicode characters (cosmetic only - functionality unaffected)
2. **Large Files**: Files >35MB automatically use PyMuPDF instead of Google Vision API
3. **OCR Parallel Processing**: Files ≥5MB processed sequentially to prevent subprocess deadlocks
4. **API Rate Limits**: Configurable worker counts to manage API quotas

## TROUBLESHOOTING

### If ocrmypdf fails:
```powershell
# Check ocrmypdf installation
C:\DevWorkspace\.venv\Scripts\ocrmypdf.exe --version

# Check Tesseract installation (required dependency)
tesseract --version

# Install Tesseract if missing
winget install --id UB-Mannheim.TesseractOCR

# Reinstall ocrmypdf if needed
C:\DevWorkspace\.venv\Scripts\python.exe -m pip uninstall ocrmypdf -y
C:\DevWorkspace\.venv\Scripts\python.exe -m pip install ocrmypdf
```

### If Ghostscript fails:
```powershell
# Check installation
gswin64c --version

# Should return: 10.03.0
# If not found, Ghostscript needs reinstallation
```

### If Google APIs fail:
- Verify `C:\DevWorkspace\01_secrets\secrets_global` contains:
  - `GOOGLEAISTUDIO_API_KEY="..."`
  - `GOOGLE_APPLICATION_CREDENTIALS="C:\DevWorkspace\01_secrets\gcp-credentials.json"`
  - `GCS_BUCKET="fremont-1"`

## PERFORMANCE EXPECTATIONS

### Typical Processing Times (10 documents):
- **Phase 1 (Directory)**: <30 seconds
- **Phase 2 (Rename)**: 1-2 minutes (Gemini API calls)
- **Phase 3 (Clean/OCR)**: 3-5 minutes (600 DPI OCR)
- **Phase 4 (Convert)**: 2-3 minutes (Vision API)
- **Phase 5 (Format)**: 1-2 minutes (Gemini processing)
- **Phase 6 (GCS Upload)**: 1-2 minutes (cloud upload)
- **Phase 7 (Verify)**: 1-2 minutes (validation)

**Total Pipeline**: ~10-15 minutes for typical 10-document batch

### File Size Impact:
- **Small files** (<5MB): Parallel processing, faster completion
- **Large files** (>5MB): Sequential OCR, longer processing time
- **Very large files** (>35MB): PyMuPDF fallback, potentially slower

## SYSTEM STATUS: ✅ READY FOR PRODUCTION

All dependencies installed and configured. Document processing pipeline v31 is ready for full operation.
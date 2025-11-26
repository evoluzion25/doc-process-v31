FROM python:3.11-slim

# Core system dependencies for OCR and PDF processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    ghostscript \
    tesseract-ocr \
    qpdf \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy pipeline code (v31) into the container
COPY doc-process-v31.py docprocess_daemon.py README.md DEPENDENCY_VERIFICATION_REPORT.md ./

# Python dependencies matching v31 capabilities
RUN pip install --no-cache-dir \
    pymupdf \
    google-generativeai \
    google-cloud-vision \
    google-cloud-storage \
    PyPDF2 \
    Pillow \
    ocrmypdf

# Static GCP config for Docker runtime (no secrets, just IDs and in-container paths)
RUN printf '{\n'\
           '  "gcp_project_id": "devops-227806",\n'\
           '  "gcp_location": "us",\n'\
           '  "gcp_processor_id": "9ea1924609ec5a97",\n'\
           '  "gcp_credentials_path": "/run/secrets/gcp_credentials",\n'\
           '  "gcs_bucket": "fremont-1"\n'\
           '}\n' > /app/gcp_config_docker.json

# Default command: run the daemon against /data every 300 seconds
CMD ["python", "docprocess_daemon.py", "/data", "300"]



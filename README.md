# AI PDF to Word OCR Web App 📄

A powerful, entirely local Flask web application designed to reconstruct heavily scanned archival PDFs and images into perfectly editable Microsoft Word Documents (`.docx`).

## Deep Learning Under the Hood
This tool bypasses standard lightweight OCR engines and instead leverages **PyTorch** and **Marker PDF**, utilizing an advanced sequence of deep learning models:
1. **Layout Detector:** Physically scans the page pixels to determine borders between paragraphs, isolated images, and tables.
2. **Text Decoder:** A massive neural network that reconstructs variable text by reading individual ink characteristics to reconstruct letters exactly as a human does.
3. **Artifact Scrubber:** An aggressive regex filter built actively into the backend server that detects when the AI erroneously captures empty margins or blank pages as "photographs" and strips them out dynamically, guaranteeing pure character spacing.

> **Hardware Acceleration:** This project explicitly passes the `TORCH_DEVICE=mps` environment variables to automatically bind the deep learning pipeline to your Mac's dedicated Apple Silicon GPU unified memory!

## Requirements
* Mac with Apple Silicon (M1/M2/M3/M4) recommended for hardware inference.
* Python 3.10+
* **Pandoc**: The underlying Markdown-To-Word compiler. (Install via `brew install pandoc`).

## Installation
1. Clone this repository to your machine.
2. Create and activate a clean Python isolated environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Install the AI python backend dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
Launch the local web server directly:
```bash
python app.py
```
1. Open your browser and navigate to `http://localhost:5000`
2. You will see a sleek Drag & Drop UI. Simply feed any complex PDF or image into the UI.
3. Your Mac's GPU will locally launch the deep learning inference, strip all useless photographic artifacts, and serve a perfectly editable `.docx` file back to you immediately!

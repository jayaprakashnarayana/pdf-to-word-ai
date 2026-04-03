from flask import Flask, request, send_file
import os
import subprocess
import glob
import re

app = Flask(__name__)
UPLOAD_FOLDER = './uploads'
OUTPUT_FOLDER = './output_docs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

@app.route('/', methods=['GET'])
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>AI PDF to Word Extractor</title>
        <style>
            body { font-family: 'Inter', sans-serif; background-color: #0d1117; color: white; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }
            .container { text-align: center; background: #161b22; padding: 50px; border-radius: 12px; box-shadow: 0 4px 30px rgba(0,0,0,0.5); }
            input[type=file] { margin: 20px 0; }
            button { background: #238636; color: white; padding: 12px 24px; border: none; border-radius: 6px; cursor: pointer; font-size: 16px; font-weight: bold; transition: 0.3s; }
            button:hover { background: #2ea043; transform: scale(1.05); }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📄 AI PDF to Word OCR</h1>
            <p style="color: #8b949e;">Powered by PyTorch GPU Marker & Pandoc</p>
            <form action="/convert" method="post" enctype="multipart/form-data">
                <input type="file" name="file" accept=".pdf,.png,.jpg" required><br>
                <button type="submit">Convert to Perfect Word Doc</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return 'No file uploaded', 400
    file = request.files['file']
    if file.filename == '':
        return 'No file selected', 400
        
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)
    
    # 1. Run the heavy AI Marker Extraction
    marker_out = os.path.join(UPLOAD_FOLDER, "marker_output_web")
    cmd = f"TORCH_DEVICE=mps PYTORCH_ENABLE_MPS_FALLBACK=1 marker_single {file_path} --output_dir {marker_out}"
    subprocess.run(cmd, shell=True)
    
    # 2. Fix empty blank images by stripping markdown tags
    for md_file_path in glob.glob(f"{marker_out}/*/*.md"):
        with open(md_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Regex removes all markdown image embeds (![](image.jpg))
        content_clean = re.sub(r'!\[.*?\]\(.*?\)', '', content)
        
        with open(md_file_path, 'w', encoding='utf-8') as f:
            f.write(content_clean)
            
        # 3. Convert clean text directly into Word Document
        out_docx = os.path.join(OUTPUT_FOLDER, file.filename + "_converted.docx")
        subprocess.run(["pandoc", md_file_path, "-o", out_docx])
        return send_file(out_docx, as_attachment=True)
        
    return 'Failed to extract text. File might be purely blank.', 500

if __name__ == '__main__':
    app.run(port=5000, debug=True)

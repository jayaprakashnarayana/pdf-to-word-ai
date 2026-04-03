import fitz  # PyMuPDF
import os
from ocrmac import ocrmac

def extract_with_apple_vision(pdf_path, txt_path):
    print(f"Connecting to Apple Vision AI to deeply scan '{pdf_path}'...")
    if not os.path.exists(pdf_path):
        print("Error: Document not found.")
        return

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    
    with open(txt_path, "w", encoding="utf-8") as f:
        for page_num in range(total_pages):
            page = doc.load_page(page_num)
            print(f"Scanning Page {page_num + 1}/{total_pages} through Apple Vision...")
            
            # Render the scanned page into a high-res image (300 DPI for best AI recognition)
            pix = page.get_pixmap(dpi=300)
            img_path = f"/tmp/vision_temp_page.png"
            pix.save(img_path)
            
            # Run Apple's incredibly powerful native Vision framework!
            # The recognize() function returns a list of tuples: (text, confidence, bounding_box)
            annotations = ocrmac.OCR(img_path).recognize()
            
            # Combine all the identified text blocks. 
            # The Vision framework automatically sorts them in reading order top-down!
            page_text = "\n".join([ann[0] for ann in annotations if ann[0].strip()])
            
            f.write(f"--- Page {page_num + 1} ---\n")
            if page_text:
                f.write(page_text)
            else:
                f.write("[Blank Page]")
            f.write("\n\n")
            
            # Cleanup temp file
            if os.path.exists(img_path):
                os.remove(img_path)
                
    print(f"\nExtraction flawlessly complete! Saved clean text to '{txt_path}'.")

if __name__ == "__main__":
    pdf_file = "yourlife.pdf"
    txt_file = "yourlife_apple_vision.txt"
    extract_with_apple_vision(pdf_file, txt_file)

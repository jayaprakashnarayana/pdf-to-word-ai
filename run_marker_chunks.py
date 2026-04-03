import fitz
import math
import subprocess
import os

def chunk_and_run_marker(pdf_path, chunk_size=30):
    print(f"Preparing to chunk {pdf_path} into {chunk_size}-page segments to avoid GPU memory overflow...")
    
    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    chunks = math.ceil(total_pages / chunk_size)
    
    for i in range(chunks):
        start_page = i * chunk_size
        end_page = min((i + 1) * chunk_size, total_pages) - 1
        
        chunk_name = f"yourlife_chunk_{i+1}_pages_{start_page+1}_to_{end_page+1}.pdf"
        
        # We skip chunk 1 if we've already done pages 1-30, but actually let's just do them all
        # so everything goes into marker_global_output smoothly.
        doc_chunk = fitz.open()
        doc_chunk.insert_pdf(doc, from_page=start_page, to_page=end_page)
        doc_chunk.save(chunk_name)
        doc_chunk.close()
        
        print(f"\n--- Running GPU Extraction on Chunk {i+1}/{chunks}: {chunk_name} ---")
        out_target = f"./marker_global_output/chunk_{i+1}"
        cmd = f"export TORCH_DEVICE=mps && export PYTORCH_ENABLE_MPS_FALLBACK=1 && source .venv/bin/activate && marker_single {chunk_name} --output_dir {out_target}"
        
        # We run it synchronously in the script so they don't overlap and crash the GPU
        try:
            subprocess.run(cmd, shell=True, check=True)
            print(f"Chunk {i+1} completed successfully!")
            os.remove(chunk_name)  # Clean up the temp pdf chunk
        except Exception as e:
            print(f"Failed on Chunk {i+1}: {e}")
            
if __name__ == "__main__":
    # Prevent creating nested directories if the output dir already exists
    os.makedirs("./marker_global_output", exist_ok=True)
    chunk_and_run_marker("yourlife.pdf", 30)

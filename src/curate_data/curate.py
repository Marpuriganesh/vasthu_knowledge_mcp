import os
from src.curate_data.pdf_utills import PDFManager,get_batch_data,get_page_data,get_pdf_info
from .read_config import config



def get_pdfs(pdf_dir:str)->list[str]:
    pdfs=[]
    for files in os.listdir(pdf_dir):
        full_path = os.path.join(pdf_dir, files)
        if not os.path.isdir(full_path):
            basename = os.path.basename(files)
            if basename.endswith(".pdf"):
                pdfs.append(basename)
    return pdfs

def get_pages_list(page_count: int, step: int) -> list[tuple[int, int]]:
    if step > page_count:
        raise ValueError("Step can't be greater than page_count")

    pages_list = []

    # Loop from 0 up to page_count, leaping by the step size
    for start in range(0, page_count, step):
        # Calculate the end index, making sure we don't overshoot page_count - 1
        end = min(start + step - 1, page_count - 1)
        pages_list.append((start, end))

    return pages_list


def curate_main():
    
    BOOKS_DIR = config["books_path"]
    MCP_SERVER_DIR = config["vasthu_mcp_tools_path"]
    pdf_manager = PDFManager(BOOKS_DIR)
    pdfs = get_pdfs(BOOKS_DIR)
    for pdf in pdfs:
        r_pdf = pdf_manager.open_document(pdf)
        pdf_info = get_pdf_info(r_pdf)
        pages_list = get_pages_list(pdf_info.get("page_count",0),5)
        pages_blocks = []
        for i, (start_page,end_page) in enumerate(pages_list):
            pages_blocks.append(get_batch_data(r_pdf,start_page,end_page))
        print(f"pages blocks: {len(pages_blocks)}")
            
        
        

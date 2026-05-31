import re
import fitz


def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def get_pdf_info(pdf:fitz.Document):


    metadata = pdf.metadata or {}
    return {
        "document_name": pdf._name,
        "page_count": len(pdf),
        "metadata": {
            "title": metadata.get("title", "not available"),
            "author": metadata.get("author", "not available"),
            "subject": metadata.get("subject", "not available"),
            "creator": metadata.get("creator", "not available"),
            "producer": metadata.get("producer", "not available"),
            "creationDate": metadata.get("creationDate", "not available"),
        },
    }

def get_page_data(pdf: fitz.Document, page_no: int) -> dict:
    """Extracts clean blocks from a specific page."""
    if page_no >= len(pdf):
        raise ValueError(
            f"Page {page_no} out of bounds for document with {len(pdf)} pages."
        )

    page = pdf[page_no]
    blocks = page.get_text("blocks")

    extracted_blocks = []
    for i, block in enumerate(blocks):
        x0, y0, x1, y1, text, block_no, block_type = block
        extracted_blocks.append(
            {
                "id": i,
                "type": block_type,
                "bbox": [x0, y0, x1, y1],
                "text": clean_text(text),
            }
        )

    return {"page_no": page_no, "blocks": extracted_blocks}


def get_batch_data(pdf: fitz.Document, start_page: int, end_page: int) -> list:
    """Returns a list of page data dictionaries for the agent to process."""
    batch = []
    if start_page>end_page:
        raise Exception("Start_page can't be greater than end page")
    
    for p_no in range(start_page, end_page + 1):
        batch.append(get_page_data(pdf, p_no))
    return batch

from pathlib import Path
import fitz


class PDFManager:
    def __init__(self, books_dir: str):
        self.books_dir = Path(books_dir)

        self.loaded_pdfs: dict[str, fitz.Document] = {}

    def open_document(self, document_name: str) -> fitz.Document:

        if document_name in self.loaded_pdfs:
            return self.loaded_pdfs[document_name]

        document_path = self.books_dir / document_name

        pdf = fitz.open(document_path)

        self.loaded_pdfs[document_name] = pdf

        return pdf

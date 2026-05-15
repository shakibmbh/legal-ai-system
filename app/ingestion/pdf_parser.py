
import fitz

def extract_text_from_pdf(pdf_path):

    document = fitz.open(pdf_path)

    extracted_pages = []

    for page_number, page in enumerate(document):

        text = page.get_text()

        extracted_pages.append({
            "page": page_number + 1,
            "text": text
        })

    return extracted_pages

import sys
from ebooklib import epub
from bs4 import BeautifulSoup
from fpdf import FPDF

def extract_text_from_epub(epub_path):
    """
    Extracts and returns the combined text content from all HTML documents
    in the given EPUB file.
    """
    book = epub.read_epub(epub_path)
    texts = []
    # Iterate over each document in the EPUB
    for item in book.get_items_of_type(epub.ITEM_DOCUMENT):
        # Get the content and parse it with BeautifulSoup
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        
        # Remove script and style elements
        for element in soup(['script', 'style']):
            element.decompose()
        
        # Get the text and clean up extra whitespace
        text = soup.get_text(separator='\n')
        texts.append(text.strip())
        
    # Combine content from all chapters/sections
    combined_text = "\n\n".join(texts)
    return combined_text

def create_pdf_from_text(text, pdf_path):
    """
    Creates a PDF file at pdf_path containing the given text.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add the text to the PDF with automatic line breaks.
    pdf.multi_cell(0, 10, text)
    pdf.output(pdf_path)

def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py input.epub output.pdf")
        sys.exit(1)
    
    epub_path = sys.argv[1]
    pdf_path = sys.argv[2]
    
    try:
        print(f"Reading EPUB file: {epub_path}")
        text = extract_text_from_epub(epub_path)
        print("EPUB read successfully. Creating PDF...")
        create_pdf_from_text(text, pdf_path)
        print(f"PDF created successfully: {pdf_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 
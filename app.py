import os
import sys
import tempfile
from io import BytesIO

from flask import Flask, request, render_template, send_file, redirect, flash
from ebooklib import epub
from bs4 import BeautifulSoup
from fpdf import FPDF

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

def extract_text_from_epub_file(epub_file_path):
    """
    Extracts and returns the combined text content from all HTML documents in the given EPUB file.
    """
    book = epub.read_epub(epub_file_path)
    texts = []
    # Iterate over each document in the EPUB
    for item in book.get_items_of_type(epub.ITEM_DOCUMENT):
        # Get the content and parse with BeautifulSoup
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

def create_pdf_from_text_buffer(text):
    """
    Creates a PDF in memory from the provided text and returns it as bytes.
    """
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add the text to the PDF with automatic line breaks.
    pdf.multi_cell(0, 10, text)
    # Get PDF as a string, then encode to bytes
    pdf_bytes = pdf.output(dest='S').encode('latin1')
    return pdf_bytes

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'epub_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['epub_file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            # Save uploaded file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, suffix=".epub") as temp_epub:
                file.save(temp_epub.name)
                temp_epub_path = temp_epub.name
            try:
                text = extract_text_from_epub_file(temp_epub_path)
                pdf_bytes = create_pdf_from_text_buffer(text)
                pdf_io = BytesIO(pdf_bytes)
                pdf_io.seek(0)
                return send_file(
                    pdf_io,
                    mimetype='application/pdf',
                    as_attachment=True,
                    download_name='output.pdf'
                )
            except Exception as e:
                flash(f"Conversion failed: {e}")
                return redirect(request.url)
            finally:
                os.remove(temp_epub_path)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True) 
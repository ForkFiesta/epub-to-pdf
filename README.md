# EPUB to PDF Converter

This is a simple Python application that converts EPUB documents to PDF files.

## Overview

The application reads an EPUB file, extracts its text content (ignoring most HTML formatting), and writes the text out to a PDF using the [FPDF](https://pyfpdf.github.io/fpdf2/) library. This solution is ideal for basic conversions where preserving complex formatting is not required.

## Dependencies

Make sure you have [Python 3](https://www.python.org/) installed. The following Python packages are required:

- [EbookLib](https://github.com/aerkalov/ebooklib)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/)
- [FPDF2](https://pyfpdf.github.io/fpdf2/)

You can install the dependencies via pip:

## Usage

Run the application from the command line by providing the input EPUB file and the desired output PDF file path. For example:

```bash
python main.py input.epub output.pdf
```

If the correct arguments are not provided, the application will display a usage message.

## Project Structure

```
├── README.md
├── requirements.txt
└── main.py
```

## Contributing

Feel free to fork the repository and submit pull requests. Any improvements to error handling, formatting, or additional features (like preserving formatting, table of contents, etc.) are welcome.

## License

This project is released under the MIT License.
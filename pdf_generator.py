from markdown2pdf.core import md_to_pdf

def generate_pdf(markdown_file, pdf_file):
    md_to_pdf(markdown_file, pdf_file)
    print(f"Summary converted to {pdf_file}")


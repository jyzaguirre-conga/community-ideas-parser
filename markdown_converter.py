from markdown_pdf import MarkdownPdf, Section

def convert_markdown_to_pdf(markdown_file, pdf_file):
    with open(markdown_file, 'r') as file:
        markdown_text = file.read()

    pdf = MarkdownPdf()
    section = Section(markdown_text)
    pdf.add_section(section)
    pdf.save(pdf_file)


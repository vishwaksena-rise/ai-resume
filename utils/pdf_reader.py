import pdfplumber
from docx import Document
import os


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from PDF, DOCX and DOC files.
    """

    filename = uploaded_file.name.lower()
    extension = os.path.splitext(filename)[1]

    text = ""

    try:

        # -----------------------------
        # PDF
        # -----------------------------
        if extension == ".pdf":

            with pdfplumber.open(uploaded_file) as pdf:

                for page in pdf.pages:

                    page_text = page.extract_text()

                    if page_text:
                        text += page_text + "\n"

        # -----------------------------
        # DOCX
        # -----------------------------
        elif extension == ".docx":

            document = Document(uploaded_file)

            for paragraph in document.paragraphs:
                text += paragraph.text + "\n"

        # -----------------------------
        # DOC
        # -----------------------------
        elif extension == ".doc":

            text = (
                "Old Microsoft Word (.doc) files are currently not supported.\n"
                "Please save the document as .docx or PDF and upload again."
            )

        # -----------------------------
        # Unsupported File
        # -----------------------------
        else:

            text = "Unsupported file format."

    except Exception as e:

        text = f"Error reading file: {str(e)}"

    return text
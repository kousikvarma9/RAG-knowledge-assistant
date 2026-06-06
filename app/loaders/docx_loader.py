from docx import Document

class DOCXLoader:

    def load(self, file_path: str) -> str:

        doc = Document(file_path)

        text = ""

        for para in doc.paragraphs:
            text += para.text + "\n"

        return text
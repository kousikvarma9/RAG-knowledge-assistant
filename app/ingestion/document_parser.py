from docling.document_converter import DocumentConverter


class DocumentParser:

    def __init__(self):
        self.converter = DocumentConverter()

    def parse(self, file_path):

        result = self.converter.convert(file_path)

        return result.document.export_to_markdown()
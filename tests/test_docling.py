from app.ingestion.document_parser import DocumentParser

parser = DocumentParser()

content = parser.parse(
    r"data/uploads/Mahindra-XUV-700-2026-NZ.pdf"
)

print(content[:3000])
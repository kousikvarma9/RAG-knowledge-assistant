from app.vision.image_extractor import ImageExtractor

extractor = ImageExtractor()

images = extractor.extract_images(
    "data/uploads/Mahindra-XUV-700-2026-NZ.pdf",
    "data/extracted_images"
)

print(
    f"Images Extracted: {len(images)}"
)

for image in images[:10]:

    print(image)
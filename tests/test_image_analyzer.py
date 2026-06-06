from app.vision.image_analyzer import ImageAnalyzer

analyzer = ImageAnalyzer()

description = analyzer.describe_image(
    "data/extracted_images/page_1_img_1.jpeg"
)

print(description)
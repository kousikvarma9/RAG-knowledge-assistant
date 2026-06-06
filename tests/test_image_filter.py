from app.vision.image_filter import ImageFilter
import os

filterer = ImageFilter()

folder = "data/extracted_images"

useful = []

for file in os.listdir(folder):

    path = os.path.join(
        folder,
        file
    )

    if filterer.is_useful_image(path):

        useful.append(path)

print("Useful Images:", len(useful))

for image in useful[:10]:
    print(image)
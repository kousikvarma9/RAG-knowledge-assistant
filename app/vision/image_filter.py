from PIL import Image


class ImageFilter:

    def is_useful_image(
        self,
        image_path
    ):

        image = Image.open(
            image_path
        )

        width, height = image.size

        if width < 300 or height < 300:
            return False

        return True
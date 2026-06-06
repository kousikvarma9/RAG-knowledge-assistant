import fitz
import os


class ImageExtractor:

    def extract_images(
        self,
        pdf_path,
        output_folder
    ):

        os.makedirs(
            output_folder,
            exist_ok=True
        )

        pdf = fitz.open(pdf_path)

        image_paths = []

        for page_index in range(len(pdf)):

            page = pdf[page_index]

            images = page.get_images(
                full=True
            )

            for image_index, img in enumerate(images):

                xref = img[0]

                base_image = pdf.extract_image(
                    xref
                )

                image_bytes = base_image["image"]

                extension = base_image["ext"]

                image_name = (
                    f"page_{page_index+1}_"
                    f"img_{image_index+1}."
                    f"{extension}"
                )

                image_path = os.path.join(
                    output_folder,
                    image_name
                )

                with open(
                    image_path,
                    "wb"
                ) as file:

                    file.write(
                        image_bytes
                    )

                image_paths.append(
                    image_path
                )

        return image_paths
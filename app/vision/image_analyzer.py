import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image


class ImageAnalyzer:

    def __init__(self):

        load_dotenv()

        genai.configure(
            api_key=os.getenv("GOOGLE_API_KEY")
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    def describe_image(
        self,
        image_path
    ):

        image = Image.open(
            image_path
        )

        response = self.model.generate_content(
    [
        """
Describe this image for retrieval.

Rules:
- Maximum 100 words
- Mention important objects
- Mention colors
- Mention labels if important
- Mention vehicles, people, animals, diagrams, charts
- Ignore decorative logos
- Return factual observations only
        """,
        image
    ]
)

        return response.text
import os
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image

load_dotenv()

genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

image = Image.open(
    "data/extracted_images/page_1_img_1.jpeg"
)

response = model.generate_content(
    [
        "Describe this image in detail.",
        image
    ]
)

print(response.text)
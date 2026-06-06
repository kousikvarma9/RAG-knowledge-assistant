import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


genai.configure(
    api_key=os.getenv("GOOGLE_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


class RAGPipeline:

    def generate_answer(
        self,
        question,
        context
    ):

        prompt = f"""
You are a RAG assistant.

Rules:
1. Answer only from the provided context.
2. If the answer is not present in the context, say:
   "The answer is not available in the provided documents."
3. Do not use outside knowledge.

Context:
{context}

Question:
{question}
"""

        response = model.generate_content(
            prompt
        )


        return response.text
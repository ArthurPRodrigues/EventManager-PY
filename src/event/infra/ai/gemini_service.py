import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class GeminiService:
    def __init__(self):
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key == "YOUR_API_KEY_HERE":
            raise ValueError("The GEMINI_API_KEY environment variable is not defined.")

        genai.configure(api_key=api_key)
        self._model = genai.GenerativeModel("gemini-flash-latest")

    def generate_event_description(
        self, event_name: str, event_type: str, event_keywords: str
    ) -> str:
        prompt = f"""
        First, identify the language of the following event details: '{event_name}', '{event_type}', '{event_keywords}'.
        Then, in the identified language, create an eye-catching and fun event description.
        The description should have at most 3 paragraphs, be optimistic and inviting.
        Use an informal and creative tone.
        The description must have a maximum of 150 characters.
        Respond only with the generated description.
        """

        try:
            response = self._model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"Error calling the Gemini API: {e}")
            return f"An error occurred while generating the description: {e!s}"

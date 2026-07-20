from google import genai
from config.settings import (
    GEMINI_API_KEY,
    MAX_RETRIES
)
import time



class GeminiService:

    def __init__(self):

        self.client = genai.Client(
            api_key=GEMINI_API_KEY
        )

        self.models = [
            "gemini-3.1-flash-lite",
            "gemini-2.5-flash-lite",
            "gemini-2.5-flash",
            "gemini-3.5-flash"
        ]

    def generate(self, prompt):

        for model in self.models:

            try:

                print(
                    f"Trying {model}..."
                )

                response = (
                    self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )
                )

                print(
                    f"Success using {model}"
                )

                return response.text

            except Exception as e:

                print(
                    f"{model} failed:"
                )

                print(e)

                time.sleep(2)
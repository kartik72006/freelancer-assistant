from google import genai
from config.settings import (
    GEMINI_API_KEY
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

                response = (
                    self.client.models.generate_content(
                        model=model,
                        contents=prompt
                    )
                )


                return response.text

            except Exception as e:

                print(e)

                time.sleep(2)
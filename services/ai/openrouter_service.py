from openai import OpenAI
from config.settings import (
    OPENROUTER_API_KEY,
    OPENROUTER_BASE_URL,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TEMPERATURE,
    MAX_RETRIES
)
import time



class OpenRouterService:

    def __init__(self):

        self.client = OpenAI(

            api_key=OPENROUTER_API_KEY,

            base_url=OPENROUTER_BASE_URL

        )

        self.models = (

            # Primary Model
            "tencent/hy3:free",

            # Fallback 1
            "nvidia/nemotron-3-ultra-550b-a55b:free",

            # Fallback 2
            "poolside/laguna-m.1:free"

        )

    def generate(self, prompt):

        for model in self.models:

            try:

                start = time.time()

                response = self.client.chat.completions.create(

                    model=model,

                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],

                    temperature=DEFAULT_TEMPERATURE,
                    timeout=120  # important
                )

                end = time.time()

                return response.choices[0].message.content

            except Exception as e:

                print(e)

                time.sleep(2)

                raise RuntimeError(
                    f"Gemini generation failed using {model}"
                ) from e
import json
import re


def parse_json(text):

    if not text:
        return None

    try:

        # Remove markdown code fences
        text = re.sub(
            r"```(?:json)?",
            "",
            text,
            flags=re.IGNORECASE
        ).strip()

        # Extract only the JSON object
        start = text.find("{")
        end = text.rfind("}")

        if start != -1 and end != -1:
            text = text[start:end + 1]

        return json.loads(text)

    except json.JSONDecodeError as e:

        print(f"JSON Decode Error: {e}")

        return None

    except Exception as e:

        print(f"Unexpected JSON Parse Error: {e}")

        return None
import re


class ResultParser:

    @staticmethod
    def parse(file_path):

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            content = file.read()

        sections = {}

        headers = [
            "ORIGINAL JOB DESCRIPTION",
            "ANALYSIS",
            "PROPOSAL",
            "PRICING",
            "REVIEW"
        ]

        for i, header in enumerate(headers):

            start = content.find(header)

            if start == -1:
                sections[header] = None
                continue

            start = content.find("\n", start)
            start = content.find("\n", start + 1)

            if i < len(headers) - 1:

                end = content.find(
                    headers[i + 1]
                )

            else:

                end = len(content)

            section = content[start:end].strip()

            sections[header] = section

        return {

            "job_description":
                sections["ORIGINAL JOB DESCRIPTION"],

            "analysis":
                sections["ANALYSIS"],

            "proposal":
                sections["PROPOSAL"],

            "pricing":
                sections["PRICING"],

            "review":
                sections["REVIEW"]

        }
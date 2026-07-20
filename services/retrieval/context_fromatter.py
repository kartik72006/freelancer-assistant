class ContextFormatter:

    @staticmethod
    def format(results):

        if not results:
            return "No relevant projects found."

        formatted_projects = []

        for index, result in enumerate(results, start=1):

            metadata = result["metadata"]
            document = result["document"]

            context = f"""
Relevant Project {index}

Title:
{metadata.get("title", "N/A")}

Role:
{metadata.get("role", "N/A")}

Domain:
{metadata.get("domain", "N/A")}

Project Type:
{metadata.get("project_type", "N/A")}

Project Details:
{document}

Similarity Score:
{result["score"]:.4f}

------------------------------------------------------------
"""

            formatted_projects.append(context.strip())

        return "\n\n".join(formatted_projects)
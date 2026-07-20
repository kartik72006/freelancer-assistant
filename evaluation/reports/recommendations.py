class RecommendationEngine:

    def __init__(self, statistics, feedback):

        self.statistics = statistics

        self.feedback = feedback

        self.metric_recommendations = {

            "relevance": [

                "Improve requirement extraction before proposal generation.",
                "Strengthen skill matching with the job description.",
                "Use semantic retrieval instead of keyword matching."

            ],

            "accuracy": [

                "Avoid unsupported technical or business claims.",
                "Use only verified portfolio information from the knowledge base.",
                "Cross-check project details before including them in proposals."

            ],

            "personalization": [

                "Reference the client's industry or business domain.",
                "Mention client-specific pain points.",
                "Avoid generic proposal introductions.",
                "Explain why your previous projects are relevant to this client.",
                "Tailor milestones specifically to the client's requirements."

            ],

            "completeness": [

                "Include clearer deliverables.",
                "Provide more detailed milestones.",
                "Improve project planning and payment breakdown."

            ],

            "tone": [

                "Reduce overly promotional language.",
                "Maintain a professional but conversational tone.",
                "Improve readability by shortening long paragraphs."

            ],

            "hallucination": [

                "Remove unsupported experience claims.",
                "Avoid fabricated metrics or achievements.",
                "Generate proposals strictly from the knowledge base."

            ]

        }

    def metric_based(self):

        recommendations = []

        averages = self.statistics["average_metrics"]

        for metric, score in averages.items():

            if score >= 8:

                continue

            recommendations.extend(

                self.metric_recommendations.get(

                    metric,

                    []

                )

            )

        return recommendations

    def keyword_based(self):

        recommendations = []

        keywords = self.feedback["keywords"]

        keyword_map = {

            "generic":

                "Increase proposal personalization and reduce template-like writing.",

            "client":

                "Reference the client's business and objectives more explicitly.",

            "specific":

                "Include more job-specific technical details.",

            "industry":

                "Mention the client's industry whenever possible.",

            "claims":

                "Avoid unsupported claims about experience or results.",

            "experience":

                "Use only verified experience from the knowledge base.",

            "timeline":

                "Generate timelines dynamically based on project complexity.",

            "business":

                "Focus more on business outcomes instead of only technologies."

        }

        for word, frequency in keywords:

            if frequency < 2:

                continue

            if word in keyword_map:

                recommendations.append(

                    keyword_map[word]

                )

        return recommendations

    def remove_duplicates(self, recommendations):

        unique = []

        seen = set()

        for recommendation in recommendations:

            if recommendation not in seen:

                unique.append(recommendation)

                seen.add(recommendation)

        return unique

    def prioritize(self, recommendations):

        high_priority = []

        medium_priority = []

        low_priority = []

        averages = self.statistics["average_metrics"]

        weakest_metric = min(

            averages,

            key=averages.get

        )

        for recommendation in recommendations:

            if weakest_metric == "personalization":

                if any(

                    word in recommendation.lower()

                    for word in [

                        "client",

                        "generic",

                        "industry",

                        "pain"

                    ]

                ):

                    high_priority.append(recommendation)

                    continue

            if weakest_metric == "accuracy":

                if any(

                    word in recommendation.lower()

                    for word in [

                        "verified",

                        "claims",

                        "knowledge"

                    ]

                ):

                    high_priority.append(recommendation)

                    continue

            medium_priority.append(recommendation)

        return {

            "high": high_priority,

            "medium": medium_priority,

            "low": low_priority

        }

    def summary(self):

        metric = self.metric_based()

        keyword = self.keyword_based()

        recommendations = metric + keyword

        recommendations = self.remove_duplicates(

            recommendations

        )

        recommendations = self.prioritize(

            recommendations

        )

        return recommendations
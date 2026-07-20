class ProposalScorer:

    MAX_SCORES = {
        "relevance": 10,
        "accuracy": 10,
        "personalization": 10,
        "completeness": 10,
        "tone": 10,
        "hallucination": 10
    }

    @staticmethod
    def calculate_total(scores):

        return sum(scores.values())

    @staticmethod
    def validate(scores):

        for criterion, max_score in ProposalScorer.MAX_SCORES.items():

            if criterion not in scores:
                raise ValueError(
                    f"Missing score for {criterion}"
                )

            score = scores[criterion]

            if score < 0 or score > max_score:

                raise ValueError(
                    f"{criterion} must be between 0 and {max_score}"
                )

        return True
class RecommendationEngine:
    """
    Generates recommendations based on experiment results.
    """

    def generate(
        self,
        winner: str,
        improvement_percentage: float,
    ):

        if winner == "Tie":
            return "No significant difference. Keep current strategy."

        if improvement_percentage >= 10:
            return (
                "Strong improvement detected. "
                "Recommend deploying the winning strategy."
            )

        if improvement_percentage >= 3:
            return (
                "Moderate improvement detected. "
                "Consider further validation."
            )

        return (
            "Improvement is marginal. "
            "Continue experimenting before deployment."
        )
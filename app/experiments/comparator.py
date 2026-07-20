from .experiment_results import StrategyMetrics


class ExperimentComparator:
    """
    Compares two experiment strategies.
    """

    def compare(
        self,
        metrics_a: StrategyMetrics,
        metrics_b: StrategyMetrics,
    ):
        """
        Returns:
            winner,
            improvement_percentage
        """

        score_a = metrics_a.overall_score
        score_b = metrics_b.overall_score

        if score_a == score_b:
            return "Tie", 0.0

        if score_a > score_b:
            improvement = (
                (score_a - score_b)
                / score_b
            ) * 100 if score_b else 0

            return "Strategy A", improvement

        improvement = (
            (score_b - score_a)
            / score_a
        ) * 100 if score_a else 0

        return "Strategy B", improvement
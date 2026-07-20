from .experiment_results import StrategyMetrics


class MetricsCalculator:

    def calculate(self, results):

        if not results:
            return StrategyMetrics()

        total_score = 0
        total_professionalism = 0
        total_personalization = 0
        total_clarity = 0
        total_tone = 0
        total_latency = 0

        for result in results:

            review = result.review

            total_score += review["overallScore"]

            total_professionalism += review["metrics"]["professionalism"]

            total_personalization += review["metrics"]["personalization"]

            total_clarity += review["metrics"]["clarity"]

            total_tone += review["metrics"]["tone"]

            total_latency += result.generation_time

        n = len(results)

        return StrategyMetrics(
            overall_score=total_score / n,
            professionalism=total_professionalism / n,
            personalization=total_personalization / n,
            clarity=total_clarity / n,
            tone=total_tone / n,
            latency=total_latency / n,
        )
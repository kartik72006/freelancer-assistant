from app.experiments.experiment_results import ExperimentResult


class ExperimentReport:

    def generate(
        self,
        result: ExperimentResult,
    ) -> str:
        """
        Generates a human-readable experiment report.
        """

        report = f"""
============================================================
                    Experiment Report
============================================================

Experiment
----------
{result.experiment_name}

Winner
------
{result.winner}

Improvement
-----------
{result.improvement_percentage:.2f}%

Recommendation
--------------
{result.recommendation}

============================================================
Strategy A : {result.strategy_a.name}
============================================================

Overall Score      : {result.strategy_a.metrics.overall_score:.2f}
Professionalism    : {result.strategy_a.metrics.professionalism:.2f}
Personalization    : {result.strategy_a.metrics.personalization:.2f}
Clarity            : {result.strategy_a.metrics.clarity:.2f}
Tone               : {result.strategy_a.metrics.tone:.2f}
Latency            : {result.strategy_a.metrics.latency:.2f} sec

============================================================
Strategy B : {result.strategy_b.name}
============================================================

Overall Score      : {result.strategy_b.metrics.overall_score:.2f}
Professionalism    : {result.strategy_b.metrics.professionalism:.2f}
Personalization    : {result.strategy_b.metrics.personalization:.2f}
Clarity            : {result.strategy_b.metrics.clarity:.2f}
Tone               : {result.strategy_b.metrics.tone:.2f}
Latency            : {result.strategy_b.metrics.latency:.2f} sec
"""

        return report
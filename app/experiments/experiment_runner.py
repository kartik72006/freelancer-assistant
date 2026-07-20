
from .comparator import ExperimentComparator
from .recommendations import RecommendationEngine
from .metrics import MetricsCalculator
from .experiment_strategy import ExperimentStrategy
from .experiment_results import (
    ExperimentResult,
    ExperimentSample,
    StrategyResult,
    StrategyMetrics,
)

class ExperimentRunner:

    def __init__(self):

        self.metrics_calculator = MetricsCalculator()

        self.comparator = ExperimentComparator()

        self.recommendation_engine = RecommendationEngine()


    def run(
        self,
        strategy_a:ExperimentStrategy,
        strategy_b:ExperimentStrategy,
        benchmark_jobs:list[dict],
    ) -> ExperimentResult:
        """
        Executes two strategies and compares them.
        """

        strategy_a_results = self._run_strategy(
            strategy_a,
            benchmark_jobs,
        )

        strategy_b_results = self._run_strategy(
            strategy_b,
            benchmark_jobs,
        )

        metrics_a = self.metrics_calculator.calculate(
            strategy_a_results
        )

        metrics_b = self.metrics_calculator.calculate(
            strategy_b_results
        )

        return self._build_result(
            strategy_a,
            strategy_b,
            strategy_a_results,
            strategy_b_results,
            metrics_a,
            metrics_b,
        )
    
    def _run_strategy(
    self,
    strategy: ExperimentStrategy,
    benchmark_jobs: list[dict],
) -> list[ExperimentSample]:
        """
        Executes one strategy on all benchmark jobs.
        """

        results = []

        for job in benchmark_jobs:
            result = strategy.execute(job)
            results.append(result)

        return results


    def _build_result(
        self,
        strategy_a,
        strategy_b,
        strategy_a_results: list[ExperimentSample],
        strategy_b_results: list[ExperimentSample],
        metrics_a: StrategyMetrics,
        metrics_b: StrategyMetrics,
        ):

        winner, improvement = self.comparator.compare(
            metrics_a,
            metrics_b,
        )

        recommendation = self.recommendation_engine.generate(
            winner,
            improvement,
        )
        return ExperimentResult(
            experiment_name=f"{strategy_a.name} vs {strategy_b.name}",
            strategy_a=StrategyResult(
                name=strategy_a.name,
                metrics=metrics_a,
                samples=strategy_a_results,
            ),
            strategy_b=StrategyResult(
                name=strategy_b.name,
                metrics=metrics_b,
                samples=strategy_b_results,
            ),
            winner=winner,
            improvement_percentage=improvement,
            recommendation=recommendation,
        )
    

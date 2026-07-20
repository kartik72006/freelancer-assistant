from evaluation.benchmark_loader import BenchmarkLoader

from app.experiments.experiment_runner import ExperimentRunner
from evaluation.reports.experiment_report import ExperimentReport

from app.experiments.strategies.prompt_v1_strategy import PromptV1Strategy
from app.experiments.strategies.prompt_v2_strategy import PromptV2Strategy
from api.dependencies import (
    proposal_service,
    review_agent,
)
from evaluation.exporters.json_exporter import JSONExporter

loader = BenchmarkLoader()

jobs = loader.load()

print(f"Loaded {len(jobs)} benchmark jobs.")

strategy_v1 = PromptV1Strategy(
    proposal_service,
    review_agent,
)

strategy_v2 = PromptV2Strategy(
    proposal_service,
    review_agent,
)

runner = ExperimentRunner()

result = runner.run(
    strategy_v1,
    strategy_v2,
    jobs,
)

report_generator = ExperimentReport()

report = report_generator.generate(result)

print(report)

exporter=JSONExporter()

exporter.export(
    result=result,
    output_path="evaluation/results/prompt_v1_vs_v2.json",
)

print("Experiment completed.")
print("Results saved to evaluation/results/prompt_v1_vs_v2.json")
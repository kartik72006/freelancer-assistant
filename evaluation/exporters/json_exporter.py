import json
from dataclasses import asdict
from pathlib import Path

from app.experiments.experiment_results import ExperimentResult


class JSONExporter:

    def export(
        self,
        result: ExperimentResult,
        output_path: str,
    ) -> None:
        """
        Saves an ExperimentResult as JSON.
        """

        Path(output_path).parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(
                asdict(result),
                file,
                indent=4,
                ensure_ascii=False,
            )
from pathlib import Path


class BenchmarkLoader:

    def __init__(
        self,
        jobs_directory: str = "evaluation/jobs",
    ):
        self.jobs_directory = Path(jobs_directory)

    def load(self):
        """
        Loads every benchmark job from evaluation/jobs.
        """

        benchmark_jobs = []

        job_files = sorted(
            self.jobs_directory.glob("*.txt")
        )

        for job_file in job_files:

            benchmark_jobs.append(
                {
                    "id": job_file.stem,
                    "description": job_file.read_text(
                        encoding="utf-8"
                    ),
                }
            )

        return benchmark_jobs
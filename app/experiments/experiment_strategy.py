from abc import ABC, abstractmethod

from .experiment_results import ExperimentSample


class ExperimentStrategy(ABC):

    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def execute(
        self,
        benchmark_job,
    ) -> ExperimentSample:
        ...
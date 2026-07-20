from evaluation.benchmark_loader import BenchmarkLoader


loader = BenchmarkLoader()

jobs = loader.load()

print(f"Loaded {len(jobs)} benchmark jobs.")
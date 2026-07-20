import os
import pandas as pd

from statistics import Statistics
from feedback_analyzer import FeedbackAnalyzer
from recommendations import RecommendationEngine
from visualization import Visualization
from markdown_writer import MarkdownWriter


BASE_DIR = os.path.dirname(__file__)

CSV_PATH = os.path.join(
    BASE_DIR,
    "..",
    "scores.csv"
)

REPORT_PATH = os.path.join(
    BASE_DIR,
    "..",
    "evaluation_report.md"
)


def main():

    print("=" * 60)
    print("Generating Evaluation Report...")
    print("=" * 60)

    # -------------------------
    # Load Scores
    # -------------------------

    df = pd.read_csv(CSV_PATH)

    # -------------------------
    # Statistics
    # -------------------------

    statistics_engine = Statistics(df)

    statistics = statistics_engine.summary()

    # -------------------------
    # Feedback Analysis
    # -------------------------

    feedback_engine = FeedbackAnalyzer(df)

    feedback = feedback_engine.summary()

    # -------------------------
    # Recommendations
    # -------------------------

    recommendation_engine = RecommendationEngine(

        statistics,

        feedback

    )

    recommendations = recommendation_engine.summary()

    # -------------------------
    # Visualization
    # -------------------------

    visualization_engine = Visualization(

        statistics

    )

    visualization = visualization_engine.generate()

    # -------------------------
    # Markdown Report
    # -------------------------

    markdown_writer = MarkdownWriter(

        statistics,

        feedback,

        recommendations,

        visualization

    )

    report = markdown_writer.generate()

    # -------------------------
    # Save Report
    # -------------------------

    with open(

        REPORT_PATH,

        "w",

        encoding="utf-8"

    ) as file:

        file.write(report)

    print("\nEvaluation report generated successfully!")

    print(f"\nSaved to:\n{REPORT_PATH}")

    print("=" * 60)


if __name__ == "__main__":

    main()
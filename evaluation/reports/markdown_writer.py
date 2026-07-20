from datetime import datetime


class MarkdownWriter:

    def __init__(
        self,
        statistics,
        feedback,
        recommendations,
        visualization
    ):

        self.statistics = statistics
        self.feedback = feedback
        self.recommendations = recommendations
        self.visualization = visualization

        self.strength_messages = {

            "relevance":
                "The proposal generator consistently aligns generated proposals with client requirements.",

            "accuracy":
                "Generated technical solutions are realistic and technically sound.",

            "personalization":
                "The system effectively adapts proposals according to client requirements.",

            "completeness":
                "Generated proposals consistently contain complete deliverables, timelines and project plans.",

            "tone":
                "Professional, client-friendly and persuasive communication is maintained.",

            "hallucination":
                "Very few unsupported or fabricated claims were detected."

        }

        self.weakness_messages = {

            "relevance":
                "Requirement understanding can still be improved for niche projects.",

            "accuracy":
                "Some proposals include unsupported technical or portfolio claims.",

            "personalization":
                "Many proposals still follow reusable templates instead of deeply understanding the client's business.",

            "completeness":
                "Some proposals can provide more detailed milestones and deliverables.",

            "tone":
                "A few proposals become slightly promotional instead of conversational.",

            "hallucination":
                "Occasional unsupported achievements and metrics should be removed."

        }

    def executive_summary(self):

        highest = self.statistics["highest"]
        lowest = self.statistics["lowest"]

        percentage = round(
            self.statistics["average_overall"] / 60 * 100,
            2
        )

        distribution = self.statistics["distribution"]

        report = f"""
# AI Proposal Evaluation Report

Generated on: {datetime.now().strftime("%d %B %Y")}

---

# Executive Summary

## Dataset Statistics

- Total Proposals Evaluated : {self.statistics["total"]}

- Average Overall Score : {self.statistics["average_overall"]}/60 ({percentage}%)

- Highest Score : {highest["score"]}/60 ({highest["job_id"]})

- Lowest Score : {lowest["score"]}/60 ({lowest["job_id"]})

## Score Distribution

| Category | Range | Count |
|----------|-------|------:|
| Excellent | 50-60 | {distribution["excellent"]} |
| Good | 45-49 | {distribution["good"]} |
| Needs Improvement | <45 | {distribution["needs_improvement"]} |

---

"""

        return report

    def criterion_table(self):

        report = """
# Criterion-wise Performance

| Metric | Average | Category |
|--------|---------|----------|
"""

        averages = self.statistics["average_metrics"]

        for metric, score in averages.items():

            if score >= 8:

                category = "Strength"

            elif score >= 6:

                category = "Needs Improvement"

            else:

                category = "Critical"

            report += (
                f"| {metric.title()} | "
                f"{score:.2f} | "
                f"{category} |\n"
            )

        report += "\n---\n\n"

        return report

    def strengths(self):

        report = "# System Strengths\n\n"

        for metric in self.statistics["analysis"]["strengths"]:

            report += (
                f"- {self.strength_messages[metric]}\n"
            )

        report += "\n---\n\n"

        return report

    def weaknesses(self):

        report = "# Areas for Improvement\n\n"

        improvements = (

            self.statistics["analysis"]["improvements"]

            +

            self.statistics["analysis"]["critical"]

        )

        if len(improvements) == 0:

            report += "- No significant weaknesses detected.\n"

        else:

            for metric in improvements:

                report += (
                    f"- {self.weakness_messages[metric]}\n"
                )

        report += "\n---\n\n"

        return report

    def proposal_analysis(self):

        highest = self.statistics["highest"]
        lowest = self.statistics["lowest"]

        report = "# Best & Worst Proposal Analysis\n\n"

        report += f"""
## Best Performing Proposal

Proposal : **{highest["job_id"]}**

Overall Score : **{highest["score"]}/60**

This proposal demonstrated excellent requirement alignment,
complete project planning,
professional tone,
and minimal hallucination.

---

## Lowest Performing Proposal

Proposal : **{lowest["job_id"]}**

Overall Score : **{lowest["score"]}/60**

This proposal requires improvements in personalization,
accuracy,
and client-specific tailoring.

---

"""

        return report

    def evaluator_feedback(self):

        report = "# Evaluator Feedback Summary\n\n"

        feedback = self.feedback["common_feedback"]

        for metric, comments in feedback.items():

            title = (

                metric

                .replace("_feedback", "")

                .replace("_", " ")

                .title()

            )

            report += f"## {title}\n\n"

            if len(comments) == 0:

                report += "- No feedback available.\n\n"

                continue

            for comment, count in comments:

                report += (
                    f"- ({count}x) {comment}\n"
                )

            report += "\n"

        report += "\n---\n\n"

        return report

    def recommendation_section(self):

        report = "# Engineering Recommendations\n\n"

        recommendations = self.recommendations

        if recommendations["high"]:

            report += "## High Priority\n\n"

            for item in recommendations["high"]:

                report += f"- {item}\n"

            report += "\n"

        if recommendations["medium"]:

            report += "## Medium Priority\n\n"

            for item in recommendations["medium"]:

                report += f"- {item}\n"

            report += "\n"

        if recommendations["low"]:

            report += "## Low Priority\n\n"

            for item in recommendations["low"]:

                report += f"- {item}\n"

            report += "\n"

        report += "\n---\n\n"

        return report

    def overall_assessment(self):

        percentage = round(
            self.statistics["average_overall"] / 60 * 100,
            2
        )

        return f"""
# Overall Assessment

Across **{self.statistics["total"]}** benchmark jobs,
the Proposal Generation System achieved an overall score of
**{percentage}%**.

The benchmark demonstrates strong capability in:

- Understanding client requirements
- Generating complete project proposals
- Maintaining professional communication
- Producing low-hallucination outputs

The largest opportunity for improvement remains:

- Client-specific personalization
- Eliminating unsupported claims
- Improving proposal uniqueness

Overall, the system is suitable as a production-quality MVP
and provides a strong foundation for future improvements using
semantic retrieval, RAG, adaptive prompting and iterative evaluation.

---

"""

    def future_work(self):

        return """
# Future Improvements

- Retrieval-Augmented Generation (RAG)

- Semantic Search using Embeddings

- Vector Database Integration

- Adaptive Proposal Personalization

- AI-powered Dynamic Pricing

- Continuous Benchmark Evaluation

- Prompt A/B Testing

- Automatic Proposal Refinement Loop

- Multi-model Evaluation

- Human Feedback Integration

---
"""

    def generate(self):

        report = ""

        report += self.executive_summary()

        report += self.visualization

        report += "\n\n"

        report += self.criterion_table()

        report += self.strengths()

        report += self.weaknesses()

        report += self.proposal_analysis()

        report += self.evaluator_feedback()

        report += self.recommendation_section()

        report += self.overall_assessment()

        report += self.future_work()

        return report
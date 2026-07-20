class Visualization:

    def __init__(self, statistics):

        self.statistics = statistics

    def bar(self, value, maximum, width=30):

        if maximum == 0:
            return ""

        filled = int((value / maximum) * width)

        return "█" * filled + "░" * (width - filled)

    def metric_chart(self):

        averages = self.statistics["average_metrics"]

        chart = []

        chart.append("## Average Metric Scores\n")

        max_score = 10

        for metric, score in averages.items():

            bar = self.bar(score, max_score)

            chart.append(
                f"{metric.title():18} {bar} {score:.2f}/10"
            )

        return "\n".join(chart)

    def score_distribution_chart(self):

        distribution = self.statistics["distribution"]

        excellent = distribution["excellent"]
        good = distribution["good"]
        improvement = distribution["needs_improvement"]

        maximum = max(
            excellent,
            good,
            improvement,
            1
        )

        chart = []

        chart.append("## Overall Score Distribution\n")

        chart.append(
            f"Excellent (50-60)      {self.bar(excellent, maximum, 20)} {excellent}"
        )

        chart.append(
            f"Good (45-49)           {self.bar(good, maximum, 20)} {good}"
        )

        chart.append(
            f"Needs Improvement      {self.bar(improvement, maximum, 20)} {improvement}"
        )

        return "\n".join(chart)

    def benchmark_summary(self):

        overall = self.statistics["average_overall"]

        percentage = round(
            (overall / 60) * 100,
            2
        )

        chart = []

        chart.append("## Overall Benchmark\n")

        chart.append(
            self.bar(
                percentage,
                100,
                40
            )
        )

        chart.append(
            f"{percentage}%"
        )

        return "\n".join(chart)

    def best_vs_worst(self):

        best = self.statistics["highest"]

        worst = self.statistics["lowest"]

        maximum = 60

        chart = []

        chart.append("## Best vs Worst Proposal\n")

        chart.append(
            f"{best['job_id']:18} {self.bar(best['score'], maximum, 25)} {best['score']}/60"
        )

        chart.append(
            f"{worst['job_id']:18} {self.bar(worst['score'], maximum, 25)} {worst['score']}/60"
        )

        return "\n".join(chart)

    def generate(self):

        sections = [

            self.benchmark_summary(),

            "",

            self.metric_chart(),

            "",

            self.score_distribution_chart(),

            "",

            self.best_vs_worst()

        ]

        return "\n".join(sections)
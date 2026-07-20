import pandas as pd


class Statistics:

    def __init__(self, dataframe):

        self.df = dataframe

        self.metrics = [

            "relevance",

            "accuracy",

            "personalization",

            "completeness",

            "tone",

            "hallucination"

        ]

    def classify(self, score):

        if score >= 8:

            return "Strength"

        elif score >= 6:

            return "Needs Improvement"

        else:

            return "Critical"

    def average_scores(self):

        averages = {}

        for metric in self.metrics:

            averages[metric] = round(

                self.df[metric].mean(),

                2

            )

        return averages

    def overall_average(self):

        return round(

            self.df["overall"].mean(),

            2

        )

    def highest_proposal(self):

        row = self.df.loc[

            self.df["overall"].idxmax()

        ]

        return {

            "job_id": row["job_id"],

            "score": row["overall"]

        }

    def lowest_proposal(self):

        row = self.df.loc[

            self.df["overall"].idxmin()

        ]

        return {

            "job_id": row["job_id"],

            "score": row["overall"]

        }

    def score_distribution(self):

        excellent = len(

            self.df[self.df["overall"] >= 50]

        )

        good = len(

            self.df[

                (self.df["overall"] >= 45)

                &

                (self.df["overall"] < 50)

            ]

        )

        improvement = len(

            self.df[self.df["overall"] < 45]

        )

        return {

            "excellent": excellent,

            "good": good,

            "needs_improvement": improvement

        }

    def strengths_and_weaknesses(self):

        averages = self.average_scores()

        strengths = []

        improvements = []

        critical = []

        for metric, score in averages.items():

            category = self.classify(score)

            if category == "Strength":

                strengths.append(metric)

            elif category == "Needs Improvement":

                improvements.append(metric)

            else:

                critical.append(metric)

        return {

            "strengths": strengths,

            "improvements": improvements,

            "critical": critical

        }

    def summary(self):

        return {

            "total": len(self.df),

            "average_overall": self.overall_average(),

            "average_metrics": self.average_scores(),

            "highest": self.highest_proposal(),

            "lowest": self.lowest_proposal(),

            "distribution": self.score_distribution(),

            "analysis": self.strengths_and_weaknesses()

        }
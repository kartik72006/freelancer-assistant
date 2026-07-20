from collections import Counter
import re


class FeedbackAnalyzer:

    def __init__(self, dataframe):

        self.df = dataframe

        self.feedback_columns = [

            "relevance_feedback",

            "accuracy_feedback",

            "personalization_feedback",

            "completeness_feedback",

            "tone_feedback",

            "hallucination_feedback"

        ]

    def feedback_by_metric(self):

        feedback = {}

        for column in self.feedback_columns:

            if column not in self.df.columns:

                feedback[column] = []

                continue

            comments = [

                str(comment).strip()

                for comment in self.df[column]

                if str(comment).strip()

            ]

            feedback[column] = comments

        return feedback

    def most_common_feedback(self, top_n=5):

        summary = {}

        feedback = self.feedback_by_metric()

        for column, comments in feedback.items():

            counter = Counter(comments)

            summary[column] = counter.most_common(top_n)

        return summary

    def strongest_feedback(self):

        summary = self.most_common_feedback()

        strengths = {}

        for metric, comments in summary.items():

            strengths[metric] = [

                comment

                for comment, count in comments

                if count >= 2

            ]

        return strengths

    def keyword_frequency(self):

        keywords = Counter()

        feedback = self.feedback_by_metric()

        stop_words = {

            "the",

            "a",

            "an",

            "is",

            "are",

            "and",

            "of",

            "to",

            "for",

            "with",

            "that",

            "this",

            "it",

            "in",

            "on",

            "as",

            "be",

            "or",

            "by",

            "from"

        }

        for comments in feedback.values():

            for comment in comments:

                words = re.findall(r"\b[a-zA-Z]+\b", comment.lower())

                for word in words:

                    word = word.strip(".,!?():;\"'")

                    if len(word) < 4:

                        continue

                    if word in stop_words:

                        continue

                    keywords[word] += 1

        return keywords.most_common(20)

    def summary(self):

        return {

            "feedback": self.feedback_by_metric(),

            "common_feedback": self.most_common_feedback(),

            "strong_feedback": self.strongest_feedback(),

            "keywords": self.keyword_frequency()

        }
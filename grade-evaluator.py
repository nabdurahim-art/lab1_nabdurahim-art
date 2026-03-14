import csv
import os


class Assignment:
    def __init__(self, name, category, score, weight):
        self.name = name
        self.category = category.lower()
        self.score = float(score)
        self.weight = float(weight)

    def is_valid_score(self):
        return 0 <= self.score <= 100


class GradeEvaluator:
    def __init__(self):
        self.assignments = []

    def load_data(self, filename):
        if not os.path.exists(filename):
            print("Error: grades.csv file not found.")
            return False

        with open(filename, "r") as file:
            reader = csv.DictReader(file)

            rows = list(reader)
            if len(rows) == 0:
                print("Error: CSV file is empty.")
                return False

            for row in rows:
                assignment = Assignment(
                    row["Assignment"],
                    row["Category"],
                    row["Score"],
                    row["Weight"]
                )
                self.assignments.append(assignment)

        return True

    def validate_scores(self):
        for a in self.assignments:
            if not a.is_valid_score():
                print(f"Invalid score for {a.name}")
                return False
        return True

    def validate_weights(self):
        total_weight = sum(a.weight for a in self.assignments)

        formative = sum(a.weight for a in self.assignments if a.category == "formative")
        summative = sum(a.weight for a in self.assignments if a.category == "summative")

        if total_weight != 100:
            print("Error: Total weight must equal 100")
            return False

        if formative != 60 or summative != 40:
            print("Error: Formative must be 60 and Summative must be 40")
            return False

        return True

    def calculate_totals(self):
        formative_score = 0
        summative_score = 0

        for a in self.assignments:
            weighted = (a.score * a.weight) / 100

            if a.category == "formative":
                formative_score += weighted
            else:
                summative_score += weighted

        total = formative_score + summative_score
        return formative_score, summative_score, total

    def calculate_gpa(self, total):
        return (total / 100) * 5.0

    def pass_fail(self, formative, summative):
        if formative >= 50 and summative >= 50:
            return "PASSED"
        return "FAILED"

    def resubmission(self):
        failed = [
            a for a in self.assignments
            if a.category == "formative" and a.score < 50
        ]

        if not failed:
            return []

        max_weight = max(a.weight for a in failed)

        return [a.name for a in failed if a.weight == max_weight]


def main():

    evaluator = GradeEvaluator()

    if not evaluator.load_data("grades.csv"):
        return

    if not evaluator.validate_scores():
        return

    if not evaluator.validate_weights():
        return

    formative, summative, total = evaluator.calculate_totals()

    gpa = evaluator.calculate_gpa(total)

    status = evaluator.pass_fail(formative, summative)

    resubmit = evaluator.resubmission()

    print("Formative Score:", formative)
    print("Summative Score:", summative)
    print("Total Score:", total)
    print("GPA:", round(gpa, 2))
    print("Final Status:", status)

    if resubmit:
        print("Eligible for Resubmission:", ", ".join(resubmit))


if __name__ == "__main__":
    main()

import csv
import os
import sys

TOTAL_WEIGHT_REQUIRED = 100
FORMATIVE_WEIGHT_REQUIRED = 60
SUMMATIVE_WEIGHT_REQUIRED = 40

FORMATIVE_PASS_MARK = 30
SUMMATIVE_PASS_MARK = 20

GPA_SCALE = 5.0

VALID_GROUPS = ["formative", "summative"]

class Assignment:
    def __init__(self, name, group, score, weight):
        """
        Initialize an Assignment object.
        Converts inputs to proper types and cleans whitespace.
        Raises ValueError if conversion fails.
        """
        try:
            self.name = str(name).strip()
            self.group = str(group).strip().lower()
            self.score = float(score)
            self.weight = float(weight)
        except Exception:
            raise ValueError("Invalid assignment data format")

    def is_valid_score(self):
        """Check if score is between 0 and 100."""
        return 0 <= self.score <= 100

    def is_valid_group(self):
        """Check if assignment group is valid."""
        return self.group in VALID_GROUPS


class GradeEvaluator:
    def __init__(self, assignments):
        """Initialize GradeEvaluator with assignments."""
        self.assignments = assignments

    def validate_scores(self):
        """Ensure all assignment scores are valid."""
        for a in self.assignments:
            if not a.is_valid_score():
                print(f"Error: Invalid score for {a.name}")
                return False
        return True

    def validate_weights(self):
        """
        Validate weight rules:
        • Total weight must equal TOTAL_WEIGHT_REQUIRED
        • Formative must equal FORMATIVE_WEIGHT_REQUIRED
        • Summative must equal SUMMATIVE_WEIGHT_REQUIRED
        """
        total_weight = sum(a.weight for a in self.assignments)
        formative = sum(a.weight for a in self.assignments if a.group == "formative")
        summative = sum(a.weight for a in self.assignments if a.group == "summative")

        if round(total_weight, 2) != TOTAL_WEIGHT_REQUIRED:
            print(f"Error: Total weight must equal {TOTAL_WEIGHT_REQUIRED}")
            return False

        if round(formative, 2) != FORMATIVE_WEIGHT_REQUIRED or round(summative, 2) != SUMMATIVE_WEIGHT_REQUIRED:
            print(f"Error: Formative must total {FORMATIVE_WEIGHT_REQUIRED} "
                  f"and Summative must total {SUMMATIVE_WEIGHT_REQUIRED}")
            return False

        return True

    def calculate_totals(self):
        """
        Calculate weighted scores.
        Returns:
        • formative_score
        • summative_score
        • total_score
        """
        formative_score = 0
        summative_score = 0

        for a in self.assignments:
            weighted = (a.score * a.weight) / 100
            if a.group == "formative":
                formative_score += weighted
            elif a.group == "summative":
                summative_score += weighted

        total = formative_score + summative_score
        return formative_score, summative_score, total

    def calculate_gpa(self, total):
        """Convert percentage score to GPA scale."""
        return (total / 100) * GPA_SCALE

    def pass_fail(self, formative, summative):
        """
        Determine pass/fail status.
        Student must score minimum marks in BOTH categories.
        """
        return "PASSED" if formative >= FORMATIVE_PASS_MARK and summative >= SUMMATIVE_PASS_MARK else "FAILED"

    def resubmission(self):
        """
        Find formative assignments eligible for resubmission.
        Rule:
        • Score < 50
        • Choose assignment(s) with highest weight
        """
        failed = [
            a for a in self.assignments
            if a.group == "formative" and a.score < 50
        ]

        if not failed:
            return []

        max_weight = max(a.weight for a in failed)
        return [a.name for a in failed if a.weight == max_weight]
 
def load_csv_data():

    """
    Ask user for CSV filename and load assignment data.
    Returns a list of Assignment objects.
 """
    filename = input("Enter the CSV filename (e.g., grades.csv): ").strip()

    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)

    assignments = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)

            # Required CSV headers
            required_headers = {"assignment", "group", "score", "weight"}

            if not reader.fieldnames or not required_headers.issubset(set(reader.fieldnames)):
                print("Error: CSV headers incorrect.")
                print("Required headers:", required_headers)
                sys.exit(1)

            rows = list(reader)
            if not rows:
                print("Error: CSV file is empty.")
                sys.exit(1)

            for row in rows:
                if not row["assignment"] or not row["group"] or not row["score"] or not row["weight"]:
                    print("Warning: Skipping row with missing data.")
                    continue

                try:
                    assignment = Assignment(
                        row["assignment"],
                        row["group"],
                        row["score"],
                        row["weight"]
                    )

                    if not assignment.is_valid_group():
                        print(f"Warning: Invalid group '{assignment.group}' in {assignment.name}")
                        continue

                    assignments.append(assignment)

                except ValueError as ve:
                    print(f"Warning: {ve} in row {row}")
                    continue

    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)

    if not assignments:
        print("Error: No valid assignment data found.")
        sys.exit(1)

    return assignments


def evaluate_grades(assignments):
    evaluator = GradeEvaluator(assignments)

    if not evaluator.validate_scores():
        return
    if not evaluator.validate_weights():
        return

    formative, summative, total = evaluator.calculate_totals()
    gpa = evaluator.calculate_gpa(total)
    status = evaluator.pass_fail(formative, summative)
    resubmit = evaluator.resubmission()

    print("\n===== STUDENT TRANSCRIPT =====")
    print("Formative Score:", round(formative, 2))
    print("Summative Score:", round(summative, 2))
    print("Total Score:", round(total, 2))
    print("GPA:", round(gpa, 2))
    print("Final Status:", status)

    if resubmit:
        print("Eligible for Resubmission:", ", ".join(resubmit))
    else:
        print("No Resubmission Needed")


if __name__ == "__main__":
    try:
        assignments = load_csv_data()
        evaluate_grades(assignments)
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    except Exception as e:
        print(f"\nUnexpected system error: {e}")

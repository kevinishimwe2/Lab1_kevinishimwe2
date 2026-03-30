import csv
import sys
import os

def load_csv_data():
    """
    Prompts the user for a filename, checks if it exists, 
    and extracts all fields into a list of dictionaries.
    """
    filename = input("Enter the name of the CSV file to process (e.g., grades.csv): ")
    
    if not os.path.exists(filename):
        print(f"Error: The file '{filename}' was not found.")
        sys.exit(1)
    
    assignments = []
    
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Convert numeric fields to floats for calculations
                assignments.append({
                    'assignment': row['assignment'],
                    'group': row['group'],
                    'score': float(row['score']),
                    'weight': float(row['weight'])
                })

        # Handle the case where the CSV file exists but is completely empty
        if len(assignments) == 0:
            print("Error: The CSV file is empty. No grades to process.")
            sys.exit(1)

        return assignments
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        sys.exit(1)


def evaluate_grades(data):
    """
    Implement your logic here.
    'data' is a list of dictionaries containing the assignment records.
    """
    print("\n--- Processing Grades ---")

    # TODO: a) Check if all scores are percentage based (0-100)
    # Loop through every assignment and verify that the score falls within
    # the valid range of 0 to 100. If any score is out of range, report it
    # and stop processing since the data cannot be trusted.
    invalid_scores = []
    for record in data:
        if record['score'] < 0 or record['score'] > 100:
            invalid_scores.append(record['assignment'])

    if len(invalid_scores) > 0:
        print(f"Error: The following assignments have scores outside the 0-100 range: {', '.join(invalid_scores)}")
        sys.exit(1)
    else:
        print("✔ All scores are valid (0-100).")

    # TODO: b) Validate total weights (Total=100, Summative=40, Formative=60)
    # Sum the weights for each group separately, then check that:
    #   - The overall total of all weights equals exactly 100
    #   - Summative weights sum to exactly 40
    #   - Formative weights sum to exactly 60
    total_weight = 0
    summative_weight = 0
    formative_weight = 0

    for record in data:
        total_weight += record['weight']
        if record['group'].strip().lower() == 'summative':
            summative_weight += record['weight']
        elif record['group'].strip().lower() == 'formative':
            formative_weight += record['weight']

    weight_errors = []
    if round(total_weight, 2) != 100:
        weight_errors.append(f"Total weight is {total_weight} (expected 100).")
    if round(summative_weight, 2) != 40:
        weight_errors.append(f"Summative weight is {summative_weight} (expected 40).")
    if round(formative_weight, 2) != 60:
        weight_errors.append(f"Formative weight is {formative_weight} (expected 60).")

    if len(weight_errors) > 0:
        for err in weight_errors:
            print(f"Error: {err}")
        sys.exit(1)
    else:
        print("✔ Weight validation passed (Total=100, Summative=40, Formative=60).")

    # TODO: c) Calculate the Final Grade and GPA
    # Compute the weighted score for each assignment: (score / 100) * weight.
    # Sum all weighted scores to get the overall final grade (out of 100).
    # Also track the weighted score totals per group so we can check pass/fail
    # per category in the next step.
    # GPA formula: GPA = (Final Grade / 100) * 5.0
    final_grade = 0
    summative_score = 0   # Accumulated weighted score for summative assignments
    formative_score = 0   # Accumulated weighted score for formative assignments

    for record in data:
        weighted = (record['score'] / 100) * record['weight']
        final_grade += weighted
        if record['group'].strip().lower() == 'summative':
            summative_score += weighted
        elif record['group'].strip().lower() == 'formative':
            formative_score += weighted

    gpa = (final_grade / 100) * 5.0

    # Convert per-group weighted scores to a percentage of that group's total weight
    # so we can compare against the 50% threshold on a fair scale.
    summative_percentage = (summative_score / summative_weight) * 100
    formative_percentage = (formative_score / formative_weight) * 100

    print(f"\n--- Grade Summary ---")
    print(f"  Summative Score : {summative_score:.2f} / {summative_weight:.0f}  ({summative_percentage:.2f}%)")
    print(f"  Formative Score : {formative_score:.2f} / {formative_weight:.0f}  ({formative_percentage:.2f}%)")
    print(f"  Final Grade     : {final_grade:.2f}%")
    print(f"  GPA             : {gpa:.2f} / 5.0")

    # TODO: d) Determine Pass/Fail status (>= 50% in BOTH categories)
    # A student passes only when BOTH the summative percentage AND the formative
    # percentage are at least 50%. Failing even one category means overall failure.
    summative_passed = summative_percentage >= 50
    formative_passed = formative_percentage >= 50
    overall_passed = summative_passed and formative_passed

    # TODO: e) Check for failed formative assignments (< 50%)
    #          and determine which one(s) have the highest weight for resubmission.
    # Collect every formative assignment where the score is below 50%.
    # Among those failed formative assignments, find the maximum weight value.
    # Any failed formative assignment that matches that maximum weight is eligible
    # for resubmission (handles ties correctly).
    failed_formative = []
    for record in data:
        if record['group'].strip().lower() == 'formative' and record['score'] < 50:
            failed_formative.append(record)

    resubmission_candidates = []
    if len(failed_formative) > 0:
        # Find the highest weight among failed formative assignments manually
        max_failed_weight = failed_formative[0]['weight']
        for record in failed_formative:
            if record['weight'] > max_failed_weight:
                max_failed_weight = record['weight']

        # Collect all failed formative assignments that share that highest weight
        for record in failed_formative:
            if record['weight'] == max_failed_weight:
                resubmission_candidates.append(record)

    # TODO: f) Print the final decision (PASSED / FAILED) and resubmission options
    # Display the overall PASSED / FAILED verdict clearly.
    # If the student failed, explain which category caused the failure.
    # Then list whichever failed formative assignment(s) are recommended for
    # resubmission (those with the highest weight among failed formatives).
    print(f"\n--- Final Decision ---")
    if overall_passed:
        print("  Status: PASSED ✔")
    else:
        print("  Status: FAILED ✘")
        if not summative_passed:
            print(f"  Reason: Summative score ({summative_percentage:.2f}%) is below 50%.")
        if not formative_passed:
            print(f"  Reason: Formative score ({formative_percentage:.2f}%) is below 50%.")

    print(f"\n--- Resubmission Recommendation ---")
    if len(resubmission_candidates) == 0:
        print("  No formative assignments failed. No resubmission required.")
    else:
        print(f"  The following failed formative assignment(s) carry the highest weight")
        print(f"  and are eligible for resubmission:")
        for record in resubmission_candidates:
            print(f"    • {record['assignment']}  (Score: {record['score']:.1f}%,  Weight: {record['weight']:.1f}%)")


if __name__ == "__main__":
    # 1. Load the data
    course_data = load_csv_data()

    # 2. Process the features
    evaluate_grades(course_data)
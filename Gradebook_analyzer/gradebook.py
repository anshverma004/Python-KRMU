# """
# GradeBook Analyzer
# Author : Ansh Verma
# Date   : 25 Nov 2025
# Title  : Mini Project – GradeBook Analyzer
# """

import csv
import statistics

# ------------------------------
# Task 1: Welcome + Menu
# ------------------------------

def print_menu():
    print("\n====== GradeBook Analyzer ======")
    print("1. Manual Entry")
    print("2. Load from CSV")
    print("3. Exit")
    print("================================\n")

# ------------------------------
# Task 2: Data Entry Methods
# ------------------------------

def manual_input():
    marks = {}
    n = int(input("Enter number of students: "))
    for _ in range(n):
        name = input("Enter student name: ")
        score = float(input("Enter marks: "))
        marks[name] = score
    return marks


def load_csv():
    marks = {}
    file_path = input("Enter CSV filename (example: marks.csv): ")

    try:
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            next(reader)  # skip header if present

            for row in reader:
                if len(row) >= 2:
                    name = row[0]
                    score = float(row[1])
                    marks[name] = score
        print("CSV loaded successfully!")
    except FileNotFoundError:
        print("File not found. Try again.")

    return marks

# ------------------------------
# Task 3: Statistical Functions
# ------------------------------

def calculate_average(marks_dict):
    return sum(marks_dict.values()) / len(marks_dict)

def calculate_median(marks_dict):
    return statistics.median(marks_dict.values())

def find_max_score(marks_dict):
    return max(marks_dict.values())

def find_min_score(marks_dict):
    return min(marks_dict.values())

# ------------------------------
# Task 4: Grade Assignment
# ------------------------------

def assign_grades(marks_dict):
    grades = {}

    for name, score in marks_dict.items():
        if score >= 90:
            grade = "A"
        elif score >= 80:
            grade = "B"
        elif score >= 70:
            grade = "C"
        elif score >= 60:
            grade = "D"
        elif score >= 40:
            grade = "E"
        else:
            grade = "F"

        grades[name] = grade

    return grades


def grade_distribution(grades):
    dist = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0}

    for g in grades.values():
        dist[g] += 1
    
    return dist

# ------------------------------
# Task 5: Pass/Fail using list comprehension
# ------------------------------

def pass_fail_list(marks_dict):
    passed = [name for name, score in marks_dict.items() if score >= 40]
    failed = [name for name, score in marks_dict.items() if score < 40]
    return passed, failed

# ------------------------------
# Task 6: Results Table + Loop
# ------------------------------

def print_table(marks_dict, grades):
    print("\nName\t\tMarks\tGrade")
    print("------------------------------------------")
    for name, score in marks_dict.items():
        print(f"{name}\t\t{score}\t{grades[name]}")
    print("------------------------------------------")

def save_to_csv(marks_dict, grades):
    out = "output_gradebook.csv"
    with open(out, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Marks", "Grade"])
        for name, score in marks_dict.items():
            writer.writerow([name, score, grades[name]])
    print(f"File saved as: {out}")


# ------------------------------
# MAIN PROGRAM LOOP
# ------------------------------

def main():
    print("\nWelcome to GradeBook Analyzer!")
    
    while True:
        print_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            marks = manual_input()

        elif choice == "2":
            marks = load_csv()

        elif choice == "3":
            print("Exiting program. Goodbye!")
            break

        else:
            print("Invalid choice.")
            continue

        if len(marks) == 0:
            print("No student data available. Try again.")
            continue

        # --- Perform Analysis ---
        print("\n--- Analysis Summary ---")
        print("Average :", calculate_average(marks))
        print("Median  :", calculate_median(marks))
        print("Max     :", find_max_score(marks))
        print("Min     :", find_min_score(marks))

        # Grade assignment
        grades = assign_grades(marks)

        print("\n--- Grade Distribution ---")
        dist = grade_distribution(grades)
        for g, c in dist.items():
            print(f"{g}: {c}")

        # Pass / Fail list
        passed, failed = pass_fail_list(marks)
        print("\nPassed Students:", passed)
        print("Failed Students:", failed)

        # Print formatted table
        print_table(marks, grades)

        # Optional CSV output
        save = input("\nSave results to CSV? (y/n): ")
        if save.lower() == 'y':
            save_to_csv(marks, grades)

        again = input("\nRun another analysis? (y/n): ")
        if again.lower() != 'y':
            print("Thank you for using GradeBook Analyzer!")
            break


# Run script
if __name__ == "__main__":
    main()

import os
import matplotlib.pyplot as plt

def load_students(filepath):
    students = {}
    with open(filepath, 'r') as file:
        for line in file:
            id, name = line[:3], line[3:].strip()
            students[int(id)] = name
    return students

def load_assignments(filepath):
    assignments = {}
    with open(filepath, 'r') as file:
        lines = file.readlines()
        for i in range(0, len(lines), 3):
            name = lines[i].strip()
            id = int(lines[i + 1].strip())
            points = int(lines[i + 2].strip())
            assignments[id] = {'name': name, 'points': points}
    return assignments

def load_submissions():
    submissions = []
    submissions_dir = "data/submissions"

    try:
        for filename in os.listdir(submissions_dir):
            filepath = os.path.join(submissions_dir, filename)
            if os.path.isfile(filepath):
                with open(filepath, 'r') as file:
                    for line in file:
                        parts = line.strip().split('|')
                        if len(parts) == 3:
                            student_id, assignment_id, score = map(float, parts)
                            submissions.append({
                                'student_id': int(student_id),
                                'assignment_id': int(assignment_id),
                                'score': score
                            })
                        else:
                            print(f"Warning: Skipping invalid line in {filename}: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: Directory '{submissions_dir}' not found.")
    except ValueError as e:
        print(f"Error parsing submission data: {e}")
    return submissions

def calculate_student_grade(student_id, submissions, assignments):
    total_score = 0
    total_possible = 0
    for submission in submissions:
        if submission['student_id'] == student_id:
            assignment_id = submission['assignment_id']
            score = submission['score']
            points = assignments[assignment_id]['points']
            total_score += score / 100 * points
            total_possible += points
    return int((total_score / total_possible) * 100) if total_possible > 0 else None

def calculate_assignment_statistics(assignment_id, submissions):
    scores = [
        submission['score'] for submission in submissions
        if submission['assignment_id'] == assignment_id
    ]
    if not scores:
        return None
    return (
        int(min(scores)),
        int(sum(scores) // len(scores)),  # Truncate decimals for average
        int(max(scores))
    )

def display_assignment_histogram(assignment_id, submissions):
    scores = [
        submission['score'] for submission in submissions
        if submission['assignment_id'] == assignment_id
    ]
    if not scores:
        print("No scores available for this assignment.")
        return
    plt.hist(scores, bins=[40, 50, 60, 70, 80, 90, 100])

    plt.show()

def main():
    students_file = "data/students.txt"
    assignments_file = "data/assignments.txt"

    students = load_students(students_file)
    assignments = load_assignments(assignments_file)
    submissions = load_submissions()

    print("1. Student grade")
    print("2. Assignment statistics")
    print("3. Assignment graph")
    choice = input("\nEnter your selection: ").strip()

    if choice == "1":
        name = input("What is the student's name: ").strip()
        student_id = next((id for id, n in students.items() if n == name), None)
        if student_id is None:
            print("Student not found")
        else:
            grade = calculate_student_grade(student_id, submissions, assignments)
            print(f"{grade}%")
    elif choice == "2":
        name = input("What is the assignment name: ").strip()
        assignment_id = next(
            (id for id, info in assignments.items() if info['name'] == name),
            None
        )
        if assignment_id is None:
            print("Assignment not found")
        else:
            stats = calculate_assignment_statistics(assignment_id, submissions)
            if stats:
                print(f"Min: {stats[0]}%")
                print(f"Avg: {stats[1]}%")
                print(f"Max: {stats[2]}%")
    elif choice == "3":
        name = input("What is the assignment name: ").strip()
        assignment_id = next(
            (id for id, info in assignments.items() if info['name'] == name),
            None
        )
        if assignment_id is None:
            print("Assignment not found")
        else:
            display_assignment_histogram(assignment_id, submissions)
    else:
        print("Invalid selection. Exiting.")

if __name__ == "__main__":
    main()

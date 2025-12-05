import ATA.pickle_ops as pickle_ops
from ATA.models import Course, Student
import json


def proceed_team_matching(max_size: int) -> None:
    """Run team matching with the given max team size."""
    if not isinstance(max_size, int):
        print("Invalid input, please enter a valid integer.")
        return
    if max_size <= 1:
        print("Invalid input, please enter a valid integer greater than 1.")
        return
    print()
    course = pickle_ops.load_data()
    course.team_matching(max_size)
    pickle_ops.save_data(course)


def return_all_students_name() -> list[str]:
    """Return list of student names (legacy function, kept for compatibility)."""
    course = pickle_ops.load_data()
    return [student.first_name for student in course.students]


def display_all_students():
    """Display all students with their name, email, and team_id."""
    course = pickle_ops.load_data()
    print(f"Number of students: {len(course.students)}")
    print()
    if len(course.students) == 0:
        print("No students found.")
        return
    
    for student in course.students:
        team_id = student.team_id if student.team_id else "None"
        print(f"  {student.first_name} | {student.email} | Team: {team_id}")


def upload_test_data():
    """Load test users from JSON and update/add them to the current course."""
    with open("test/test_user.json", "r") as f:
        data = json.load(f)
    course = pickle_ops.load_data()

    for student_data in data["students"].values():
        student = Student(
            first_name=student_data["first_name"],
            email=student_data["email"],
            skill_level=student_data["skill_level"],
            ambition=student_data["ambition"],
            role=student_data["role"],
            teamwork_style=student_data["teamwork_style"],
            pace=student_data["pace"],
            backgrounds=set(student_data["backgrounds"]),  # convert list to set
            backgrounds_preference=student_data["backgrounds_preference"],
            hobbies=set(student_data["hobbies"]),  # convert list to set
            project_summary=student_data["project_summary"],
        )
        # Use update_student to ensure existing students are updated, not duplicated
        course.update_student(student)

    pickle_ops.save_data(course)


def clear_team_assignments_cli():
    """CLI helper to clear all team assignments but keep students."""
    course = pickle_ops.load_data()
    course.clear_team_assignments()
    pickle_ops.save_data(course)
    print("All team assignments have been cleared (students kept).")


def remove_student_cli():
    """CLI helper to remove a single student by email."""
    email = input("Enter the email of the student to remove: ").strip()
    course = pickle_ops.load_data()
    try:
        course.remove_student_by_email(email)
        pickle_ops.save_data(course)
        print(f"Student with email {email} has been removed.")
    except ValueError:
        print(f"No student found with email {email}.")


q = """_____________________________________
Please enter the following command:
S - current students
T - team matching
P - print results
R - reset system (delete all students)
U - clear all team assignments (keep students)
D - delete a student by email
test - input test data

INPUT: """


def main():
    # Try to load existing course; if not found, create a new empty course.
    try:
        course = pickle_ops.load_data()
        if not isinstance(course, Course):
            raise Exception("Loaded data is not a Course instance")
    except Exception:
        course = Course([])
        pickle_ops.save_data(course)
        print("Initialized new empty course data file.")

    while True:
        inp = input(q)
        if inp.lower() == "s":
            print()
            display_all_students()
        elif inp.lower() == "t":
            print()
            try:
                team_size = int(input("Enter team size: "))
            except ValueError:
                print("Invalid input, please enter a valid integer.")
                continue
            proceed_team_matching(team_size)
            print("Team matching completed.")
        elif inp.lower() == "p":
            print()
            course = pickle_ops.load_data()
            course.print_result()
        elif inp.lower() == "r":
            print()
            confirm = input("Are you sure you want to reset the system (delete all students)? (y/n): ")
            if confirm.lower() in ("y", "yes"):
                course = Course([])
                pickle_ops.save_data(course)
                print("System has been fully reset (all students deleted).")
        elif inp.lower() == "u":
            print()
            clear_team_assignments_cli()
        elif inp.lower() == "d":
            print()
            remove_student_cli()
        elif inp.lower() == "test":
            upload_test_data()
            print("Test data uploaded.")
        else:
            print("Invalid command, please try again.")
        print()


if __name__ == "__main__":
    main()
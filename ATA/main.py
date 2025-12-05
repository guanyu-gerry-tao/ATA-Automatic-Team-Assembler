import ATA.pickle_ops as pickle_ops
from ATA.models import Course, Student
import json


def proceed_team_matching(max_size: int) -> None:
    """Run team matching with the given max team size.
    
    Args:
        max_size: Maximum number of students per team.
    """
    # Validate input - must be an integer
    if not isinstance(max_size, int):
        print("Invalid input, please enter a valid integer.")
        return
    
    # Validate input - must be greater than 1 (can't form teams with 1 or fewer students)
    if max_size <= 1:
        print("Invalid input, please enter a valid integer greater than 1.")
        return
    
    print()  # blank line for formatting
    
    # Load course data and run matching algorithm
    course = pickle_ops.load_data()  # load existing course data
    course.team_matching(max_size)  # run team matching with specified max team size
    pickle_ops.save_data(course)  # save updated course data with team assignments


def return_all_students_name() -> list[str]:
    """Return list of student names.
    
    Legacy function kept for compatibility. Consider using display_all_students() instead.
    
    Returns:
        List of student first names.
    """
    course = pickle_ops.load_data()  # load course data
    return [student.first_name for student in course.students]  # extract and return list of student names


def display_all_students():
    """Display all students with their name, email, and team_id.
    
    Prints formatted output showing each student's information and current team assignment.
    """
    course = pickle_ops.load_data()  # load course data
    
    # Display total number of students
    print(f"Number of students: {len(course.students)}")
    print()  # blank line for formatting
    
    # Handle empty student list
    if len(course.students) == 0:
        print("No students found.")
        return  # exit early if no students
    
    # Display each student with their information
    for student in course.students:
        team_id = student.team_id if student.team_id else "None"  # show "None" if not in a team
        print(f"  {student.first_name} | {student.email} | Team: {team_id}")  # formatted output


def upload_test_data():
    """Load test users from JSON and update/add them to the current course.
    
    Reads test/test_user.json and updates existing students (by email) or adds new ones.
    Uses update_student() to prevent duplicates.
    """
    # Load test data from JSON file
    with open("test/test_user.json", "r") as f:
        data = json.load(f)  # parse JSON file
    
    course = pickle_ops.load_data()  # load existing course data

    # Process each student from test data
    for student_data in data["students"].values():
        # Create Student object from JSON data
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
        # if student with same email exists, update their info; otherwise add as new
        course.update_student(student)

    # Save updated course data
    pickle_ops.save_data(course)


def clear_team_assignments_cli():
    """CLI helper to clear all team assignments but keep students.
    
    Removes all team assignments and resets students to not-in-team status,
    but preserves all student data.
    """
    course = pickle_ops.load_data()  # load existing course data
    course.clear_team_assignments()  # remove all team assignments but keep students
    pickle_ops.save_data(course)  # save updated course data
    print("All team assignments have been cleared (students kept).")  # confirm operation


def remove_student_cli():
    """CLI helper to remove a single student by email.
    
    Prompts user for email and removes all students with that email from the course.
    """
    # Prompt user for student email
    email = input("Enter the email of the student to remove: ").strip()  # get and clean input
    course = pickle_ops.load_data()  # load existing course data
    
    try:
        course.remove_student_by_email(email)  # attempt to remove student
        pickle_ops.save_data(course)  # save updated course data
        print(f"Student with email {email} has been removed.")  # confirm success
    except ValueError:
        # Handle case where student doesn't exist
        print(f"No student found with email {email}.")  # show error message


# Command prompt string displayed to users
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
    """Main entry point for the CLI application.
    
    Provides an interactive command-line interface for managing students and teams.
    Handles loading/saving course data and routing user commands to appropriate functions.
    """
    # Initialize course data
    # Try to load existing course; if not found, create a new empty course
    try:
        course = pickle_ops.load_data()  # attempt to load existing course data
        if not isinstance(course, Course):  # verify loaded data is a Course instance
            raise Exception("Loaded data is not a Course instance")
    except Exception:
        # If loading fails (file doesn't exist or is corrupted), create new empty course
        course = Course([])  # create empty course
        pickle_ops.save_data(course)  # save empty course to initialize data file
        print("Initialized new empty course data file.")

    # Main command loop - continuously prompt for user input
    while True:
        inp = input(q)  # get user command input
        
        # Command: S - Display all current students
        if inp.lower() == "s":
            print()  # blank line for formatting
            display_all_students()  # show all students with their info
        
        # Command: T - Run team matching algorithm
        elif inp.lower() == "t":
            print()  # blank line for formatting
            try:
                team_size = int(input("Enter team size: "))  # prompt for max team size
            except ValueError:
                # Handle invalid input (non-integer)
                print("Invalid input, please enter a valid integer.")
                continue  # skip to next iteration, prompt again
            proceed_team_matching(team_size)  # run matching algorithm
            print("Team matching completed.")  # confirm completion
        
        # Command: P - Print team matching results
        elif inp.lower() == "p":
            print()  # blank line for formatting
            course = pickle_ops.load_data()  # reload course data to get latest results
            course.print_result()  # display formatted team results
        
        # Command: R - Reset system (delete all students)
        elif inp.lower() == "r":
            print()  # blank line for formatting
            # Ask for confirmation before destructive operation
            confirm = input("Are you sure you want to reset the system (delete all students)? (y/n): ")
            if confirm.lower() in ("y", "yes"):  # check if user confirmed
                course = Course([])  # create empty course (deletes all students)
                pickle_ops.save_data(course)  # save empty course
                print("System has been fully reset (all students deleted).")
            # If user says no, silently continue (no action taken)
        
        # Command: U - Clear all team assignments but keep students
        elif inp.lower() == "u":
            print()  # blank line for formatting
            clear_team_assignments_cli()  # remove team assignments, preserve students
        
        # Command: D - Delete a student by email
        elif inp.lower() == "d":
            print()  # blank line for formatting
            remove_student_cli()  # prompt for email and remove student
        
        # Command: test - Upload test data from JSON file
        elif inp.lower() == "test":
            upload_test_data()  # load and add test students from test_user.json
            print("Test data uploaded.")  # confirm completion
        
        # Invalid command - user entered something not recognized
        else:
            print("Invalid command, please try again.")  # show error message
        
        print()  # blank line after each command for better readability


if __name__ == "__main__":
    main()
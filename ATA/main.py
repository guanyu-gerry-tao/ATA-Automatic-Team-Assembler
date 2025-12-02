import ATA.pickle_ops as pickle_ops
from ATA.models import Course, Student
import json
import requests

data_filepath = "data/data.json"


def proceed_team_matching(max_size: int) -> None:
    if not isinstance(max_size, int):
        print("Invalid input, please enter a valid integer.")
        return
    if max_size <= 1:
        print("Invalid input, please enter a valid integer greater than 1.")
        return
    print() # add a new line
    course = pickle_ops.load_data()
    course.team_matching(max_size)
    pickle_ops.save_data(course)


def return_all_students_name() -> list[str]:
    course = pickle_ops.load_data()
    students_name = []
    for student in course.students:
        students_name.append(student.first_name)
    return students_name


def upload_test_data():
    with open("test/test_user.json", "r") as f:
        data = json.load(f)
    course = pickle_ops.load_data()
    
    # create student objects
    student_objects = []
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
            other_prompts=student_data["other_prompts"],
        )
        student_objects.append(student)
    
    course.add_students(student_objects)
    pickle_ops.save_data(course)


q = """_____________________________________
Please enter the following command:
S - current students
T - team matching
P - print results
R - reset system
test - input test data

INPUT: """

def main():
    course = Course([])
    pickle_ops.save_data(course)
    while True:
        inp = input(q)
        if inp.lower() == "s":
            print()
            students = return_all_students_name()
            print("Number of students: ", len(students))
            print("Student List:\n ", ", ".join(students))
        elif inp.lower() == "t":
            print()  # add a new line
            team_size = int(input("Enter team size: "))
            proceed_team_matching(team_size)
            print("Team matching completed.")
        elif inp.lower() == "p":
            print()
            course = pickle_ops.load_data()
            course.print_result()
        elif inp.lower() == "r":
            print()
            confirm = input("Are you sure you want to reset the system? (y/n): ")
            if confirm.lower() == "y" or confirm.lower() == "yes":
                course = Course([])
                pickle_ops.save_data(course)
                print("System has been reset.")
        elif inp.lower() == "test":
            upload_test_data()
            print("Test data uploaded.")
        else:
            print("Invalid command, please try again.")
        print()


if __name__ == "__main__":
    main()
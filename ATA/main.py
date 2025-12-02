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


q = """
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
            with open("test/test_user.json", "r") as f:
                data = json.load(f)
            for student in data["students"].values():
                requests.post("http://localhost:8000/student_submit", data={"data": json.dumps(student)})
            print("Test data uploaded.")
        else:
            print("Invalid command, please try again.")
        print()


if __name__ == "__main__":
    main()
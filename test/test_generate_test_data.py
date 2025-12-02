import json
import requests
import ATA.pickle_ops as pickle_ops


def upload_test_data():
    with open("test/test_user.json", "r") as f:
        data = json.load(f)

    for student in data["students"].values():
        requests.post("http://localhost:8000/student_submit", data={"data": json.dumps(student)})


if __name__ == "__main__":
    upload_test_data()

    course = pickle_ops.load_data()
    for student in course.students:
        print(student.first_name)
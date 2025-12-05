"""Script to upload test data to the local API server.

Reads test/test_user.json and submits each student to the API endpoint.
Useful for populating the database with test data during development.
"""

import json
import requests
import ATA.pickle_ops as pickle_ops


def upload_test_data():
    """Upload all students from test_user.json to the API server.
    
    Reads test/test_user.json and POSTs each student to http://localhost:8000/student_submit.
    After uploading, prints all student names from the loaded course data.
    """
    with open("test/test_user.json", "r") as f:
        data = json.load(f)

    for student in data["students"].values():
        requests.post("http://localhost:8000/student_submit", data={"data": json.dumps(student)})


if __name__ == "__main__":
    upload_test_data()

    course = pickle_ops.load_data()
    for student in course.students:
        print(student.first_name)
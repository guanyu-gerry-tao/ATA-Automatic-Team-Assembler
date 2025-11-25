import time
import unittest
import requests
import json
import os


class TestIfServerIsUp(unittest.TestCase):
    def test_server_is_up(self):
        result = requests.get("http://localhost:8000/health")
        self.assertEqual(result.status_code, 200)


class TestRecordingSystem(unittest.TestCase):
    def test_student_upload_data(self):
        with open("test/test_user.json", "r") as f:
            data = json.load(f)
            student1 = data["Alice"]
            student2 = data["Bob"]
        result1 = requests.post("http://localhost:8000/student_submit",
                                params={"course_code": "CS5001", "number_of_teaming": 0},
                                data={"data": json.dumps(student1)})
        self.assertEqual(result1.status_code, 200)
        print("Alice uploaded")
        time.sleep(0.1)
        result2 = requests.post("http://localhost:8000/student_submit",
                                params={"course_code": "CS5001", "number_of_teaming": 0},
                                data={"data": json.dumps(student2)})
        self.assertEqual(result2.status_code, 200)
        print("Bob uploaded")
        time.sleep(0.1)

        if not os.path.exists("ATA/student_data/CS5001_0.json"):
            self.fail("No data saved")

        saved = data["Alice"]
        for k, v in student1.items():
            self.assertEqual(saved[k], v)
        saved = data["Bob"]
        for k, v in student2.items():
            self.assertEqual(saved[k], v)


if __name__ == '__main__':
    unittest.main()

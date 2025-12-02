import time
import unittest
import requests
import json
import os


class TestIfServerIsUp(unittest.TestCase):
    def test_server_is_up(self):
        result = requests.get("http://localhost:8000/health")
        self.assertEqual(result.status_code, 200)


class TestRecordingSystemLocalIO(unittest.TestCase):
    def test_student_upload_data(self):
        with open("test/test_user.json", "r") as f:
            data = json.load(f)
            student1 = data["students"]["alice@test.com"]
            student2 = data["students"]["bob@test.com"]
        result1 = requests.post("http://localhost:8000/student_submit",
                                data={"data": json.dumps(student1)})
        self.assertEqual(result1.status_code, 200)
        print("Alice uploaded")
        time.sleep(0.1)
        result2 = requests.post("http://localhost:8000/student_submit",
                                data={"data": json.dumps(student2)})
        self.assertEqual(result2.status_code, 200)
        print("Bob uploaded")
        time.sleep(0.1)

        # if not os.path.exists("ATA/student_data/CS5001_202501.json"):
        #     self.fail("No data saved")
        #
        # with open("ATA/student_data/CS5001_202501.json", "r") as f:
        #     saved_data = json.load(f)
        #
        # saved_alice = saved_data["students"]["alice@test.com"]
        # saved_bob = saved_data["students"]["bob@test.com"]
        #
        # for k, v in student1.items():
        #     if k not in ["uid", "student_ip"]:
        #         self.assertEqual(saved_alice[k], v)
        #
        # for k, v in student2.items():
        #     if k not in ["uid", "student_ip"]:
        #         self.assertEqual(saved_bob[k], v)


if __name__ == '__main__':
    unittest.main()

"""Test suite for the backend API server.

Tests the FastAPI endpoints including student submission, status checking,
and data persistence. Requires the API server to be running on localhost:8000.
"""

import time
import unittest
import requests
import json
from ATA.models import Course
from ATA import pickle_ops


class TestIfServerIsUp(unittest.TestCase):
    """Test if the server is running."""
    
    def test_server_is_up(self):
        result = requests.get("http://localhost:8000/health")
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json()["status"], "ok")


class TestBackendAPI(unittest.TestCase):
    """Test backend API endpoints."""
    
    def setUp(self):
        """Clear data before each test.
        
        Creates an empty Course and saves it to ensure clean state for each test.
        """
        course = Course([])
        pickle_ops.save_data(course)
    
    def tearDown(self):
        """Clear data after each test.
        
        Creates an empty Course and saves it to clean up after each test.
        """
        course = Course([])
        pickle_ops.save_data(course)
    
    def load_student(self, email: str):
        """Load student data from test_user.json.
        
        Args:
            email: Email address of the student to load.
            
        Returns:
            Dictionary containing student data from test_user.json.
        """
        with open("test/test_user.json", "r") as f:
            data = json.load(f)
        return data["students"][email]
    
    def test_submit_student(self):
        """Test submitting a student."""
        student = self.load_student("alice@test.com")
        
        response = requests.post(
            "http://localhost:8000/student_submit",
            data={"data": json.dumps(student)}
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        
        # Verify student was saved
        course = pickle_ops.load_data()
        self.assertEqual(len(course.students), 1)
        self.assertEqual(course.students[0].email, "alice@test.com")
    
    def test_update_student_same_email(self):
        """Test that same email updates instead of adding duplicate."""
        student = self.load_student("alice@test.com")
        
        # Submit first time
        requests.post(
            "http://localhost:8000/student_submit",
            data={"data": json.dumps(student)}
        )
        time.sleep(0.1)
        
        # Update with same email
        student["first_name"] = "Alice Updated"
        student["project_summary"] = "Updated summary"
        
        requests.post(
            "http://localhost:8000/student_submit",
            data={"data": json.dumps(student)}
        )
        time.sleep(0.1)
        
        # Verify updated, not duplicated
        course = pickle_ops.load_data()
        self.assertEqual(len(course.students), 1)
        self.assertEqual(course.students[0].first_name, "Alice Updated")
    
    def test_check_status(self):
        """Test check_status endpoint."""
        student = self.load_student("alice@test.com")
        
        requests.post(
            "http://localhost:8000/student_submit",
            data={"data": json.dumps(student)}
        )
        time.sleep(0.1)
        
        response = requests.get(
            "http://localhost:8000/check_status",
            params={"email": "alice@test.com"}
        )
        
        self.assertEqual(response.status_code, 200)
        result = response.json()
        self.assertEqual(result["status"], "ok")
        self.assertFalse(result["has_result"])


if __name__ == '__main__':
    unittest.main()

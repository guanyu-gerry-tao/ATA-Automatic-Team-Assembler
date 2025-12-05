"""Test suite for vector construction and team matching.

Tests the Student.construct_vector() method and Course.team_matching() algorithm
to ensure vectors are correctly constructed and teams are properly formed.
"""

import unittest
import numpy as np
from ATA.models import Student, Course
from ATA.config import CONFIG
import json
import math


def student_data_opener(test_file_path: str):
    """Load JSON test data file.
    
    Args:
        test_file_path: Path to the JSON test data file.
        
    Returns:
        Parsed JSON data as dictionary.
    """
    with open(test_file_path, "r") as f:
        return json.load(f)


def student_data_importer_helper(json_file, email):
    """Create a Student object from JSON data.
    
    Args:
        json_file: Parsed JSON data dictionary.
        email: Email address of the student to import.
        
    Returns:
        Student object created from the JSON data.
    """
    data = json_file["students"][email]
    student = Student(
        first_name=data["first_name"],
        email=data["email"],
        skill_level=data["skill_level"],
        ambition=data["ambition"],
        role=data["role"],
        teamwork_style=data["teamwork_style"],
        pace=data["pace"],
        backgrounds=set(data["backgrounds"]),
        backgrounds_preference=data["backgrounds_preference"],
        hobbies=set(data["hobbies"]),
        project_summary=data["project_summary"]
    )
    return student


def load_all_test_students_helper(test_file_path: str):
    """Load all students from test JSON file.
    
    Args:
        test_file_path: Path to the JSON test data file.
        
    Returns:
        List of Student objects created from the JSON data.
    """
    js = student_data_opener(test_file_path)
    students_emails = list(js["students"].keys())
    students = []
    for email in students_emails:
        student = student_data_importer_helper(js, email)
        students.append(student)
    return students


class TestConstructVector(unittest.TestCase):
    """Test vector construction for Student objects."""
    
    def test_normal_case(self):
        """Test vector construction with normal values."""
        try:
            student = Student(
                first_name="test",
                email="test",
                skill_level=1,  # ok
                ambition=1,  # ambitious
                role=1,  # follower
                teamwork_style=1,  # offline_meeting
                pace=1,  # finish_late
                backgrounds={1},  # Finance
                backgrounds_preference=1,  # different
                hobbies={1, 2, 3},
                project_summary="test"
            )
            vector_have, vector_want = student.construct_vector()
        except Exception as e:
            self.fail(f"construct_vector() raised Exception unexpectedly! {e}")
        
        # Normalized weights must match Student.construct_vector
        w_skill = CONFIG["skill_level"]["weight"] / math.sqrt(len(CONFIG["skill_level"]["choices"]))
        w_amb = CONFIG["ambition"]["weight"] / math.sqrt(len(CONFIG["ambition"]["choices"]))
        w_role = CONFIG["role"]["weight"] / math.sqrt(len(CONFIG["role"]["choices"]))
        w_style = CONFIG["teamwork_style"]["weight"] / math.sqrt(len(CONFIG["teamwork_style"]["choices"]))
        w_pace = CONFIG["pace"]["weight"] / math.sqrt(len(CONFIG["pace"]["choices"]))
        w_bg = CONFIG["backgrounds"]["weight"] / math.sqrt(len(CONFIG["backgrounds"]["choices"]))
        w_hobby = CONFIG["hobbies"]["weight"] / math.sqrt(len(CONFIG["hobbies"]["choices"]))

        exp_vector_have = np.concatenate((
            np.array([0, 1, 0]) * w_skill,  # skill_level
            np.array([0, 1]) * w_amb,        # ambition
            np.array([0, 1]) * w_role,       # role
            np.array([0, 1, 0]) * w_style,   # teamwork_style
            np.array([0, 1, 0]) * w_pace,    # pace
            np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]) * w_bg,  # backgrounds
            np.array([0, 1, 1, 1, 0, 0, 0]) * w_hobby      # hobbies
        ))

        exp_vector_want = np.concatenate((
            np.array([1, 0, 1]) * w_skill,  # skill_level (diversity)
            np.array([0, 1]) * w_amb,       # ambition
            np.array([1, 0]) * w_role,      # role (diversity)
            np.array([0, 1, 0]) * w_style,  # teamwork_style
            np.array([0, 1, 0]) * w_pace,   # pace
            np.array([1, 0, 1, 1, 1, 1, 1, 1, 1]) * w_bg,  # backgrounds (different)
            np.array([0, 1, 1, 1, 0, 0, 0]) * w_hobby      # hobbies
        ))

        np.testing.assert_allclose(vector_have, exp_vector_have, rtol=1e-6, atol=1e-6)
        np.testing.assert_allclose(vector_want, exp_vector_want, rtol=1e-6, atol=1e-6)

    def test_no_pref_case(self):
        """Test vector construction with no preference (None values)."""
        try:
            student = Student(
                first_name="test",
                email="test",
                skill_level=0,  # noob
                ambition=None,  # no_pref
                role=None,  # no_pref
                teamwork_style=None,  # no_pref
                pace=None,  # no_pref
                backgrounds=set(),  # empty set
                backgrounds_preference=None,  # no_pref
                hobbies=set(),  # empty set
                project_summary="test"
            )
            vector_have, vector_want = student.construct_vector()
        except Exception as e:
            self.fail(f"construct_vector() raised Exception unexpectedly! {e}")

        w_skill = CONFIG["skill_level"]["weight"] / math.sqrt(len(CONFIG["skill_level"]["choices"]))
        w_amb = CONFIG["ambition"]["weight"] / math.sqrt(len(CONFIG["ambition"]["choices"]))
        w_role = CONFIG["role"]["weight"] / math.sqrt(len(CONFIG["role"]["choices"]))
        w_style = CONFIG["teamwork_style"]["weight"] / math.sqrt(len(CONFIG["teamwork_style"]["choices"]))
        w_pace = CONFIG["pace"]["weight"] / math.sqrt(len(CONFIG["pace"]["choices"]))
        w_bg = CONFIG["backgrounds"]["weight"] / math.sqrt(len(CONFIG["backgrounds"]["choices"]))
        w_hobby = CONFIG["hobbies"]["weight"] / math.sqrt(len(CONFIG["hobbies"]["choices"]))

        exp_vector_have = np.concatenate((
            np.array([1, 0, 0]) * w_skill,  # skill_level
            np.array([0, 0]) * w_amb,        # ambition none
            np.array([0, 0]) * w_role,       # role none
            np.array([0, 0, 0]) * w_style,   # teamwork_style none
            np.array([0, 0, 0]) * w_pace,    # pace none
            np.array([0, 0, 0, 0, 0, 0, 0, 0, 0]) * w_bg,  # backgrounds none
            np.array([0, 0, 0, 0, 0, 0, 0]) * w_hobby      # hobbies none
        ))

        exp_vector_want = np.concatenate((
            np.array([0, 1, 1]) * w_skill,  # skill wants diversity
            np.array([1, 1]) * w_amb,       # ambition no pref -> any
            np.array([1, 1]) * w_role,      # role no pref -> any
            np.array([1, 1, 1]) * w_style,  # teamwork_style no pref -> any
            np.array([1, 1, 1]) * w_pace,   # pace no pref -> any
            np.array([1, 1, 1, 1, 1, 1, 1, 1, 1]) * w_bg,  # backgrounds no pref -> any
            np.array([1, 1, 1, 1, 1, 1, 1]) * w_hobby      # hobbies no pref -> any
        ))

        np.testing.assert_allclose(vector_have, exp_vector_have, rtol=1e-6, atol=1e-6)
        np.testing.assert_allclose(vector_want, exp_vector_want, rtol=1e-6, atol=1e-6)


class TestMoreStudents(unittest.TestCase):
    """Test vector construction for all students in test data."""
    
    def test_more_students(self):
        """Test that all students from test_user.json can construct vectors."""
        js = student_data_opener("test/test_user.json")
        students_emails = list(js["students"].keys())
        for email in students_emails:
            student = student_data_importer_helper(js, email)
            try:
                student.construct_vector()
            except Exception as e:
                self.fail(f"Failed to construct vector for {email}: {e}")


class TestTeamMatching(unittest.TestCase):
    """Test team matching functionality."""
    
    def test_team_matching(self):
        """Test team matching with test students."""
        students = load_all_test_students_helper("test/test_user.json")
        course = Course(students)
        max_team_size = 3
        course.team_matching(max_size=max_team_size)

        teams = course.teams
        self.assertGreater(len(teams), 0, "Should have at least one team")
        
        # Print teams for debugging
        for index, team in enumerate(teams):
            print(f"-- team {index}:")
            for student in team.students:
                print(f"  {student.first_name} ({student.email})")


if __name__ == '__main__':
    unittest.main()

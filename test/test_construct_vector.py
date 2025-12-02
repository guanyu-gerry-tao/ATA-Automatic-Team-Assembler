import unittest

import numpy as np

from ATA.models import Student, Course
from ATA.config import CONFIG
import json
import math


def student_data_opener(test_file_path: str):
    with open(test_file_path, "r") as f:
        return json.load(f)


def student_data_importer_helper(json_file, email):
    data = json_file["students"][email]
    student = Student(
        student_ip=data.get("student_ip"),
        first_name=data["first_name"],
        email=data["email"],
        skill_level=data["skill_level"],  # ok
        ambition=data["ambition"],  # ambitious
        role=data["role"],  # follower
        teamwork_style=data["teamwork_style"],  # offline_meeting
        pace=data["pace"],  # finish_late
        backgrounds=set(data["backgrounds"]),  # Finance
        backgrounds_preference=data["backgrounds_preference"],  # different
        hobbies=set(data["hobbies"]),  # Outdoor Sports & Fitness/
        project_summary=data["project_summary"],
        other_prompts=data["other_prompts"]
    )
    return student


def load_all_test_students_helper(test_file_path: str):
    js = student_data_opener(test_file_path)
    students_emails = list(js["students"].keys())
    students = []
    for email in students_emails:
        student = student_data_importer_helper(js, email)
        students.append(student)
    return students


class TestConstructVector(unittest.TestCase):
    def test_normal_case(self):
        try:
            student = Student(
                student_ip=None,
                first_name="test",
                email="test",
                skill_level=1,  # ok
                ambition=1,  # ambitious
                role=1,  # follower
                teamwork_style=1,  # offline_meeting
                pace=1,  # finish_late
                backgrounds={1},  # Finance
                backgrounds_preference=1,  # different
                hobbies={1, 2, 3},  # Outdoor Sports & Fitness/
                project_summary="test",
                other_prompts="test"
            )
            vector_have, vector_want = student.construct_vector()
        except:
            self.fail("construct_vector() raised Exception unexpectedly!")
        # normalized weights must match Student.construct_vector
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
        try:
            student = Student(
                student_ip=None,
                first_name="test",
                email="test",
                skill_level=0,  # noob
                ambition=None,  # no_pref
                role=None,  # follower
                teamwork_style=None,  # offline_meeting
                pace=None,  # finish_late
                backgrounds=None,  # Finance
                backgrounds_preference=None,  # different
                hobbies=None,  # Outdoor Sports & Fitness/
                project_summary="test",
                other_prompts="test"
            )
            vector_have, vector_want = student.construct_vector()
        except:
            self.fail("construct_vector() raised Exception unexpectedly!")

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
    def test_more_students(self):
        js = student_data_opener("test/test_user.json")
        students_emails = list(js["students"].keys())
        for email in students_emails:
            student = student_data_importer_helper(js, email)
            student.construct_vector()


class TestTeamMatching(unittest.TestCase):
    def test_team_matching(self):
        students = load_all_test_students_helper("test/test_user.json")
        test_num_of_group = 8
        course = Course(semester=1, course_code="CS5001", num_of_group=test_num_of_group)
        course.add_students(students)
        course.team_matching()

        teams = course.teams
        for index, team in enumerate(teams):
            print(f"-- team {index}:")
            for student in team.students:
                print(student.first_name)


if __name__ == '__main__':
    unittest.main()

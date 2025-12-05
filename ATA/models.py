from ATA.config import CONFIG
import numpy as np
import math


class Student:
    def __init__(self,
                 first_name: str,
                 email: str,
                 skill_level: int,
                 ambition: int,
                 role: int,
                 teamwork_style: int,
                 pace: int,
                 backgrounds: set[int],
                 backgrounds_preference: int,
                 hobbies: set[int],
                 project_summary: str,
                 other_prompts: str,
                 team_id: str = None,
                 ):
        self.team_id = team_id
        self.first_name = first_name
        self.email = email
        self.skill_level = skill_level
        self.ambition = ambition
        self.role = role
        self.teamwork_style = teamwork_style
        self.pace = pace
        self.backgrounds = backgrounds
        self.backgrounds_preference = backgrounds_preference
        self.hobbies = hobbies
        self.project_summary = project_summary
        self.other_prompts = other_prompts
        self.vector_have, self.vector_want = self.construct_vector()


    def get_json(self):
        return {
            "team_id": self.team_id,
            "first_name": self.first_name,
            "email": self.email,
            "skill_level": self.skill_level,
            "ambition": self.ambition,
            "role": self.role,
            "teamwork_style": self.teamwork_style,
            "pace": self.pace,
            "backgrounds": list(self.backgrounds),
            "backgrounds_preference": self.backgrounds_preference,
            "hobbies": list(self.hobbies),
            "project_summary": self.project_summary,
            "other_prompts": self.other_prompts
        }


    def construct_vector(self) -> tuple[np.ndarray, np.ndarray]:
        """
        Using this function to construct a vector for a student
        :param student: object of Student class, directly from student's submitted form (frontend)
        :return: return (vector_have, vector_want)
        """

        vector_have = np.array([])  # init a vector describe this student's property
        vector_want = np.array([])  # init a vector describe what we want from this student

        # to handle skill level
        # handling skill level, we need to consider the diversity of skill level.
        # best case: 1 pro 1 ok 1 noob
        l_skill_level = len(CONFIG["skill_level"]["choices"])  # cardinality of skill level
        w_skill_level = CONFIG["skill_level"]["weight"] / math.sqrt(l_skill_level)  # weight of skill level, normalized
        vector = np.zeros(l_skill_level)  # init a vector with all 0
        vector[self.skill_level] = w_skill_level  # apply value to the index of skill level
        vector_have = np.concatenate((vector_have, vector))  # append to vector_have
        vector_want = np.concatenate((vector_want,
                                      w_skill_level - vector))  # append to vector_want, swap 1 and 0 because that we want diversity of skill level

        # to handle ambition,
        # ambition should match, just_pass matches just_pass, normal matches normal, ambitious matches ambitious
        l_ambition = len(CONFIG["ambition"]["choices"])  # cardinality of ambition choice
        w_ambition = CONFIG["ambition"]["weight"] / math.sqrt(l_ambition)  # weight of ambition, normalized
        vector = np.zeros(l_ambition)  # init a vector with all 0
        if self.ambition is not None:  # if ambition has value, meaning NOT no preference
            vector[self.ambition] = w_ambition  # apply value to the index of ambition
            vector_want = np.concatenate((vector_want, vector))  # append to vector_want
        else:  # if ambition is None, meaning no preference
            vector_want = np.concatenate((vector_want,
                                          w_ambition - vector))  # when no preference, we assume the student wants any kind. so all values are True
        vector_have = np.concatenate((vector_have, vector))  # append to vector_have

        # handle role
        # we want diversity of role
        # and here we allow students to choose "no preference"
        # when student choose "no preference", then the property of student is [0, 0]
        # but also assume the student want any kind, so the want vector is [1, 1]
        l_role = len(CONFIG["role"]["choices"])
        w_role = CONFIG["role"]["weight"] / math.sqrt(l_role)
        vector = np.zeros(l_role)
        if self.role is not None:  # if role has value, meaning NOT no preference
            vector[self.role] = w_role  # apply value to the index of role
        vector_have = np.concatenate((vector_have, vector))  # append to vector_have
        vector_want = np.concatenate((vector_want, w_role - vector))  # append to vector_want
        # NOTE: when has preference, we set student like [1,0] or [0,1], and the want vector is reversed type [0,1] or [1,0]
        #       when no preference, we assume the student wants any kind. so have is [0, 0] and want is [1, 1]

        # handle teamwork style
        # similar to the ambition, we want their style match within team
        l_teamwork_style = len(CONFIG["teamwork_style"]["choices"])
        w_teamwork_style = CONFIG["teamwork_style"]["weight"] / math.sqrt(l_teamwork_style)
        vector = np.zeros(l_teamwork_style)
        if self.teamwork_style is not None:
            vector[self.teamwork_style] = w_teamwork_style
            vector_want = np.concatenate((vector_want, vector))
        else:
            vector_want = np.concatenate((vector_want, w_teamwork_style - vector))
        vector_have = np.concatenate((vector_have, vector))

        # handle pace preference
        # similar to teamwork style, we want their pace match within team
        l_pace = len(CONFIG["pace"]["choices"])
        w_pace = CONFIG["pace"]["weight"] / math.sqrt(l_pace)
        vector = np.zeros(l_pace)
        if self.pace is not None:
            vector[self.pace] = w_pace
            vector_want = np.concatenate((vector_want, vector))
        else:
            vector_want = np.concatenate((vector_want, w_pace - vector))
        vector_have = np.concatenate((vector_have, vector))

        # handle backgrounds
        # backgrounds should match
        # notice, the backgrounds are in a list, so we need a forloop to handle
        # in addition, we allowed student to choose if they want different backgrounds or same backgrounds
        l_backgrounds = len(CONFIG["backgrounds"]["choices"])
        w_backgrounds = CONFIG["backgrounds"]["weight"] / math.sqrt(l_backgrounds)
        vector = np.zeros(l_backgrounds)
        if self.backgrounds:  # the student choose backgrounds
            for background in self.backgrounds:  # use the forloop to handle applying value to the index of backgrounds
                vector[background] = w_backgrounds
            if self.backgrounds_preference == 1:  # 1=different, means the student want different backgrounds
                vector_want = np.concatenate((vector_want, w_backgrounds - vector))  # swap 1 and 0
            else:  # 0=same, means the student want the same backgrounds
                vector_want = np.concatenate((vector_want, vector))  # apply same as the student's property
        else:  # the student choose no backgrounds
            vector_want = np.concatenate((vector_want,
                                          w_backgrounds - vector))  # when no preference, we assume the student wants any kind. so all values are 1
        vector_have = np.concatenate((vector_have, vector))  # append to vector_have

        # handle hobby
        # similar to backgrounds, we want their hobby match
        # and hobbies are in a list, so we need a forloop to handle
        # students are allowed to choose no hobbies, so we need to handle that case
        # however, we directly assume students want same hobby.
        l_hobbies = len(CONFIG["hobbies"]["choices"])
        w_hobbies = CONFIG["hobbies"]["weight"] / math.sqrt(l_hobbies)
        vector = np.zeros(l_hobbies)
        if self.hobbies:
            for hobby in self.hobbies:
                vector[hobby] = w_hobbies
            vector_want = np.concatenate((vector_want, vector))
        else:
            vector_want = np.concatenate((vector_want, w_hobbies - vector))
        vector_have = np.concatenate((vector_have, vector))

        return vector_have, vector_want  # return


class Team:
    def __init__(self, team_id: str, students: list[Student]):
        self.team_id = team_id
        self.students = students
        # Set team_id for all students in the team
        for student in students:
            student.team_id = team_id
        self.vector_have, self.vector_want = np.array([]), np.array([])
        self.__generate_have_want()
        self.score_matrix_with_rest_of_students = np.array([])
        self.list_mutual_crush_score_with_rest_of_students = []
        self.mutual_crush_score_with_rest_of_students(self.students)
        self.AI_suggestion = ""

    def get_json(self):
        return {
            "team_id": self.team_id,
            "students": [student.get_json() for student in self.students],
            "vector_have": self.vector_have.tolist(),
            "vector_want": self.vector_want.tolist(),
            "score_matrix_with_rest_of_students": self.score_matrix_with_rest_of_students.tolist(),
            "list_mutual_crush_score_with_rest_of_students": self.list_mutual_crush_score_with_rest_of_students,
            "AI_suggestion": self.AI_suggestion
        }

    def add_student(self, student: Student):
        '''
        add student to the team
        :param student:
        :return:
        '''
        self.students.append(student)
        # Set team_id for the student
        student.team_id = self.team_id
        self.__generate_have_want()  # recalculate the have and want vector
        self.mutual_crush_score_with_rest_of_students(self.students)  # recalculate the mutual crush score

    def __generate_have_want(self):
        '''
        Generate the have and want vector for the team
        :return:
        '''
        if len(self.students) > 0:  # handle the case when there is at least one student in the team
            list_of_have = [student.vector_have for student in self.students]  # init a list of have vector for each student
            list_of_want = [student.vector_want for student in self.students]  # init a list of want vector for each student
            self.vector_have = np.add.reduce(list_of_have) / len(list_of_have)  # average have vector
            self.want = np.add.reduce(list_of_want) / len(list_of_want)  # average want vector
        else:  # handle the case when there is no student in the team
            self.vector_have = np.array([])  # set have vector to be empty
            self.vector_want = np.array([])  # set want vector to be empty

    def mutual_crush_score_with_rest_of_students(self, students_not_in_team: list[Student]):
        '''
        Generate the mutual crush score for the team. This is a private function.
        This function requires a list of students who are not in the team: because we only care students not in the team, so we can decide who to be added to the team later.
        :param students_not_in_team: input the students who are not in the team
        :return:
        '''
        self.list_mutual_crush_score_with_rest_of_students = []  # init an empty list
        for student in students_not_in_team:
            score_be_like = np.dot(self.vector_have, student.vector_want)
            score_like = np.dot(self.want, student.vector_have)
            score = (score_be_like + score_like) / 2
            self.list_mutual_crush_score_with_rest_of_students.append((student, score))
        self.list_mutual_crush_score_with_rest_of_students.sort(key=lambda x: x[1])  # sort based on the score, highest score last


class Course:
    def __init__(self, students: list[Student]):
        self.students = self.add_students(students) if students else []
        self.teams = []
        self.array_of_have, self.array_of_want = np.array([]), np.array([])
        self.score_matrix = np.array([])
        self.mutual_crush_score_list = []
        self.student_not_in_team = []

    def get_student_by_email(self, email: str) -> Student:
        for student in self.students:
            if student.email == email:
                return student
        else:
            raise ValueError("Student not found")

    def get_team_by_team_id(self, team_id: str) -> Team:
        for team in self.teams:
            if team.team_id == team_id:
                return team
        else:
            raise ValueError("Team not found")

    def add_students(self, students: list[Student]):
        '''
        This function can add multiple students at once
        :param students: new students instances to be added
        :return:
        '''
        for student in students:
            self.students.append(student)  # add student obj to the students list
            self.student_not_in_team.append(
                student)  # add student obj to the student_not_in_team list. Assuming new students are not in team.
        self.__generate_have_want_arrays()  # generate array_of_have and array_of_want after each time new students are added
        self.__crush_matrix()  # calculate the score matrix after each time new students are added
        self.__mutual_crush_score()  # calculate the mutual crush score list after each time new students are added

    def update_student(self, new_student: Student):
        '''
        Update an existing student's information by email. If student doesn't exist, add them.
        :param new_student: Student instance with updated information
        :return:
        '''
        try:
            existing_student = self.get_student_by_email(new_student.email)
            # Preserve team_id if student is already in a team
            new_student.team_id = existing_student.team_id
            
            # Update the student in the students list
            student_index = self.students.index(existing_student)
            self.students[student_index] = new_student
            
            # Update in student_not_in_team list if applicable
            if existing_student in self.student_not_in_team:
                not_in_team_index = self.student_not_in_team.index(existing_student)
                if new_student.team_id is None:
                    self.student_not_in_team[not_in_team_index] = new_student
                else:
                    # If student has a team_id, remove from not_in_team list
                    self.student_not_in_team.remove(existing_student)
            
            # If student is in a team, update the team's student reference
            if existing_student.team_id is not None:
                team = self.get_team_by_team_id(existing_student.team_id)
                team_index = team.students.index(existing_student)
                team.students[team_index] = new_student
                team.__generate_have_want()  # Recalculate team vectors
            
        except ValueError:
            # Student doesn't exist, add as new student
            self.add_students([new_student])
            return
        
        # Recalculate all arrays and matrices after update
        self.__generate_have_want_arrays()
        self.__crush_matrix()
        self.__mutual_crush_score()

    def add_team(self, team: Team):
        '''
        This function can add a team.
        :param team: a new team instance to be added
        :return:
        '''
        self.teams.append(team)

    def add_student_to_team(self, student: Student, team: Team):
        '''
        add student to the team
        :param student: instance the student to be added to the team
        :param team: the team the student will be added to
        :return:
        '''
        team.add_student(student)
        self.student_not_in_team.remove(student)  # remove student from student_not_in_team list

    def __generate_have_want_arrays(self):
        array_have = []
        array_want = []
        for student in self.students:
            array_have.append(student.vector_have)
            array_want.append(student.vector_want)
        self.array_of_have, self.array_of_want = np.array(array_have), np.array(array_want)

    def __crush_matrix(self):
        '''
        This function calculates the score matrix based on the have and want vectors
        The matrix shows single direction favorite of one student over the other
        :return:
        '''
        score_matrix = self.array_of_have @ self.array_of_want.T
        # AI prompt:
        # I asked how to calculate the dot product of two vectors, AI suggests "@"
        # Also asked why the second argument needs ".T"

        np.fill_diagonal(score_matrix, 0)  # never match with self

        max_score = score_matrix.max()  # normalize the value, find the largest value first
        if max_score > 0:
            score_matrix = score_matrix / max_score  # normalize each value

        self.score_matrix = score_matrix

    def __mutual_crush_score(self):
        '''
        This function calculates the mutual crush score for each student pair
        :return:
        '''
        n = self.score_matrix.shape[0]
        mutual_crush_score_list = []
        # here is the typical 2-forloop
        for i in range(n):
            for j in range(i + 1, n):
                mutual_crush_score_list.append(
                    (self.students[i], self.students[j], (self.score_matrix[i, j] + self.score_matrix[j, i]) / 2))
        # sort based on the score, we need to find the largest score, make it as team's core first
        mutual_crush_score_list.sort(key=lambda x: x[2])
        self.mutual_crush_score_list = mutual_crush_score_list

    def team_matching(self, max_size: int = 3):
        '''
        This is the actual team matching algorithm.
        '''
        if len(self.students) == 0:
            raise ValueError("No students to match")
        num_of_group = math.ceil(len(self.students) / max_size)
        if num_of_group > len(self.students):  # handle the case when number of group is larger than number of students
            raise ValueError("Number of group is larger than number of students")

        # First round of matching, just match two students a team at a time as team's core
        k = 0  # init a counter
        while k < num_of_group:  # while there are still teams left to be formed
            if len(self.student_not_in_team) + len(self.teams) == num_of_group:
                # meaning we have enough teams, however there are still single students left.
                # it is because number of teams is smaller than 2x number of students.
                # so there are partial students formed team, the rest students form as a team as single
                while self.student_not_in_team:
                    student = self.student_not_in_team.pop()
                    self.teams.append(Team(str(len(self.teams) + 1), [student]))
                break

            # current team is a two-student pair
            current_team = self.mutual_crush_score_list.pop()
            # if both students are not in team, then add them to the team.
            # else, start the next round of matching.
            if current_team[0] in self.student_not_in_team and current_team[1] in self.student_not_in_team:
                self.student_not_in_team.remove(current_team[0])
                self.student_not_in_team.remove(current_team[1])
                self.teams.append(Team(str(len(self.teams) + 1), [current_team[0], current_team[1]]))
                k += 1

        # rest rounds of matching, by forloop each team.
        # the algorithm is to find best matching student for each team, then add the student to the team.
        while self.student_not_in_team:  # until all students are matched
            for team in self.teams:  # roll through each team
                if not self.student_not_in_team:  # if there is no student left to be matched, then break the forloop, in case not in team students drain out during one round of matching
                    break
                team.mutual_crush_score_with_rest_of_students(self.student_not_in_team)  # recalculate the mutual crush score with the rest of students
                like_list = team.list_mutual_crush_score_with_rest_of_students[:]  # copy the list
                if like_list:  # if there is at least one student left to be matched, then add the student to the team
                    most_matching_student = like_list.pop()[0]  # get the student with the highest mutual crush score. [0] is the student obj, [1] is the score. We only need the student obj.
                    while like_list and most_matching_student not in self.student_not_in_team:  # until all students are matched, keep popping the student with the highest score. Also make sure the student is not in team.
                        most_matching_student = like_list.pop()[0]  # get the student with the highest mutual crush score. This loop will run until we find a student who is not in team.
                    if most_matching_student in self.student_not_in_team:  # if we find a student who is not in team, then add the student to the team
                        team.add_student(most_matching_student)
                        self.student_not_in_team.remove(most_matching_student)

        # Ensure all students have team_id set (in case of any missed assignments)
        for team in self.teams:
            for student in team.students:
                if student.team_id != team.team_id:
                    student.team_id = team.team_id

    def print_result(self):
        for team in self.teams:
            print(f"Team {team.team_id}:")
            for student in team.students:
                print(f"  {student.first_name} - {student.email}")
            print()

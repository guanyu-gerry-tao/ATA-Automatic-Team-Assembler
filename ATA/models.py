from ATA.config import CONFIG
import numpy as np
import math


class Student:
    """Represents a student with their preferences and attributes for team matching.
    
    Each student has various attributes (skill level, ambition, role, etc.) that are
    converted into vector representations for matching with other students.
    """
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
                 team_id: str = None,
                 ):
        """Initialize a Student instance.
        
        Args:
            first_name: Student's first name.
            email: Student's email address (used as unique identifier).
            skill_level: Skill level index (0=noob, 1=ok, 2=pro).
            ambition: Ambition level index (0=just_pass, 1=ambitious, None=no preference).
            role: Preferred role index (0=leader, 1=follower, None=no preference).
            teamwork_style: Teamwork style index (0=online_meeting, 1=offline_meeting, 2=divide_and_conquer, None=no preference).
            pace: Work pace preference index (0=finish_early, 1=finish_late, 2=little_by_little, None=no preference).
            backgrounds: Set of background indices the student has.
            backgrounds_preference: Preference for backgrounds (0=same, 1=different).
            hobbies: Set of hobby indices the student has.
            project_summary: Description of the project the student wants to work on.
            team_id: Optional team ID if student is already assigned to a team.
        """
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
            "project_summary": self.project_summary
        }


    def construct_vector(self) -> tuple[np.ndarray, np.ndarray]:
        """Construct feature vectors for team matching.
        
        Creates two vectors:
        - vector_have: Represents the student's attributes/preferences
        - vector_want: Represents what the student wants in teammates
        
        The vectors are normalized and weighted according to CONFIG settings.
        Different attributes have different matching strategies:
        - Skill level: Diversity preferred (want different skill levels)
        - Ambition: Matching preferred (want similar ambition)
        - Role: Diversity preferred (want different roles)
        - Teamwork style: Matching preferred (want similar style)
        - Pace: Matching preferred (want similar pace)
        - Backgrounds: Can prefer same or different based on preference
        - Hobbies: Matching preferred (want similar hobbies)
        
        Returns:
            Tuple of (vector_have, vector_want) as numpy arrays.
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
    """Represents a team of students.
    
    A team contains multiple students and maintains aggregate vectors representing
    the team's collective attributes and preferences for matching with other students.
    """
    
    def __init__(self, team_id: str, students: list[Student]):
        """Initialize a Team instance.
        
        Args:
            team_id: Unique identifier for the team.
            students: List of Student objects in this team.
        """
        self.team_id = team_id  # unique identifier for this team
        self.students = students  # list of Student objects in this team
        
        # Set team_id for all students in the team
        # ensure every student knows which team they belong to
        for student in students:
            student.team_id = team_id
        
        # Initialize team vectors (aggregate of all students' vectors)
        self.vector_have, self.vector_want = np.array([]), np.array([])
        self.__generate_have_want()  # calculate aggregate vectors from students
        
        # Initialize score tracking for matching with other students
        self.score_matrix_with_rest_of_students = np.array([])  # matrix of compatibility scores
        self.list_mutual_crush_score_with_rest_of_students = []  # list of (student, score) tuples
        
        # Calculate initial compatibility scores with all students
        # pass empty list since all students are already in this team initially
        self.mutual_crush_score_with_rest_of_students(self.students)
        self.AI_suggestion = ""  # placeholder for future AI-generated team suggestions

    def get_json(self):
        """Convert team data to JSON-serializable dictionary.
        
        Returns:
            Dictionary containing team ID, students, vectors, and scores.
        """
        return {
            "team_id": self.team_id,  # team identifier
            "students": [student.get_json() for student in self.students],  # list of student dictionaries
            "vector_have": self.vector_have.tolist(),  # convert numpy array to list for JSON
            "vector_want": self.vector_want.tolist(),  # convert numpy array to list for JSON
            "score_matrix_with_rest_of_students": self.score_matrix_with_rest_of_students.tolist(),  # compatibility scores matrix
            "list_mutual_crush_score_with_rest_of_students": self.list_mutual_crush_score_with_rest_of_students,  # sorted list of (student, score) tuples
            "AI_suggestion": self.AI_suggestion  # AI-generated team analysis
        }

    def add_student(self, student: Student):
        """Add a student to the team.
        
        Updates the student's team_id and recalculates team vectors and scores.
        
        Args:
            student: Student object to add to the team.
        """
        self.students.append(student)  # add student to the team's student list
        
        # Set team_id for the student
        # ensure the student knows they belong to this team
        student.team_id = self.team_id
        
        # Recalculate team vectors since team composition changed
        self.__generate_have_want()  # recalculate the have and want vector
        
        # Recalculate compatibility scores with students not in team
        # pass current students list (will filter internally)
        self.mutual_crush_score_with_rest_of_students(self.students)  # recalculate the mutual crush score

    def __generate_have_want(self):
        """Generate aggregate have and want vectors for the team.
        
        Calculates the average of all students' vectors to represent the team's
        collective attributes and preferences.
        """
        # Generate aggregate vectors by averaging all students' individual vectors
        if len(self.students) > 0:  # handle the case when there is at least one student in the team
            # Collect all students' have vectors into a list
            list_of_have = [student.vector_have for student in self.students]  # init a list of have vector for each student
            
            # Collect all students' want vectors into a list
            list_of_want = [student.vector_want for student in self.students]  # init a list of want vector for each student
            
            # Calculate average have vector (sum all vectors and divide by count)
            self.vector_have = np.add.reduce(list_of_have) / len(list_of_have)  # average have vector
            
            # Calculate average want vector (sum all vectors and divide by count)
            self.want = np.add.reduce(list_of_want) / len(list_of_want)  # average want vector
        else:  # handle the case when there is no student in the team
            # If team is empty, set vectors to empty arrays
            self.vector_have = np.array([])  # set have vector to be empty
            self.vector_want = np.array([])  # set want vector to be empty

    def mutual_crush_score_with_rest_of_students(self, students_not_in_team: list[Student]):
        """Calculate mutual compatibility scores with students not in the team.
        
        For each student not in the team, calculates a bidirectional compatibility score:
        - score_be_like: How much the team matches what the student wants
        - score_like: How much the student matches what the team wants
        - Final score: Average of both directions
        
        Results are stored in list_mutual_crush_score_with_rest_of_students,
        sorted by score (lowest to highest).
        
        Args:
            students_not_in_team: List of Student objects not currently in this team.
        """
        # Calculate bidirectional compatibility score for each student not in team
        self.list_mutual_crush_score_with_rest_of_students = []  # init an empty list
        
        for student in students_not_in_team:
            # Calculate how well the team matches what this student wants
            score_be_like = np.dot(self.vector_have, student.vector_want)  # team attributes match student's preferences
            
            # Calculate how well this student matches what the team wants
            score_like = np.dot(self.want, student.vector_have)  # student attributes match team's preferences
            
            # Final score is average of both directions (mutual compatibility)
            score = (score_be_like + score_like) / 2
            
            # Store the student and their compatibility score
            self.list_mutual_crush_score_with_rest_of_students.append((student, score))
        
        # Sort by score (lowest to highest) so best matches are at the end
        self.list_mutual_crush_score_with_rest_of_students.sort(key=lambda x: x[1])  # sort based on the score, highest score last


class Course:
    """Manages all students and teams for a course.
    
    The Course class handles student management, team formation, and matching algorithms.
    It maintains data structures for efficient team matching calculations.
    """
    
    def __init__(self, students: list[Student]):
        """Initialize a Course instance.
        
        Args:
            students: Optional list of Student objects to initialize the course with.
        """
        # Initialize empty data structures
        self.students = []  # list of all Student objects in the course
        self.teams = []  # list of all Team objects formed
        self.array_of_have, self.array_of_want = np.array([]), np.array([])  # numpy arrays for efficient matrix operations
        self.score_matrix = np.array([])  # compatibility score matrix between all students
        self.mutual_crush_score_list = []  # list of (student1, student2, score) tuples for all pairs
        self.student_not_in_team = []  # pool of students not yet assigned to any team
        
        # Add initial students if provided
        if students:
            self.add_students(students)

    def get_student_by_email(self, email: str) -> Student:
        """Find a student by their email address.
        
        Args:
            email: Email address to search for.
            
        Returns:
            Student object with matching email.
            
        Raises:
            ValueError: If no student with the given email is found.
        """
        # Search through all students to find matching email
        for student in self.students:
            if student.email == email:  # email is used as unique identifier
                return student
        else:
            raise ValueError("Student not found")  # no student with this email exists

    def get_team_by_team_id(self, team_id: str) -> Team:
        """Find a team by its team ID.
        
        Args:
            team_id: Team ID to search for.
            
        Returns:
            Team object with matching team_id.
            
        Raises:
            ValueError: If no team with the given ID is found.
        """
        # Search through all teams to find matching team_id
        for team in self.teams:
            if team.team_id == team_id:  # team_id is unique identifier
                return team
        else:
            raise ValueError("Team not found")  # no team with this ID exists

    def add_students(self, students: list[Student]):
        """Add multiple students to the course.
        
        New students are added to the students list and the not-in-team pool.
        After adding, all arrays and score matrices are recalculated.
        
        Args:
            students: List of Student objects to add.
        """
        # Add each student to the course
        for student in students:
            self.students.append(student)  # add student obj to the students list
            
            # Add student to not-in-team pool (new students are assumed not in any team)
            self.student_not_in_team.append(
                student)  # add student obj to the student_not_in_team list. Assuming new students are not in team.
        
        # Recalculate all matrices and scores after adding new students
        self.__generate_have_want_arrays()  # generate array_of_have and array_of_want after each time new students are added
        self.__crush_matrix()  # calculate the score matrix after each time new students are added
        self.__mutual_crush_score()  # calculate the mutual crush score list after each time new students are added

    def update_student(self, new_student: Student):
        """Update an existing student's information by email.
        
        If a student with the same email exists, all duplicates are removed and
        replaced with the updated student. If no student exists, the new student
        is added. The student's team_id is preserved if they were already in a team.
        
        Args:
            new_student: Student object with updated information.
        """
        # Find all students with this email (handle duplicates)
        # search through all students to find matches by email
        existing_students = [s for s in self.students if s.email == new_student.email]
        
        if not existing_students:
            # Student doesn't exist, add as new student
            # if no match found, treat as a new student addition
            self.add_students([new_student])
            return
        
        # If student exists, preserve team_id from the first existing student
        # (assuming duplicates should have the same team_id)
        # maintain team assignment if student was already in a team
        first_existing = existing_students[0]
        new_student.team_id = first_existing.team_id  # preserve team assignment
        
        # Remove all existing students with this email (including duplicates)
        # clean up all duplicate entries before adding the updated one
        for existing_student in existing_students:
            # Remove from teams if in a team
            # if student was assigned to a team, remove them from that team
            if existing_student.team_id is not None:
                try:
                    team = self.get_team_by_team_id(existing_student.team_id)  # find the team
                    if existing_student in team.students:
                        team.students.remove(existing_student)  # remove from team's student list
                        # Drop empty teams
                        # if team becomes empty after removal, delete the team
                        if not team.students and team in self.teams:
                            self.teams.remove(team)
                except ValueError:
                    pass  # team not found, continue with removal from other lists
            
            # Remove from main students list and not-in-team list
            # clean up from course's main data structures
            if existing_student in self.students:
                self.students.remove(existing_student)  # remove from students list
            if existing_student in self.student_not_in_team:
                self.student_not_in_team.remove(existing_student)  # remove from not-in-team pool
        
        # Add the updated student
        self.students.append(new_student)  # add updated student to course
        
        # Add to not_in_team list if not in a team
        # place student in appropriate pool based on team assignment
        if new_student.team_id is None:
            self.student_not_in_team.append(new_student)  # add to unassigned pool
        else:
            # If student is in a team, add to that team
            # restore student to their team if they had one
            try:
                team = self.get_team_by_team_id(new_student.team_id)  # find the team
                team.students.append(new_student)  # add student back to team
                team.__generate_have_want()  # Recalculate team vectors
            except ValueError:
                # Team not found, clear team_id and add to not_in_team
                # if team doesn't exist, clear assignment and add to unassigned pool
                new_student.team_id = None
                self.student_not_in_team.append(new_student)
        
        # Recalculate all arrays and matrices after update
        # refresh all compatibility scores since student data changed
        self.__generate_have_want_arrays()  # regenerate student vector arrays
        self.__crush_matrix()  # recalculate compatibility matrix
        self.__mutual_crush_score()  # recalculate mutual crush scores

    def add_team(self, team: Team):
        """Add a team to the course.
        
        Args:
            team: Team object to add.
        """
        # Simply add the team to the teams list
        self.teams.append(team)  # add team to course's teams list

    def add_student_to_team(self, student: Student, team: Team):
        """Add a student to a team.
        
        The student is removed from the not-in-team pool and added to the specified team.
        
        Args:
            student: Student object to add to the team.
            team: Team object to add the student to.
        """
        # Add student to the team (this updates team vectors and scores)
        team.add_student(student)
        
        # Remove student from not-in-team pool since they're now assigned
        self.student_not_in_team.remove(student)  # remove student from student_not_in_team list

    def clear_team_assignments(self):
        """
        Clear all team assignments but keep all students.
        After this call, there will be no teams and all students will be considered 'not in team'.
        """
        # Clear team_id for every student
        # remove team assignment from all students
        for student in self.students:
            student.team_id = None  # reset team assignment

        # Reset teams and not-in-team pool
        self.teams = []  # clear all teams
        self.student_not_in_team = list(self.students)  # all students are now unassigned

        # Recompute arrays and score matrix
        # recalculate all compatibility scores since teams were cleared
        if self.students:
            self.__generate_have_want_arrays()  # regenerate student vector arrays
            self.__crush_matrix()  # recalculate compatibility matrix
            self.__mutual_crush_score()  # recalculate mutual crush scores
        else:
            # If no students, reset all arrays to empty
            self.array_of_have = np.array([])
            self.array_of_want = np.array([])
            self.score_matrix = np.array([])
            self.mutual_crush_score_list = []

    def remove_student_by_email(self, email: str):
        """Completely remove all students with the given email from the course.
        
        Removes all students with matching email from students list, teams, and
        not-in-team pool. Empty teams are automatically removed.
        
        Args:
            email: Email address of the student(s) to remove.
            
        Raises:
            ValueError: If no student with the given email is found.
        """
        # Find all students with this email (in case of duplicates)
        # search through all students to find all matches
        students_to_remove = [s for s in self.students if s.email == email]
        
        if not students_to_remove:
            raise ValueError("Student not found")  # no students match this email
        
        # Remove each matching student
        # iterate through all matches to handle duplicates
        for student in students_to_remove:
            # If the student is in a team, remove from that team
            # clean up team assignment first
            if student.team_id is not None:
                try:
                    team = self.get_team_by_team_id(student.team_id)  # find the team
                    if student in team.students:
                        team.students.remove(student)  # remove student from team
                        # Drop empty teams
                        # if team becomes empty, remove the team entirely
                        if not team.students and team in self.teams:
                            self.teams.remove(team)
                except ValueError:
                    # Team not found – ignore, we'll still remove the student from course lists
                    # if team doesn't exist, continue with removal from other lists
                    pass

            # Remove from main students list and not-in-team list
            # clean up from course's main data structures
            if student in self.students:
                self.students.remove(student)  # remove from students list
            if student in self.student_not_in_team:
                self.student_not_in_team.remove(student)  # remove from not-in-team pool

        # Recompute arrays and score matrix
        # refresh all compatibility scores after student removal
        if self.students:
            # If students remain, recalculate all scores
            self.__generate_have_want_arrays()  # regenerate student vector arrays
            self.__crush_matrix()  # recalculate compatibility matrix
            self.__mutual_crush_score()  # recalculate mutual crush scores
        else:
            # If no students remain, reset all arrays to empty
            self.array_of_have = np.array([])
            self.array_of_want = np.array([])
            self.score_matrix = np.array([])
            self.mutual_crush_score_list = []

    def __generate_have_want_arrays(self):
        """Generate arrays of have and want vectors for all students.
        
        Creates numpy arrays where each row represents a student's vector.
        Used for efficient matrix operations in score calculations.
        """
        # Build arrays where each row is a student's vector
        # this allows efficient matrix operations for score calculations
        array_have = []  # temporary list to collect have vectors
        array_want = []  # temporary list to collect want vectors
        
        # Collect each student's vectors into lists
        for student in self.students:
            array_have.append(student.vector_have)  # add student's have vector
            array_want.append(student.vector_want)  # add student's want vector
        
        # Convert lists to numpy arrays for matrix operations
        self.array_of_have, self.array_of_want = np.array(array_have), np.array(array_want)

    def __crush_matrix(self):
        """Calculate the compatibility score matrix between all students.
        
        The score matrix represents one-way compatibility: how much student A
        matches what student B wants. The matrix is normalized and diagonal is set
        to 0 (students don't match with themselves).
        """
        # Calculate compatibility score matrix using matrix multiplication
        # @ operator performs matrix multiplication (dot product for each pair)
        # .T transposes array_of_want so we get all pairwise combinations
        score_matrix = self.array_of_have @ self.array_of_want.T
        # AI prompt:
        # I asked how to calculate the dot product of two vectors, AI suggests "@"
        # Also asked why the second argument needs ".T"

        # Set diagonal to 0 (students don't match with themselves)
        np.fill_diagonal(score_matrix, 0)  # never match with self

        # Normalize scores to range [0, 1] for easier comparison
        max_score = score_matrix.max()  # normalize the value, find the largest value first
        if max_score > 0:
            score_matrix = score_matrix / max_score  # normalize each value

        self.score_matrix = score_matrix  # store the normalized score matrix

    def __mutual_crush_score(self):
        """Calculate mutual compatibility scores for all student pairs.
        
        For each pair of students, calculates the average of their bidirectional
        compatibility scores. Results are stored in mutual_crush_score_list,
        sorted by score (lowest to highest).
        """
        # Calculate mutual compatibility score for each unique pair of students
        n = self.score_matrix.shape[0]  # number of students
        mutual_crush_score_list = []  # list to store (student1, student2, score) tuples
        
        # Iterate through all unique pairs (avoid duplicates and self-pairs)
        # here is the typical 2-forloop
        for i in range(n):
            for j in range(i + 1, n):  # j starts from i+1 to avoid duplicates
                # Mutual score is average of bidirectional compatibility
                # score_matrix[i, j] = how much i matches what j wants
                # score_matrix[j, i] = how much j matches what i wants
                mutual_score = (self.score_matrix[i, j] + self.score_matrix[j, i]) / 2
                mutual_crush_score_list.append(
                    (self.students[i], self.students[j], mutual_score))
        
        # Sort by score (lowest to highest) so best matches are at the end
        # sort based on the score, we need to find the largest score, make it as team's core first
        mutual_crush_score_list.sort(key=lambda x: x[2])  # sort by score (third element)
        self.mutual_crush_score_list = mutual_crush_score_list

    def team_matching(self, max_size: int = 3):
        """Run the team matching algorithm to form teams.
        
        The algorithm works in multiple rounds:
        1. Reset all team assignments and recalculate scores
        2. First round: Form team cores (pairs) based on highest mutual crush scores
        3. Subsequent rounds: Add remaining students to teams based on team-student compatibility
        
        Args:
            max_size: Maximum number of students per team.
            
        Raises:
            ValueError: If there are no students to match, or if number of groups
                        exceeds number of students.
        """
        if len(self.students) == 0:
            raise ValueError("No students to match")

        # Always recompute from scratch:
        # 1) clear existing team assignments
        # 2) treat all students as not-in-team
        for student in self.students:
            student.team_id = None
        self.teams = []
        self.student_not_in_team = list(self.students)

        # Recompute arrays and mutual crush scores for the full student set
        self.__generate_have_want_arrays()
        self.__crush_matrix()
        self.__mutual_crush_score()

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
        """Print team matching results to console.
        
        Displays each team with its members and their project summaries.
        """
        # Print each team and its members with their project summaries
        for team in self.teams:
            print("----------------------------------------")
            print(f"Team {team.team_id}:")  # print team identifier
            
            # Print each student in the team
            for student in team.students:
                print()  # blank line between students
                print(f"    {student.first_name} - {student.email}")  # student name and email
                print(f"        Project: {student.project_summary}")  # student's project idea
            print()  # blank line between teams

from typing import Dict, List, Optional

from .student import Student
from .instructor import Instructor
from .course import Course
from .enrollment import Enrollment

from utils.enums.grade import Grade


class StudentManagementSystem:
    """
    Manages students, instructors, courses, and enrollments within an educational institution.

    This class provides functionalities to manage students, instructors, and courses, as well as 
    to enroll students in courses and assign grades. It also allows for retrieving information 
    about students and courses, such as which students are enrolled in a specific course and 
    which courses a particular student is enrolled in.

    Attributes:
        students (Dict[str, Student]): A dictionary mapping student IDs to `Student` instances.
        instructors (Dict[str, Instructor]): A dictionary mapping instructor IDs to `Instructor` instances.
        courses (Dict[str, Course]): A dictionary mapping course IDs to `Course` instances.
    """

    def __init__(self) -> None:
        """
        Initializes the StudentManagementSystem with empty dictionaries for students, instructors, and courses.
        """

        self.students: Dict[str, Student] = {}
        self.instructors: Dict[str, Instructor] = {}
        self.courses: Dict[str, Course] = {}

    def add_student(self, student: Student) -> None:
        """
        Adds a new student to the system.

        Args:
            student (Student): The `Student` instance to add.

        Raises:
            ValueError: If a student with the same ID already exists in the system.
        """

        existing_student = self.find_student(id_number=student.id_number)

        if existing_student:
            raise ValueError(
                f"Student with ID {student.id_number} already exists in this management system.")

        # Add the student to the system
        self.students[student.id_number] = student

    def update_student(self, student: Student) -> None:
        """
        Updates an existing student's information.

        Args:
            student (Student): The `Student` instance with updated information.

        Raises:
            KeyError: If no student with the given ID exists in the system.
        """

        existing_student = self.find_student(id_number=student.id_number)

        if existing_student is None:
            raise KeyError(
                f"Student with ID {student.id_number} does not exist and can not be updated in this management system.")

        self.students.update({
            student.id_number: student
        })

    def remove_student(self, id_number: str) -> None:
        """
        Removes a student from the system by their ID.

        Args:
            student_id (str): The unique identifier of the student to remove.

        Raises:
            KeyError: If no student with the given ID exists in the system.
        """

        student = self.students.pop(id_number, None)

        if student is None:
            raise KeyError(
                f"Student with ID {id_number} does not exist.")

        # Remove student from enrolled_students attribute of all course in courses and update the course in courses
        for course in self.courses.values():
            enrolled_student = course.find_enrolled_student(
                id_number=id_number)

            if enrolled_student:
                course.remove_student(id_number=id_number)
                self.update_course(course=course)

    def find_student(self, id_number: str) -> Optional[Student]:
        """
        Finds a student in the system by their unique ID number.

        This method searches for a student using their ID number in the 
        students dictionary and returns the corresponding `Student` instance 
        if found.

        Args:
            id_number (str): The unique identifier of the student to find.

        Returns:
            Optional[Student]: The `Student` instance if the student is found; 
            otherwise, `None`.
        """

        student = self.students.get(id_number, None)
        return student

    def add_instructor(self, instructor: Instructor) -> None:
        """
        Adds a new instructor to the system.

        This method registers a new instructor in the `StudentManagementSystem`. If an instructor 
        with the same ID already exists, it raises a `ValueError` to prevent duplication.

        Args:
            instructor (Instructor): The `Instructor` instance to add.

        Raises:
            ValueError: If an instructor with the same ID already exists in the system.
        """

        existing_instructor = self.find_instructor(
            id_number=instructor.id_number)

        if existing_instructor:
            raise ValueError(
                f"Instructor with ID {instructor.id_number} already exists in this management system.")

        # Add the instructor in the system
        self.instructors[instructor.id_number] = instructor

    def update_instructor(self, instructor: Instructor) -> None:
        """
        Updates an existing instructor's information in the system.

        If an instructor with the given ID exists in the system, their information 
        will be updated with the details provided in the `Instructor` instance.

        Args:
            instructor (Instructor): The `Instructor` instance with updated information.

        Raises:
            KeyError: If no instructor with the given ID exists in the system.
        """

        existing_instructor = self.find_instructor(
            id_number=instructor.id_number)

        if existing_instructor is None:
            raise KeyError(
                f"Instructor with ID {instructor.id_number} does not exist and can not be updated in this management system.")

        self.instructors.update({
            instructor.id_number: instructor
        })

        # Update instructor in instructors attribute of all course in courses and update the course in courses
        for course in self.courses.values():
            course_instructor = course.find_instructor(
                id_number=instructor.id_number)

            if course_instructor:
                course.update_instructor(instructor=instructor)
                self.update_course(course=course)

    def remove_instructor(self, id_number: str) -> None:
        """
        Removes an instructor from the system by their ID.

        Args:
            id_number (str): The unique identifier of the instructor to remove.

        Raises:
            KeyError: If no instructor with the given ID exists in the system.
        """

        instructor = self.instructors.pop(id_number, None)

        if instructor is None:
            raise KeyError(
                f"Instructor with ID {id_number} does not exist.")

        # Remove instructor from instructors attribute in all course in courses
        for course in self.courses.values():
            course_instructor = course.find_instructor(id_number)

            if course_instructor:
                course.remove_instructor(id_number=id_number)
                self.update_course(course=course)

    def find_instructor(self, id_number: str) -> Optional[Instructor]:
        """
        Finds and returns an instructor by their unique ID number.

        Args:
            id_number (str): The unique identifier of the instructor to find.

        Returns:
            Optional[Instructor]: The `Instructor` instance if found, otherwise `None`.

        Example:
            >>> sms = StudentManagementSystem()
            >>> instructor = sms.find_instructor("INS-4d5619d5")
            >>> if instructor:
            ...     print(f"Instructor Name: {instructor.name}")
            ... else:
            ...     print("Instructor not found.")
        """

        instructor = self.instructors.get(id_number, None)
        return instructor

    def add_course(self, course: Course) -> None:
        """
        Adds a new course to the system.

        Args:
            course (Course): The `Course` instance to add.

        Raises:
            ValueError: If a course with the same ID already exists in the system.
        """

        found_course = self.find_course(course_id=course.course_id)

        if found_course:
            raise ValueError(
                f"Course with ID {course.course_id} already exists in this management system.")

        # Add the course to the system
        self.courses[course.course_id] = course

    def update_course(self, course: Course) -> None:
        """
        Updates an existing course's information.

        Args:
            course (Course): The `Course` instance with updated information.

        Raises:
            KeyError: If no course with the given ID exists in the system.
        """

        found_course = self.find_course(course_id=course.course_id)

        if found_course is None:
            raise KeyError(
                f"Course with ID {course.course_id} does not exist and can not be updated in this management system.")

        # Update the course in the system
        self.courses.update({
            course.course_id: course
        })

    def remove_course(self, course_id: str) -> None:
        """
        Removes a course from the system by its ID.

        Args:
            course_id (str): The unique identifier of the course to remove.

        Raises:
            KeyError: If no course with the given ID exists in the system.
        """

        course = self.courses.pop(course_id, None)

        if course is None:
            raise KeyError(
                f"Course with ID {course_id}, does not exist in this management system.")

    def find_course(self, course_id: str) -> Optional[Course]:
        """
        Finds a course by its unique identifier in the system.

        Args:
            course_id (str): The unique identifier of the course to find.

        Returns:
            Optional[Course]: The `Course` instance if found; otherwise, `None`.

        Example:
            >>> sms = StudentManagementSystem()
            >>> course = Course(course_name_id=CourseNameId.INTRO_TO_PROGRAMMING)
            >>> sms.add_course(course)
            >>> course = sms.find_course(course.course_id)
            >>> print(course.course_name)
            Introduction to Programming
        """

        course = self.courses.get(course_id, None)
        return course

    def enroll_student(self, id_number: str, course_id: str) -> None:
        """
        Enrolls a student in a specific course.

        Args:
            student_id (str): The unique identifier of the student to enroll.
            course_id (str): The unique identifier of the course.

        Raises:
            KeyError: If the student does not exist in the system.
            KeyError: If the course does not exist in the system.
        """

        student = self.find_student(id_number=id_number)
        course = self.find_course(course_id=course_id)

        if student is None:
            raise KeyError(
                f"Student with ID {id_number} does not exist and can not be enrolled in this management system.")

        if course is None:
            raise KeyError(
                f"Course with ID {course_id} does not exist in this management system. Student with ID {id_number} was not enrolled.")

        # Create the enrollment of the student
        enrollment = Enrollment(id_number=id_number, course_id=course_id)

        # Enroll the student in the course
        course.add_student(enrollment=enrollment)

        # Update the course in the system
        self.update_course(course=course)

    def grade_student(self, id_number: str, course_id: str, grade: Grade) -> None:
        """
        Assigns a grade to a student for a specific course.

        Args:
            student_id (str): The unique identifier of the student.
            course_id (str): The unique identifier of the course.
            grade (float): The grade to assign.

        Raises:
            KeyError: If the student or course does not exist in the system.
            ValueError: If the student is not enrolled in the course.
        """

        student = self.find_student(id_number=id_number)
        course = self.find_course(course_id=course_id)

        if student is None:
            raise KeyError(
                f"Student with ID {id_number} does not exist and can not be assigned a grade in this management system.")

        if course is None:
            raise KeyError(
                f"Course with ID {course_id} does not exist in this management system. Student with ID {id_number} was not assigned a grade.")

        # Find enrolled student in the course
        enrolled_student = course.find_enrolled_student(id_number=id_number)

        if enrolled_student is None:
            raise ValueError(
                f"Student with ID {id_number}, is not enrolled in this course: {course.enrolled_students}. Grade was not assigned.")

        # Assign a grade and update the student enrollment in the course
        enrolled_student.assign_grade(grade=grade)
        course.update_student(enrollment=enrolled_student)

        # Update the course in the system
        self.update_course(course=course)

    def find_course_enrollments(self, course_id: str) -> Dict[str, Enrollment]:
        """
        Retrieves a dictionary of students enrolled in a specific course, including their enrollment details.        

        Args:
            course_id (str): The unique identifier of the course for which enrollments are being retrieved.

        Returns:
            Dict[str, Enrollment]: A dictionary where the keys are student IDs and the values are `Enrollment` instances.

        Raises:
            KeyError: If no course with the given ID exists in the system.

        Notes:
            This method returns a dictionary mapping student IDs to their corresponding `Enrollment` instances 
            for a given course. It provides a robust way to access not just the list of students, but also their 
            associated enrollment information, such as grades or other enrollment-specific attributes.
            For simplicity, doing a list(course_enrollments) is equivalent to the list of students enrolled in the specific course
        """

        course = self.find_course(course_id=course_id)

        if course is None:
            raise KeyError(
                f"Course with ID {course_id} does not exist in this management system.")

        course_enrollments = course.enrolled_students
        return course_enrollments

    def find_course_enrolled_students(self, course_id: str) -> List[str]:
        """
        Retrieves a list of student IDs enrolled in a specific course.

        Args:
            course_id (str): The unique identifier of the course.

        Returns:
            List[str]: A list of student IDs enrolled in the specified course.
        """

        course_enrollments = self.find_course_enrollments(course_id=course_id)

        course_students = list(course_enrollments)
        return course_students

    def find_student_enrollments(self, id_number: str) -> Dict[str, List[Enrollment]]:
        """
        Retrieves a dictionary of enrollments for a specific student.

        Args:
            id_number (str): The unique identifier of the student whose enrollments are to be retrieved.

        Returns:
            Dict[str, List[Enrollment]]: A dictionary where the keys are course IDs and the values are lists 
            of `Enrollment` instances for the specified student.

        Raises:
            KeyError: If no enrollments exist for the student with the given ID.

        Notes:
            This method can be used to obtain a list of enrollments for a student across different courses. 
            Each `Enrollment` instance contains details about the student's participation and grades in each course.

            For all student grades, do [enrollment.grade for enrollment in student_enrollments.get(id_number)]
        """

        student = self.find_student(id_number=id_number)

        if student is None:
            raise KeyError(
                f"Student with ID {id_number} does not exist in this management system.")

        student_enrollments: Dict[str, List[Enrollment]] = {id_number: []}

        for course in self.courses.values():
            enrolled_student = course.find_enrolled_student(
                id_number=id_number)

            if enrolled_student is not None:
                student_enrollments[id_number].append(enrolled_student)

        return student_enrollments

    def find_enrolled_student_courses(self, id_number: str) -> List[str]:
        """
        Retrieves a list of course IDs for which a specific student is enrolled.

        Args:
            id_number (str): The unique identifier of the student.

        Returns:
            List[str]: A list of course IDs that the student is enrolled in.            
        """

        student_enrollments = self.find_student_enrollments(
            id_number=id_number)

        student_courses = [
            enrollment.course_id for enrollment in student_enrollments.get(id_number)]

        return student_courses

    def __str__(self) -> str:
        return f"Student Management System, ©️ 2024. \nMade with 💖 by Gabriel Okundaye"

    def __repr__(self) -> str:
        return self.__str__()

from typing import Dict, Optional

from utils.enums.course_name_id import CourseNameId
from .instructor import Instructor
from .enrollment import Enrollment


class Course:
    """
    Represents a course, including its name, unique identifier, enrolled students, and instructors.

    Attributes:
        course_name (str): The name of the course.
        course_id (str): A unique identifier for the course.
        enrolled_students (Optional[Dict[str, Enrollment]]): A dictionary mapping student IDs to `Enrollment` instances for students enrolled in the course.
        instructors (Optional[Dict[str, Instructor]]): A dictionary mapping instructor IDs to `Instructor` instances for those teaching the course, or None if no instructors are assigned.
    """
    __slots__ = ("course_name", "course_id",
                 "enrolled_students", "instructors")

    def __init__(self, course_name_id: CourseNameId, enrolled_students: Optional[Dict[str, Enrollment]] = None, instructors: Optional[Dict[str, Instructor]] = None) -> None:
        """
        Initializes a Course instance.

        Args:
            course_name_id (CourseNameId): An instance containing both the course name and its unique identifier.
            enrolled_students (Optional[Dict[str, Enrollment]], optional): A dictionary of students enrolled in the course, with student IDs as keys. Defaults to an empty dictionary if not provided.
            instructors (Optional[Dict[str, Instructor]], optional): A dictionary of instructors for the course, with instructor IDs as keys. Defaults to an empty dictionary if not provided.
        """

        self.course_name = course_name_id.course_name
        self.course_id = course_name_id.course_id
        self.enrolled_students = enrolled_students if enrolled_students is not None else {}
        self.instructors = instructors if instructors is not None else {}

    def add_student(self, enrollment: Enrollment) -> None:
        # Check if the student is already enrolled in the course
        enrolled_student = self.find_enrolled_student(
            id_number=enrollment.id_number)

        if enrolled_student:
            raise ValueError(
                f"Student with ID {enrollment.id_number}, is already enrolled in this course: ({self})")

        # Enroll the student in the course
        self.enrolled_students[enrollment.id_number] = enrollment

    def update_student(self, enrollment: Enrollment) -> None:
        enrolled_student = self.find_enrolled_student(
            id_number=enrollment.id_number)

        if enrolled_student is None:
            raise ValueError(
                f"Student with ID {enrollment.id_number}, is not enrolled in this course: ({self})")

        self.enrolled_students.update({
            enrollment.id_number: enrollment
        })

    def remove_student(self, id_number: str) -> None:
        enrolled_student = self.enrolled_students.pop(id_number, None)

        if enrolled_student is None:
            raise Exception(
                f"Student with ID {id_number}, is not enrolled in this course: ({self})")

    def find_enrolled_student(self, id_number: str) -> Optional[Enrollment]:
        enrolled_student = self.enrolled_students.get(id_number, None)
        return enrolled_student

    def add_instructor(self, instructor: Instructor) -> None:
        course_instructor = self.find_instructor(
            id_number=instructor.id_number)

        if course_instructor:
            raise ValueError(
                f"Instructor with ID {instructor.id_number}, is already an instructor for this course: ({self})")

        self.instructors[instructor.id_number] = instructor

    def update_instructor(self, instructor: Instructor) -> None:
        course_instructor = self.find_instructor(
            id_number=instructor.id_number)

        if course_instructor is None:
            raise ValueError(
                f"Instructor with ID {instructor.id_number}, is not an instructor for this course: ({self})")

        self.instructors.update({
            instructor.id_number: instructor
        })

    def remove_instructor(self, id_number: str) -> None:
        instructor = self.instructors.pop(id_number, None)

        if instructor is None:
            raise Exception(
                f"Instructor with ID {id_number}, is not an instructor for this course: ({self})")

    def find_instructor(self, id_number: str) -> Optional[Instructor]:
        instructor = self.instructors.get(id_number, None)
        return instructor

    def __str__(self) -> str:
        """
        Returns a string representation of the course.

        Returns:
            str: A string describing the course, including the course name, course ID, and the number of enrolled students.
        """
        return f"Course(course_name: {self.course_name}, course_id: {self.course_id}, enrolled_students: {self.enrolled_students}, total_students_enrolled: {len(self.enrolled_students)}, instructors: {self.instructors}, total_instructors: {len(self.instructors)})"

    def __repr__(self) -> str:
        return self.__str__()

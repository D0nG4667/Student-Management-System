from typing import List
from sqlmodel import SQLModel, Field, Relationship

from utils.enums.course_name_id import CourseNameId
from .instructor import Instructor
from .enrollment import Enrollment


class Course(SQLModel, table=True):
    """
    Represents a course, including its name, unique identifier, enrolled students, and instructors.

    Attributes:
        id (str): A unique identifier for the course.
        course_name (str): The name of the course.        
        enrolled_students (Dict[str, Enrollment]): A dictionary mapping student IDs to `Enrollment` instances for students enrolled in the course. 
        instructors (Dict[str, Instructor]): A dictionary mapping instructor IDs to `Instructor` instances for those teaching the course, or None if no instructors are assigned.

    Notes:
        Attributes defaults to an empty dictionary using default_factory. This ensures that each instance of the class gets a new dictionary instead of sharing a single instance across all instances of the model.
    """

    id: str = Field(
        default=CourseNameId.INTRO_TO_PROGRAMMING.course_id, primary_key=True)
    course_name: str = Field(
        default=CourseNameId.INTRO_TO_PROGRAMMING.course_name)

    enrollments: List[Enrollment] = Relationship(
        back_populates="course", cascade_delete=True)
    instructors: List[Instructor] = Relationship(back_populates="course")

    def __str__(self) -> str:
        """
        Returns a string representation of the course.

        Returns:
            str: A string describing the course, including the course name, course ID, and the number of enrolled students.
        """
        return f"Course(course_name: {self.course_name}, id: {self.id}, enrolled_students: {self.enrollments}, total_students_enrolled: {len(self.enrollments)}, instructors: {self.instructors}, total_instructors: {len(self.instructors)})"

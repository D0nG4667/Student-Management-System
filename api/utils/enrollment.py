from utils.enums.grade import Grade
import uuid

from sqlmodel import SQLModel, Field, Relationship


class Enrollment(SQLModel, table=True):
    """
    Represents an Enrollment, including the student, the course they are enrolled in, and the assigned grade.

    Attributes:
        id: (int): The enrollment ID
        student_id (str): The ID of the student who is enrolled in the course.
        course_id (str): The ID of the course in which the student is enrolled.
        grade (Grade): The grade assigned to the student for the course. Default if NO_GRADE with enum value of None if no grade has been assigned yet.
    """

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),  # Generates a UUID4 string
        primary_key=True,
        index=True,
        nullable=False,
        sa_column_kwargs={"unique": True}
    )
    student_id: str = Field(foreign_key="student.id")
    course_id: str = Field(foreign_key="course.id")
    grade: Grade = Field(sa_column=Field(sa_type=Grade))

    course: "Course" = Relationship(
        back_populates="enrollments")

    def assign_grade(self, grade: Grade) -> None:
        """
        Assigns a grade to the student for the course.

        Args:
            grade (Grade): The grade to assign to the student.
        """
        self.grade = grade

    def __str__(self) -> str:
        """
        Returns a string representation of the Enrollment.

        Returns:
            str: A description of the enrollment including the student id_number, course_id, and grade.
        """
        return f"Enrollment(student id: {self.student_id}, course: {self.course_id}, grade: {self.grade.value})"

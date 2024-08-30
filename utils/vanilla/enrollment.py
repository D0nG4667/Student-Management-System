from utils.enums.grade import Grade


class Enrollment:
    """
    Represents an Enrollment, including the student, the course they are enrolled in, and the assigned grade.

    Attributes:
        id_number (str): The ID of the student who is enrolled in the course.
        course_id (str): The ID of the course in which the student is enrolled.
        grade (Optional[str]): The grade assigned to the student for the course. Default if NO_GRADE with enum value of None if no grade has been assigned yet.
    """

    __slots__ = ("id_number", "course_id", "grade")

    def __init__(self, id_number: str, course_id: str, grade: Grade = Grade.NO_GRADE) -> None:
        """
        Initializes an Enrollment instance.

        Args:
            id_number (str): The ID of the student enrolled in the course.
            course_id (str): The ID of the course in which the student is enrolled.
            grade (Grade): The grade assigned to the student, initially set to NO_GRADE with enum value of None.
        """
        self.id_number = id_number
        self.course_id = course_id
        self.grade = grade

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
        return f"Enrollment(student id: {self.id_number}, course: {self.course_id}, grade: {self.grade.value})"

    def __repr__(self) -> str:
        return self.__str__()

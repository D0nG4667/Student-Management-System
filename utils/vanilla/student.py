from typing import Optional

from .person import Person
from utils.enums.major import Major


class Student(Person):
    """
    Represents a student, inheriting from the Person class and adding a major.

    Attributes:
        first_name (str): The first name of the student.
        last_name (str): The last name of the student.
        major (Major): The major field of study for the student.
        id_number (Optional[str]): An optional unique identifier for the student. 
            If not provided, a random ID with prefix 'STU' is generated.
    """

    __slots__ = ("first_name", "last_name", "major", "id_number")

    def __init__(self, first_name: str, last_name: str, major: Major, id_number: Optional[str] = None) -> None:
        """
        Initializes a Student instance.

        Args:
            first_name (str): The first name of the student.
            last_name (str): The last name of the student.
            major (str): The major field of study for the student.
            id_number (Optional[str]): An optional unique identifier for the student. 
                If not provided, a random ID with prefix 'STU' is generated.

        Calls:
            super().__init__: Initializes the base Person class with the provided or generated ID.
        """

        super().__init__(first_name, last_name, self.handle_id("STU", id_number))
        self.major = major

    def __str__(self) -> str:
        """
        Returns a string representation of the student.

        Returns:
            str: A description of the student including their name, ID number, and major.
        """
        return f"Student(name: {self.name}, id: {self.id_number}, major: {self.major.value})"

    def __repr__(self) -> str:
        return self.__str__()

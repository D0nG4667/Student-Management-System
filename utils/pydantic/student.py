from pydantic import model_validator
from typing_extensions import Self

from .person import Person
from utils.enums.major import Major


class Student(Person):
    """
    Represents a Student, inheriting from Person, with an additional major field.

    Attributes:
        major (Major): The major that the student is pursuing.

    Methods:
        set_id() -> Self: A Pydantic model validator that automatically sets the student's ID with a "STU" prefix through handle_id method in the Person class.
    """

    major: Major

    @model_validator(mode='after')
    def set_id(self) -> Self:
        self.handle_id(prefix="STU")

        return self

    def __str__(self) -> str:
        """
        Returns a string representation of the student.

        Returns:
            str: A description of the student including their name, ID number, and major.
        """

        return f"Student(name: {self.name}, id: {self.id_number}, major: {self.major.value})"

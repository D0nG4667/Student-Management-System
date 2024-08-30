from typing_extensions import Self
from pydantic import model_validator

from .person import Person
from utils.enums.department import Department


class Instructor(Person):
    """
    Represents an Instructor, inheriting from Person, with an additional department field.

    Attributes:
        department (Department): The  instructor's department.

    Methods:
        set_id() -> Self: A Pydantic model validator that automatically sets the instructor's ID with a "INS" prefix through handle_id method in the Person class.
    """

    department: Department

    @model_validator(mode='after')
    def set_id(self) -> Self:
        self.handle_id(prefix="INS")

        return self

    def __str__(self) -> str:
        """
        Returns a string representation of the instructor.

        Returns:
            str: A description of the instructor including their name, ID number, and department.
        """

        return f"Instructor(name: {self.name}, id: {self.id_number}, department: {self.department.value})"

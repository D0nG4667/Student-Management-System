from typing import Optional

from .person import Person
from utils.enums.department import Department


class Instructor(Person):
    """
    Represents an instructor, inheriting from the Person class and adding a department.

    Attributes:
        first_name (str): The first name of the instructor.
        last_name (str): The last name of the instructor.
        department (Department): The department in which the instructor teaches.
        id_number (Optional[str]): An optional unique identifier for the instructor. 
            If not provided, a random ID with the prefix 'INS' is generated.
    """

    __slots__ = ("first_name", "last_name", "department", "id_number")

    def __init__(self, first_name: str, last_name: str, department: Department, id_number: Optional[str] = None) -> None:
        """
        Initializes an instructor instance.

        Args:
            first_name (str): The first name of the instructor.
            last_name (str): The last name of the instructor.
            department (str): The department in which the instructor teaches.
            id_number (Optional[str]): An optional unique identifier for the instructor. 
                If not provided, a random ID with the prefix 'INS' is generated.

        Calls:
            super().__init__: Initializes the base Person class with the provided first name, last name, 
                              and the generated or provided ID number.
        """

        super().__init__(first_name, last_name, self.handle_id("INS", id_number))
        self.department = department

    def __str__(self) -> str:
        """
        Returns a string representation of the instructor.

        Returns:
            str: A description of the instructor including their name, ID number, and department.
        """
        return f"Instructor(name: {self.name}, id: {self.id_number}, department: {self.department.value})"

    def __repr__(self) -> str:
        return self.__str__()

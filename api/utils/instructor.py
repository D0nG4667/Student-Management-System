from typing_extensions import Self, Optional
from pydantic import model_validator
from sqlmodel import Field, Relationship


from .person import Person
from utils.enums.department import Department


class Instructor(Person, table=True):
    """
    Represents an Instructor, inheriting from Person, with an additional department field.

    Attributes:
        department (Department): The  instructor's department.

    Methods:
        set_id() -> Self: An SQLmodel validator that automatically sets the instructor's ID with a "INS" prefix through handle_id method in the Person class.
    """

    department: Department = Field(sa_column=Field(sa_type=Department))

    course_id: Optional[str] = Field(
        default=None, foreign_key="course.id")
    course: Optional["Course"] = Relationship(
        back_populates="instructors")

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

        return f"Instructor(name: {self.name}, id: {self.id}, department: {self.department})"

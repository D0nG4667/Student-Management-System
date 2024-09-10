import uuid
from typing import Optional
from typing_extensions import Self

from pydantic import model_validator
from sqlmodel import SQLModel, Field


class Person(SQLModel):
    """
    A class representing a person with a first name, last name, and optional ID number.

    Attributes:
        id (str, optional): An optional identifier for the person, generated if not provided.
        first_name (str): The first name of the person.
        last_name (str): The last name of the person.
        name (str, optional): The full name of the person, automatically generated from first and last name.
    """
    id: Optional[str] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    name: Optional[str] = Field(default=None)

    @model_validator(mode='after')
    def set_name(self) -> Self:
        """
        Sets the full name of the person by combining the first and last name.

        Returns:
            Self: The instance with the name attribute set.
        """

        self.name = f"{self.first_name} {self.last_name}"

        return self

    @model_validator(mode='after')
    def set_id(self) -> Self:
        """
        Sets a unique ID for the person if one is not provided.

        Returns:
            Self: The instance with the id attribute set.
        """

        self.handle_id()
        return self

    def handle_id(self, prefix: str = "PER") -> None:
        """
        Generates or returns a unique identifier with a given prefix.

        Args:
            prefix (str): The prefix to be added to the ID.
            id (Optional[str]): An optional ID. If provided, it is returned as-is.

        Returns:
            str: A unique identifier with the given prefix. If no ID is provided, a new ID is generated using UUID.
        """

        # Use id if give else generate id
        if self.id is None or self.id == "":
            # Generate a random UUID and take only the first 8 characters
            short_uuid = str(uuid.uuid4())[:8]

            # Add a custom prefix
            self.id = f"{prefix}-{short_uuid}"

    def __str__(self) -> str:
        """
        Returns a string representation of the person.

        Returns:
            str: A description of the person including their name and ID number.
        """
        return f"Person(name: {self.name}, id: {self.id})"

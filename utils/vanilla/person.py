import uuid
from typing import Optional


class Person:
    """
    Represents a person with a name and an optional unique identifier.

    Attributes:
        name (str): The full name of the person, created from the first and last names.
        id_number (str): A unique identifier for the person. If not provided, a random ID with the 'PER' prefix is generated.
    """

    __slots__ = ("first_name", "last_name", "name", "id_number")

    def __init__(self, first_name: str, last_name: str, id_number: Optional[str]) -> None:
        """
        Initializes a Person instance.

        Args:
            first_name (str): The first name of the person.
            last_name (str): The last name of the person.
            id_number (Optional[str]): An optional unique identifier for the person. 
                If not provided, a random ID with the 'PER' prefix is generated.
        """

        self.name: str = f"{first_name} {last_name}"
        self.id_number = self.handle_id(
            "PER") if not id_number else id_number

    @staticmethod
    def handle_id(prefix: str, id: Optional[str] = None) -> str:
        """
        Generates or returns a unique identifier with a given prefix.

        Args:
            prefix (str): The prefix to be added to the ID.
            id (Optional[str]): An optional ID. If provided, it is returned as-is.

        Returns:
            str: A unique identifier with the given prefix. If no ID is provided, a new ID is generated using UUID.
        """

        if id is None:
            # Generate a random UUID and take only the first 8 characters
            short_uuid = str(uuid.uuid4())[:8]

            # Add the custom prefix
            id = f"{prefix}-{short_uuid}"
        return id

    def __str__(self) -> str:
        """
        Returns a string representation of the person.

        Returns:
            str: A description of the person including their name and ID number.
        """

        return f"Person(name: {self.name}, id: {self.id_number})"

    def __repr__(self) -> str:
        return self.__str__()

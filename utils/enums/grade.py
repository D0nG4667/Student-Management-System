from enum import Enum


class Grade(Enum):
    """
    Enum representing possible letter grades.
    """
    A_PLUS = "A+"
    A = "A"
    A_MINUS = "A-"
    B_PLUS = "B+"
    B = "B"
    B_MINUS = "B-"
    C_PLUS = "C+"
    C = "C"
    C_MINUS = "C-"
    D_PLUS = "D+"
    D = "D"
    D_MINUS = "D-"
    F = "F"
    PASS = "Pass"
    FAIL = "Fail"
    NO_GRADE = None

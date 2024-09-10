from enum import Enum


class CourseNameId(Enum):
    """
    Enum representing various courses with their corresponding IDs.
    """
    INTRO_TO_PROGRAMMING = ("Introduction to Programming", "CS101")
    DATA_STRUCTURES = ("Data Structures", "CS102")
    ALGORITHMS = ("Algorithms", "CS201")
    OPERATING_SYSTEMS = ("Operating Systems", "CS202")
    DATABASE_SYSTEMS = ("Database Systems", "CS301")
    LINEAR_ALGEBRA = ("Linear Algebra", "MATH101")
    CALCULUS = ("Calculus", "MATH102")
    ORGANIC_CHEMISTRY = ("Organic Chemistry", "CHEM101")
    PHYSICS_I = ("Physics I", "PHYS101")
    PHYSICS_II = ("Physics II", "PHYS102")
    MICROECONOMICS = ("Microeconomics", "ECON101")
    MACROECONOMICS = ("Macroeconomics", "ECON102")
    INTRO_TO_PSYCHOLOGY = ("Introduction to Psychology", "PSYCH101")
    SOCIOLOGY_THEORY = ("Sociological Theory", "SOC101")
    AMERICAN_LITERATURE = ("American Literature", "ENGL101")
    WORLD_HISTORY = ("World History", "HIST101")
    CONSTITUTIONAL_LAW = ("Constitutional Law", "LAW101")
    BIOCHEMISTRY = ("Biochemistry", "BIOCHEM101")
    ENGINEERING_MECHANICS = ("Engineering Mechanics", "MECH101")
    ART_HISTORY = ("Art History", "ART101")
    MUSIC_THEORY = ("Music Theory", "MUSIC101")
    ANATOMY = ("Anatomy", "BIO101")

    def __init__(self, course_name: str, course_id: str) -> None:
        self._course_name = course_name
        self._course_id = course_id

    @property
    def course_name(self) -> str:
        return self._course_name

    @property
    def course_id(self) -> str:
        return self._course_id

    def __str__(self) -> str:
        return f"CourseNameId(course_name: {self._course_name}, course_id: {self._course_id})"

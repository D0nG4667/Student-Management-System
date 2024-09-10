from pathlib import Path

# ENV when using standalone uvicorn server running FastAPI in api directory
ENV_PATH = Path("../env/api.env")

ONE_DAY_SEC = 24*60*60

ONE_WEEK_SEC = ONE_DAY_SEC*7

# Cache
USE_REDIS_CACHE = True  # Change to True to use Redis Cache

# Postgres
USE_POSTGRES_DB = True  # Change to True to use Posgres DB


DESCRIPTION = """
This API is the backend of the student management system.\n

Manages students, instructors, courses, and enrollments within an educational institution.\n

Provides functionalities to manage students, instructors, and courses, as well as 
to enroll students in courses and assign grades.\n

- Add, remove, and update students and instructors
- Add, remove, and update courses
- Enroll students in courses
- Assign grades to students for specific courses
- Retrieve a list of students enrolled in a specific course
- Retrieve a list of courses a specific student is enrolled in


### GitHub 
[![GitHub Logo](https://github.com/favicon.ico) D0nG4667](https://github.com/D0nG4667/Student-Management-System)

### Explore this api below
⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️


© 2024, Made with 💖 [Gabriel Okundaye](https://www.linkedin.com/in/dr-gabriel-okundaye) 
"""

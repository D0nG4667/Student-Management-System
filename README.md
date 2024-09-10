# Student-Management-System

<a name="readme-top"></a>

## Project Overview

The goal of this project is to apply the principles of Object-Oriented Programming (OOP) to build a simple Student Management System. This system will allow the management of students, courses, and enrollments, demonstrating the use of classes, objects, inheritance, polymorphism, and encapsulation.

## Description  

A Student Management System showcasing Object-Oriented Programming principles. Includes classes for `Person`, `Student`, `Instructor`, `Course`, and `Enrollment`, with functionalities for managing students, instructors, courses, and enrollments, including adding, updating, and retrieving data as listed below.

- Add, remove, and update students and instructors
- Add, remove, and update courses
- Enroll students in courses
- Assign grades to students for specific courses
- Retrieve a list of students enrolled in a specific course
- Retrieve a list of courses a specific student is enrolled in

**NB:** Person class has a method for generating ID based on the type of person, Instructor INS---, Student STU---

## Sample Code

```sh
    from utils.pydantic.student_management_system import Student, Instructor, Course, StudentManagementSystem

    # Create an instance of the student management system
    sms = StudentManagementSystem()

    # Create the student instance
    student = Student(first_name='Gabriel', last_name='Okundaye',
                      major=Major.COMPUTER_SCIENCE)

    # Create the instructor instance
    instructor = Instructor(first_name='Guido', last_name='Rossum',
                            department=Department.COMPUTER_SCIENCE)

    # Create the course instance
    course = Course(course_name_id=CourseNameId.INTRO_TO_PROGRAMMING)
```

## Technologies Used

- Anaconda
- Python
- Pydantic
- Sqlmodel
- FastAPI
- Docker
- Redis
- PostgreSQL

### FastAPI backend- Demo

[API](https://gabcares-sms-fastapi.hf.space/docs)

## Installation

### Quick install

```bash
 pip install -r requirements.txt
```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 💻 Getting Started

To get a local copy up and running, follow these steps.

### Setup

Clone this repository to your desired folder:

```sh
  cd your-folder
  git clone https://github.com/D0nG4667/Student-Management-System.git
```

Change into the cloned repository

```sh
  cd Student-Management-System
  
```

After cloning this repo,

- Run these commands in the root of the repo to explore the application:

```sh
python app.py

```

### FastAPI Setup

### Prerequisites

- [Docker Desktop](https://docs.docker.com/desktop/)

After cloning this repo,

- Add an env folder in the root of the project.

- Create and env file named `api.env` using this sample

```env
# Redis
REDIS_URL=redis://cache:6379/
REDIS_USERNAME=default

# Postgres
POSTGRES_URL=postgresql+asyncpg://berkely:ucberkely@db:5432/studentmanagement_db
POSTGRES_USER=berkely
POSTGRES_PASSWORD=ucberkely
POSTGRES_DB=studentmanagement_db
```

- Run these commands in the root of the repo to explore the student management API:

```sh
docker-compose pull

docker-compose up --build

```

## Contributions

### How to Contribute

1. Fork the repository and clone it to your local machine.
2. Explore the Jupyter Notebooks and documentation.
3. Implement enhancements, fix bugs, or propose new features.
4. Submit a pull request with your changes, ensuring clear descriptions and documentation.
5. Participate in discussions, provide feedback, and collaborate with the community.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Feedback and Support

Feedback, suggestions, and contributions are welcome! Feel free to open an issue for bug reports, feature requests, or general inquiries. For additional support or questions, you can connect with me on [LinkedIn](https://www.linkedin.com/in/dr-gabriel-okundaye).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 👥 Authors <a name="authors"></a>

🕺🏻**Gabriel Okundaye**

- GitHub: [GitHub Profile](https://github.com/D0nG4667)

- LinkedIn: [LinkedIn Profile](https://www.linkedin.com/in/dr-gabriel-okundaye)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## ⭐️ Show your support <a name="support"></a>

If you like this project kindly show some love, give it a 🌟 **STAR** 🌟. Thank you!

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## 📝 License <a name="license"></a>

This project is [MIT](/LICENSE) licensed.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

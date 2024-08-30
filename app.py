from utils.enums import *

from utils.emojie_support import *


def add_student():
    sms.add_student(student)
    print("Action: Add student")
    return sms.find_student(student.id_number)


def add_instructor():
    sms.add_instructor(instructor)
    print("Action: Add instructor")
    return sms.find_instructor(instructor.id_number)


def add_course():
    sms.add_course(course)
    print("Action: Add course")
    return sms.find_course(course.course_id)


def add_course_instructor():
    found_course = sms.find_course(course.course_id)
    found_course.add_instructor(instructor)
    print("Action: Add course instructor")
    return found_course.find_instructor(instructor.id_number)


def enroll_student():
    sms.enroll_student(student.id_number, course.course_id)
    print("Action: Enroll students in a course")
    return sms.find_course(course.course_id).find_enrolled_student(student.id_number)


def grade_student():
    sms.grade_student(student.id_number, course.course_id, Grade.A_PLUS)
    print("Action: Assign grade to student for specific course")
    return sms.find_course(course.course_id).find_enrolled_student(student.id_number)


def find_student():
    print("Action: Find student")
    return sms.find_student(student.id_number)


def find_course():
    print("Action: Find course")
    return sms.find_course(course.course_id)


def find_course_enrolled_students():
    print("Action: Find list of students enrolled in a specific course")
    return sms.find_course_enrolled_students(course.course_id)


def find_enrolled_student_courses():
    print("Action: Find list of courses a specific student is enrolled in")
    return sms.find_enrolled_student_courses(student.id_number)


# Outline the process in a dictionary
sms_process = {
    "1": add_student,
    "2": add_instructor,
    "3": add_course,
    "4": add_course_instructor,
    "5": enroll_student,
    "6": grade_student,
    "7": find_student,
    "8": find_course,
    "9": find_course_enrolled_students,
    "10": find_enrolled_student_courses,
}


def main():
    print("""
********************************************
👋 Welcome to the Student Management System
********************************************

For the best experience, follow the actions 
sequentially from 1 through 11 to preview the 
result of a process in the system. 
 
💡 Choose an action below: 
 
1. Add student
2. Add instructor
3. Add course
4. Add course instructor
5. Enroll students in a course
6. Assign grades to students for specific courses
7. Find student
8. Find course 
9. Retrieve a list of students enrolled in a specific course
10.Retrieve a list of courses a specific student is enrolled in
11. End program! 

NB:
The system has other CRUD operations like remove 
and update students, instructors and courses that 
can be explored by manually importing and creating 
your own instance of the StudentManagementSystem class
or spinning up the FastAPI.    
   
    """)

    def validate_input(action: str):
        valid = False
        try:
            number = int(action)
            if 1 <= number <= 11:
                valid = True
        except ValueError as e:
            print(e)
        finally:
            return valid

    action = "1"
    while 1 <= int(action) <= 10:
        action = input("What action do you want to perform? \n")

        if action == "11":
            print("Exiting application...\n")
            break

        if validate_input(action):
            try:
                print(f"\n{sms_process.get(action)()}\n")
            except Exception as e:
                print(f"\nOops, an error occured: {e}\n")
        else:
            print(f"\nChoose an action from 1 through 11. Choose 11 to end program.")
            action = "1"

    print(f"Student Management System, ©️ 2024. \nMade with 💖 by Gabriel Okundaye")

    # Restore the default stdout
    sys.stdout = default_stdout


if __name__ == "__main__":
    print(
        """
        Choose a module:
        1. Vanilla
        2. Pydantic
        """
    )

    choice = input("Enter '1' for Vanilla or any other input for Pydantic: ")

    if choice == "1":
        from utils.vanilla.student_management_system import Student, Instructor, Course, StudentManagementSystem
        print("🚀 Vanilla module loaded from utils.vanilla")
    else:
        from utils.pydantic.student_management_system import Student, Instructor, Course, StudentManagementSystem
        print("🚀 Pydantic module loaded from utils.pydantic")

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

    main()

# A program that simulates a school management system, with classes for the students,the teachers, and the courses

class Student:
    def __init__(self, name, student_id):
        self.name = name
        self.student_id = student_id
        self.courses = []

    def enroll(self, course):
        self.courses.append(course)
        print(f"Student {self.name} enrolled in {course.name}.")

    def list_courses(self):
        print(f"Courses for {self.name}:")
        for course in self.courses:
            print(f" - {course.name} (Code: {course.course_code})")


class Teacher:
    def __init__(self, name, teacher_id):
        self.name = name
        self.teacher_id = teacher_id
        self.courses = []

    def assign_course(self, course):
        self.courses.append(course)
        print(f"Teacher {self.name} assigned to course {course.name}.")

    def list_courses(self):
        print(f"Courses taught by {self.name}:")
        for course in self.courses:
            print(f" - {course.name} (Code: {course.course_code})")


class Course:
    def __init__(self, name, course_code):
        self.name = name
        self.course_code = course_code
        self.students = []
        self.teacher = None

    def assign_teacher(self, teacher):
        self.teacher = teacher
        print(f"Course {self.name} assigned to teacher {teacher.name}.")
    
    def enroll_student(self, student):
        self.students.append(student)
        print(f"Student {student.name} enrolled in course {self.name}.")
    
    def list_details(self):
        print(f"Course: {self.name} (Code: {self.course_code})")
        print(f"Teacher: {self.teacher.name if self.teacher else 'None assigned'}")
        print("Students:")
        for student in self.students:
            print(f" - {student.name}")

# Create students
student1 = Student("Alice", "S001")
student2 = Student("Bob", "S002")

# Create teachers
teacher1 = Teacher("Dr. Smith", "T001")
teacher2 = Teacher("Ms. Johnson", "T002")

# Create courses
course1 = Course("Mathematics", "MATH101")
course2 = Course("Science", "SCI102")

# Assign teachers to courses
course1.assign_teacher(teacher1)
course2.assign_teacher(teacher2)
teacher1.assign_course(course1)
teacher2.assign_course(course2)

# Enroll students in courses
course1.enroll_student(student1)
course2.enroll_student(student2)
student1.enroll(course1)
student2.enroll(course2)

# Display details
print("\n-- Course Details --")
course1.list_details()
course2.list_details()
print("\n-- Teacher Details --")
teacher1.list_courses()
teacher2.list_courses()
print("\n-- Student Details --")
student1.list_courses()
student2.list_courses()
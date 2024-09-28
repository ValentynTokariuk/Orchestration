from fastapi import FastAPI, HTTPException, Body, status
from pydantic import BaseModel
from typing import List, Optional
import json

app = FastAPI()

class Course(BaseModel):
    id: int
    title: str
    description: str
    credits: int

class Student(BaseModel):
    id: int
    name: str
    enrolled_courses: List[int] = []

# Initialize courses and students
courses = []
students = []

def load_data():
    global courses, students
    try:
        with open('courses.json', 'r') as file:
            courses = json.load(file)
        with open('students.json', 'r') as file:
            students = json.load(file)
    except FileNotFoundError:
        pass

def save_courses():
    with open('courses.json', 'w') as file:
        json.dump(courses, file, indent=4)

def save_students():
    with open('students.json', 'w') as file:
        json.dump(students, file, indent=4)

load_data()

@app.get("/courses/", response_model=List[Course])
def list_courses():
    return courses

@app.get("/students/", response_model=List[Student])
def list_students():
    return students

@app.post("/courses/bulk", response_model=List[Course], status_code=status.HTTP_201_CREATED)
def create_courses(new_courses: List[Course]):
    global courses
    existing_ids = {course['id'] for course in courses}
    for new_course in new_courses:
        if new_course.id in existing_ids:
            raise HTTPException(status_code=400, detail=f"Duplicate course ID: {new_course.id}")
        courses.append(new_course.dict())
        existing_ids.add(new_course.id)
    save_courses()
    return new_courses

@app.post("/students/bulk", response_model=List[Student], status_code=status.HTTP_201_CREATED)
def create_students(new_students: List[Student]):
    global students
    existing_ids = {student['id'] for student in students}
    for new_student in new_students:
        if new_student.id in existing_ids:
            raise HTTPException(status_code=400, detail=f"Duplicate student ID: {new_student.id}")
        students.append(new_student.dict())
        existing_ids.add(new_student.id)
    save_students()
    return new_students

@app.put("/courses/{course_id}", response_model=Course)
def update_course(course_id: int, course: Course):
    global courses
    for i, existing_course in enumerate(courses):
        if existing_course['id'] == course_id:
            courses[i] = course.dict()
            save_courses()
            return course
    raise HTTPException(status_code=404, detail="Course not found")

@app.put("/students/{student_id}", response_model=Student)
def update_student(student_id: int, student: Student):
    global students
    for i, existing_student in enumerate(students):
        if existing_student['id'] == student_id:
            students[i] = student.dict()
            save_students()
            return student
    raise HTTPException(status_code=404, detail="Student not found")

@app.delete("/courses/{course_id}", response_model=dict)
def delete_course(course_id: int):
    global courses
    courses = [course for course in courses if course['id'] != course_id]
    save_courses()
    return {"message": "Course deleted"}

@app.delete("/students/{student_id}", response_model=dict)
def delete_student(student_id: int):
    global students
    students = [student for student in students if student['id'] != student_id]
    save_students()
    return {"message": "Student deleted"}

@app.post("/enroll/", response_model=Student)
def enroll_student(student_id: int, course_id: int):
    student = next((s for s in students if s['id'] == student_id), None)
    course = next((c for c in courses if c['id'] == course_id), None)
    if not student or not course:
        raise HTTPException(status_code=404, detail="Student or course not found")
    if course_id not in student['enrolled_courses']:
        student['enrolled_courses'].append(course_id)
        save_students()
    return student

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

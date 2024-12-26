from datetime import date, datetime

from sqlalchemy import func
from sqlalchemy.orm import aliased

from web import db, app
from web.models import Classes, Students


# Function: Count list class
def countClasses():
    return Classes.query.count()

# Function: Count student in class
def countStudentsInClass(classId):
    return Students.query.filter(Students.class_id == classId).count()

# Function: Get all class
def getAllClasses():
    return Classes.query.all()

def countClassNoStudent():
    number = (Classes.query
        .outerjoin(Students, Students.class_id == Classes.id)
        .group_by(Classes.id)
        .having(func.count(Students.id) == 0)
        .count())
    return number

# Function: Get list class with pagination
def getClasses(pageIndex=1, selectedgrade = None):
    query = Classes.query

    if selectedgrade:
        query = query.filter(Classes.grade == int(selectedgrade))  # Lọc theo grade

    # Lấy tổng số bản ghi (trước khi phân trang)
    totalRecords = query.count()

    # Pagination
    pageSize = app.config['PAGE_SIZE']
    skip = (pageIndex - 1) * pageSize
    classes = query.offset(skip).limit(pageSize).all()

    for class_item in classes:
        class_item.numberStudent = countStudentsInClass(class_item.id)

    return classes, totalRecords


# Function: Create new student
def createClass(new_class):
    try:
        db.session.add(new_class)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False


def calculateGrade(birth_date):
    current_year = date.today().year
    birth_year = birth_date.year
    age = current_year - birth_year
    if 15 <= age <= 16:
        return 10
    elif 17 <= age <= 18:
        return 11
    elif 19 <= age <= 20:
        return 12
    else:
        return None  # Không hợp lệ


# Function: Auto assign student to random class
def autoAssign(student):
    DOB = datetime.strptime(student.birth_date, "%Y-%m-%d")
    grade = calculateGrade(DOB)
    if not grade:
        return None
    # Tìm lớp thuộc khối và có sĩ số ít nhất hiện tại và chưa quá 40 học sinh
    available_class = (
        db.session.query(Classes)
        .outerjoin(Students, Students.class_id == Classes.id)
        .filter(Classes.grade == grade)
        .group_by(Classes.id)
        .having(func.count(Students.id) < app.config['MAX_STUDENT'])
        .order_by(func.count(Students.id))
        .first()
    )
    if not available_class:
        return None

    return available_class.id


#: Function get list student by class id
def getStudentsByClassId(class_id, pageIndex=1, search=None):
    query = Students.query.filter_by(class_id=class_id)

    # Filter tìm kiếm
    if search:
        query = query.filter(
            Students.name.like(f"%{search}%")  # Tìm theo tên
        )

    # Lấy tổng số bản ghi (trước khi phân trang)
    totalRecords = query.count()

    # Pagination
    pageSize = app.config['PAGE_SIZE']
    skip = (pageIndex - 1) * pageSize
    students = query.offset(skip).limit(pageSize).all()

    return students, totalRecords


#: Function get class info
def getClassById(class_id):
    classInfo = Classes.query.filter_by(id=class_id).first()
    classInfo.numberStudent = countStudentsInClass(class_id)
    return classInfo

#: Function remove student in class
def removeStudentById(class_id, student_id):
    try:
        student = Students.query.filter(Students.id==student_id,Students.class_id==class_id).first()
        student.class_id = None
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

#: Function add student into class
def addStudentToClass(class_id, student_id):
    try:
        student = Students.query.get(student_id)
        student.class_id = class_id
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

#Function statistic
def statisticClass():
    data = (db.session.query(Classes.name, db.func.count(Students.id))
        .outerjoin(Students, Classes.id == Students.class_id)
        .group_by(Classes.id, Classes.name)
        .all())
    return data
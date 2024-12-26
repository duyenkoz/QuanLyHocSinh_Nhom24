from web import app, db
from web.models import Students, Users


def load_user(user_id):
    return Users.query.get(user_id)


# Function: Get list student with pagination
def getStudents(pageIndex=1, search=None):
    query = Students.query

    # Filter tìm kiếm
    if search:
        query = query.filter(
            Students.name.like(f"%{search}%") |  # Tìm theo tên
            Students.email.like(f"%{search}%") |  # Tìm theo email
            Students.phone.like(f"%{search}%")  # Tìm theo số điện thoại
        )

    # Lấy tổng số bản ghi (trước khi phân trang)
    totalRecords = query.count()

    # Pagination
    pageSize = app.config['PAGE_SIZE']
    skip = (pageIndex - 1) * pageSize
    students = query.offset(skip).limit(pageSize).all()

    return students, totalRecords

# Function: Count list student
def countStudents():
    total_students = Students.query.count()
    return total_students

# Function: Count student not in class
def countStudentNotInClass():
    return Students.query.filter(Students.class_id.is_(None)).count()

# Function: Create new student
def createStudent(new_student):
    try:
        db.session.add(new_student)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

# Function: Edit student
def editStudent(student_id, edit_student):
    try:
        #Get student info
        student = Students.query.get(student_id)
        #Update info
        student.name = edit_student.name
        student.email = edit_student.email
        student.phone = edit_student.phone
        student.gender = edit_student.gender
        student.birth_date = edit_student.birth_date
        student.address = edit_student.address
        student.class_id = edit_student.class_id

        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

# Function: Delete student
def deleteStudent(student_id):
    try:
        Students.query.filter_by(id=student_id).delete()
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        return False

# Function: Get student by id
def getStudentById (student_id):
    return Students.query.get(student_id)

# Function: Get student not in class
def getStudentsNotInClass(pageIndex=1):
    query = Students.query.filter(Students.class_id.is_(None))

    # Lấy tổng số bản ghi (trước khi phân trang)
    totalRecords = query.count()

    # Pagination
    pageSize = app.config['PAGE_SIZE']
    skip = (pageIndex - 1) * pageSize
    students = query.offset(skip).limit(pageSize).all()

    return students, totalRecords






import math
from re import search

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from web import app, db
import services.authservice
from web.extentions.pagination import calcPagination
from web.models import Students, GenderEnum, Classes, Course
from web.services import studentservice, classservice


@app.before_request
def required_login():
    if not current_user.is_authenticated and request.endpoint != 'login':
        return redirect(url_for('login'))


@app.route('/')
# @login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method.__eq__('POST'):
        username = request.form.get('username')
        password = request.form.get('password')

        user = services.authservice.login(username, password)

        if user:
            login_user(user)
            return redirect(url_for('index'))

    return render_template('login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/manage-student')
def manage_student():
    pageIndex = request.args.get('pageIndex', 1, type=int)
    search = request.args.get('search', '').strip()

    # Lấy danh sách học sinh và tổng số bản ghi từ service
    students, totalRecords = studentservice.getStudents(pageIndex, search)

    # Tính tổng số trang
    totalPage = math.ceil(totalRecords / app.config['PAGE_SIZE'])

    # Tạo pagination
    pagination = calcPagination(pageIndex, totalPage)

    return render_template(
        'ManageStudent/index.html',
        students=students,
        totalPage=totalPage,
        currentPage=pageIndex,
        pagination=pagination,
        search=search,  # Gửi từ khóa tìm kiếm hiện tại để hiển thị
        totalRecords=totalRecords  # Tổng số kết quả để xử lý hiển thị thông báo
    )

@app.route('/manage-student/create', methods=['GET', 'POST'])
def manage_student_create():
    if request.method.__eq__('POST'):
        # Lấy dữ liệu từ form
        name = request.form.get('name')
        gender = request.form.get('gender')
        birth_date = request.form.get('birth_date')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')
        class_id = request.form.get('class_id')
        # Tạo đối tượng Student mới
        new_student = Students(
            name=name,
            gender=gender,
            birth_date=birth_date,
            phone=phone,
            email=email,
            address=address,
        )
        if class_id is None:
            new_student.class_id = classservice.autoAssign(new_student)
        new_student.class_id = class_id
        result = studentservice.createStudent(new_student)

        if result:
            return redirect(url_for('manage_student', message='Thêm thành công', statuscode=1))
        else:
            return redirect(url_for('manage_student', message='Thêm không thành công', statuscode=2))

    #Method: GET
    classes = classservice.getAllClasses()

    return render_template('ManageStudent/create.html', classes=classes)

@app.route('/manage-student/edit', methods=['GET', 'POST'])
def manage_student_edit():
    if request.method.__eq__('POST'):
        id = request.form.get('id')
        name = request.form.get('name')
        gender = request.form.get('gender')
        birth_date = request.form.get('birth_date')
        phone = request.form.get('phone')
        email = request.form.get('email')
        address = request.form.get('address')

        edit_student = Students(
            name=name,
            gender=gender,
            birth_date=birth_date,
            phone=phone,
            email=email,
            address=address
        )
        result = studentservice.editStudent(id, edit_student)

        if result:
            return redirect(url_for('manage_student', message='Chỉnh sửa thành công', statuscode=1))
        else:
            return redirect(url_for('manage_student', message='Chỉnh sửa không thành công', statuscode=2))

    id = request.args.get('id')
    student = studentservice.getStudentById(id)
    classes = classservice.getAllClasses()
    return render_template('ManageStudent/edit.html', student=student, classes=classes)

@app.route('/manage-student/delete')
def manage_student_delete():
    studentId = request.args.get('id')
    result = studentservice.deleteStudent(studentId)
    if result:
        return redirect(url_for('manage_student', message = 'Xóa thành công', statuscode = 1))
    else:
        return redirect(url_for('manage_student', message = 'Xóa không thành công', statuscode = 2))

@app.route('/manage-class')
def manage_class():
    pageIndex = request.args.get('pageIndex', 1, type=int)

    # Lấy danh sách học sinh và tổng số bản ghi từ service
    classes, totalRecords = classservice.getClasses(pageIndex)

    # Tính tổng số trang
    totalPage = math.ceil(totalRecords / app.config['PAGE_SIZE'])

    # Tạo pagination
    pagination = calcPagination(pageIndex, totalPage)

    return render_template(
        'ManageClass/index.html',
        classes=classes,
        totalPage=totalPage,
        currentPage=pageIndex,
        pagination=pagination,
        totalRecords=totalRecords  # Tổng số kết quả để xử lý hiển thị thông báo
    )

@app.route('/manage-class/create', methods=['GET', 'POST'])
def manage_class_create():
    if request.method.__eq__('POST'):
        # Lấy dữ liệu từ form
        name = request.form.get('name')
        grade = request.form.get('grade')

        # Tạo đối tượng Student mới
        new_class = Classes(
            name=name,
            grade=grade,

        )
        result = classservice.createClass(new_class)

        if result:
            return redirect(url_for('manage_class', message='Thêm thành công', statuscode=1))
        else:
            return redirect(url_for('manage_class', message='Thêm không thành công', statuscode=2))

    return render_template('ManageClass/create.html')

@app.route('/manage-class/students')
def manage_class_students():
    pageIndex = request.args.get('pageIndex', 1, type=int)
    classId = request.args.get('classId')
    search = request.args.get('search', None, type=str)
    # Lấy danh sách học sinh và tổng số bản ghi từ service
    students, totalRecords = classservice.getStudentsByClassId(classId, pageIndex, search)

    classInfo = classservice.getClassById(classId)
    # Tính tổng số trang
    totalPage = math.ceil(totalRecords / app.config['PAGE_SIZE'])

    # Tạo pagination
    pagination = calcPagination(pageIndex, totalPage)

    return render_template(
        'ManageClass/listStudent.html',
        classInfo=classInfo,
        students=students,
        totalPage=totalPage,
        currentPage=pageIndex,
        pagination=pagination,
        pageSize=app.config['PAGE_SIZE'],
        totalRecords=totalRecords  # Tổng số kết quả để xử lý hiển thị thông báo
    )
@app.route('/update_course', methods=['GET', 'POST'])
def update_course():
    courses = Course.query.all()  # Lấy danh sách môn học
    if request.method == 'POST':
        # Lấy dữ liệu từ form
        id = request.form.get('course_id')
        name = request.form.get('name')


        # Tìm môn học và cập nhật thông tin
        course = Course.query.get(id)
        if course:
            course.id = id
            course.name= name
            db.session.commit()
            flash('Cập nhật môn học thành công!', 'success')
        else:
            flash('Không tìm thấy môn học!', 'danger')

        return redirect(url_for('update_course'))

    return render_template('ManageCourse/update_course.html', courses=courses)
#them mon hoc

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        id = request.form.get('id')
        name = request.form.get('name')

        # Thêm môn học vào cơ sở dữ liệu
        new_course = Course(id=id, name=name)
        db.session.add(new_course)
        db.session.commit()

        flash('Thêm môn học thành công!', 'success')  # Thông báo thành công
        return redirect(url_for('add_course'))

    return render_template('ManageCourse/add_course.html')

# hiển thị danh sách môn học và tìm kiếm
@app.route('/manage_courses', methods=['GET'])
def manage_courses():
    keyword = request.args.get('keyword', '')
    if keyword:
        courses = Course.query.filter(Course.name.contains(keyword)).all()
        flash(f"Kết quả tìm kiếm cho từ khóa: '{keyword}'", 'info')
    else:
        courses = Course.query.all()
    return render_template('ManageCourse/manage_course.html', courses=courses)
@app.route('/delete_course/<string:course_id>', methods=['POST'])
def delete_course(course_id):
    course = Course.query.get(course_id)
    if course:
        db.session.delete(course)
        db.session.commit()
        flash(f'Đã xóa môn học "{course.name}" thành công!', 'success')
    else:
        flash('Không tìm thấy môn học để xóa!', 'danger')
    return redirect(url_for('manage_courses'))
if __name__ == '__main__':
    app.run(debug=True)

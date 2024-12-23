import math

from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user
from web import app, db
import services.authservice
from web.extentions.pagination import calcPagination
from web.models import Students, GenderEnum
from web.services import studentservice


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
    search = request.args.get('search')
    students = studentservice.getStudents(pageIndex, search)
    totalRecords = studentservice.countStudents()
    totalPage = math.ceil(totalRecords / app.config['PAGE_SIZE'])

    pagination = calcPagination(pageIndex, totalPage)
    return render_template('ManageStudent/index.html'
                           , students = students
                           , totalPage = totalPage
                           , currentPage = pageIndex
                           , pagination = pagination)


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

        # Kiểm tra giới tính để gán giá trị cho Gender Enum
        gender_enum = GenderEnum.FEMALE if gender == 'Nữ' else GenderEnum.MALE

        # Tạo đối tượng Student mới
        new_student = Students(
            name=name,
            gender=gender_enum,
            birth_date=birth_date,
            phone=phone,
            email=email,
            address=address
        )

        # Thêm vào database
        db.session.add(new_student)
        db.session.commit()

        # Sau khi thêm xong, redirect về trang danh sách học sinh
        flash('Học sinh đã được thêm thành công!', 'success')
        return redirect(url_for('manage_student'))

    return render_template('ManageStudent/create.html')


if __name__ == '__main__':
    app.run(debug=True)

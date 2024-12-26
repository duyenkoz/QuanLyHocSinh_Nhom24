import enum
import hashlib
from sqlalchemy.orm import relationship
from web import db, app, login
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Float, Enum, DateTime, Date
from enum import Enum as RoleEnum


# Tạo bảng người dùng
class UserRole(RoleEnum):
    ADMIN = 1
    USER = 2


class Users(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100),
                    default='https://res.cloudinary.com/dxxwcby8l/image/upload/v1679134375/ckvdo90ltnfns77zf1xb.jpg')
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    def __str__(self):
        return self.username


@login.user_loader
def user_load(user_id):
    return Users.query.get(user_id)


# Tạo bảng Gender Enum
class GenderEnum(enum.Enum):
    MALE = "Nam"
    FEMALE = "Nữ"


# Tạo bảng lớp
class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    grade = db.Column(db.Integer, nullable=False)
    max_students = db.Column(db.Integer, default=app.config['MAX_STUDENT'])
    students = relationship("Students", backref="class")

    def __str__(self):
        return self.name

# Tạo bảng Students
class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    gender = db.Column(Enum(GenderEnum), nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(15), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    class_id  = db.Column(db.Integer, db.ForeignKey('classes.id'), nullable=True)

    @property
    def numberStudent(self):
        return

    def __str__(self):
        return self.name



# Seed data
def seed_data():
    if not Users.query.first():
        admin = Users(
            name="Admin",
            username="admin",
            password=str(hashlib.md5('admin'.encode('utf-8')).hexdigest()),
            user_role=UserRole.ADMIN
        )
        user = Users(
            name="NhanVien",
            username="nhanvien",
            password=str(hashlib.md5('nhanvien'.encode('utf-8')).hexdigest()),
            user_role=UserRole.USER
        )
        db.session.add_all([admin, user])
        db.session.commit()



    if not Classes.query.first():
        classes = [
            Classes(name="10A1", grade=10),
            Classes(name="11A1", grade=11),
            Classes(name="12A1", grade=12),
        ]
        db.session.add_all(classes)
        db.session.commit()

class Course(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()

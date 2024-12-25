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
    name = db.Column(db.String(50), nullable=False)
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

    # if not Classes.query.first():
    #     classes = [
    #         Classes(name="10A1"),
    #         Classes(name="10A2"),
    #         Classes(name="11A1"),
    #         Classes(name="12A1"),
    #     ]
    #     db.session.add_all(classes)
    #     db.session.commit()

    # if not Students.query.first():
    #     students = [
    #         Students(
    #             name="Nguyễn Văn A",
    #             gender=GenderEnum.MALE,  # Sử dụng GenderEnum.MALE thay vì Gender.Nam
    #             birth_date="2001-01-15",
    #             address="123 Đường Lý Thường Kiệt, TP.HCM",
    #             phone="0912345678",
    #             email="vana@gmail.com",
    #             class_id=1
    #         ),
    #         Students(
    #             name="Trần Thị B",
    #             gender=GenderEnum.FEMALE,  # Sử dụng GenderEnum.FEMALE thay vì Gender.Nữ
    #             birth_date="2001-03-22",
    #             address="456 Đường Nguyễn Văn Linh, TP.HCM",
    #             phone="0987654321",
    #             email="thib@gmail.com",
    #             class_id=1
    #         ),
    #         Students(
    #             name="Lê Văn C",
    #             gender=GenderEnum.MALE,
    #             birth_date="2000-07-09",
    #             address="789 Đường Hai Bà Trưng, Hà Nội",
    #             phone="0934567890",
    #             email="vanc@gmail.com",
    #             class_id=2
    #         ),
    #         Students(
    #             name="Phạm Thị D",
    #             gender=GenderEnum.FEMALE,
    #             birth_date="2002-05-12",
    #             address="101 Đường Lê Lợi, Đà Nẵng",
    #             phone="0923456789",
    #             email="thid@gmail.com",
    #             class_id=1
    #         ),
    #         Students(
    #             name="Hoàng Văn E",
    #             gender=GenderEnum.MALE,
    #             birth_date="2001-11-20",
    #             address="202 Đường Võ Nguyên Giáp, Cần Thơ",
    #             phone="0911223344",
    #             email="vane@gmail.com",
    #             class_id=2
    #         ),
    #         Students(
    #             name="Nguyễn Thị F",
    #             gender=GenderEnum.FEMALE,
    #             birth_date="2002-09-30",
    #             address="303 Đường Nguyễn Huệ, TP.HCM",
    #             phone="0945678901",
    #             email="thif@gmail.com",
    #             class_id=1
    #         ),
    #         Students(
    #             name="Trần Văn G",
    #             gender=GenderEnum.MALE,
    #             birth_date="2000-12-25",
    #             address="404 Đường Hoàng Văn Thụ, Hà Nội",
    #             phone="0981234567",
    #             email="vang@gmail.com",
    #             class_id=2
    #         ),
    #         Students(
    #             name="Lê Thị H",
    #             gender=GenderEnum.FEMALE,
    #             birth_date="2001-08-18",
    #             address="505 Đường Trần Hưng Đạo, Đà Nẵng",
    #             phone="0956789012",
    #             email="thih@gmail.com",
    #             class_id=2
    #         ),
    #         Students(
    #             name="Phạm Văn I",
    #             gender=GenderEnum.MALE,
    #             birth_date="2002-06-10",
    #             address="606 Đường Phạm Ngũ Lão, Cần Thơ",
    #             phone="0935678902",
    #             email="vani@gmail.com",
    #             class_id=1
    #         ),
    #         Students(
    #             name="Hoàng Thị K",
    #             gender=GenderEnum.FEMALE,
    #             birth_date="2000-04-05",
    #             address="707 Đường Lê Lợi, TP.HCM",
    #             phone="0912345679",
    #             email="thik@gmail.com",
    #             class_id=2
    #         )
    #     ]
    #     db.session.add_all(students)
    #     db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()

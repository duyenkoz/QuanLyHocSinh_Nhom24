import hashlib
from flask import Flask
from flask_login import LoginManager, UserMixin
from urllib.parse import quote
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:%s@localhost/qlhs?charset=utf8mb4" % quote('admin@123')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['PAGE_SIZE'] = 10
app.secret_key = 'QuanLyHocSinhNhom24'

login = LoginManager(app)
login.init_app(app)
login.login_view = 'login'

db = SQLAlchemy(app)



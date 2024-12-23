from web import app
from web.models import Students, Users


def load_user(user_id):
    return Users.query.get(user_id)

#Function: Get list student with pagination
def getStudents(pageIndex = 1, search = None):
    students = Students.query

    #Filter
    if search:
        students = students.filter(Students.name.contains(search))

    #Pagination
    pageSize = app.config['PAGE_SIZE']
    skip = (pageIndex - 1) * pageSize
    students = students.offset(skip).limit(pageSize)

    return students

#Function: Count list student
def countStudents():
    return Students.query.count()
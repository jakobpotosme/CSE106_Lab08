from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
# from database import db, Students, Teachers, Admin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)
admin = Admin(app)


class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    studentEnrollment = db.relationship(
        'Enrollment', backref='Students', lazy=True)


class Teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    classes = db.relationship('Classes', backref='Teachers', lazy=True)


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=True, nullable=False)


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String, unique=True, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey(
        Teachers.id), nullable=False)
    numEnrolled = db.Column(db.Integer, unique=False, nullable=False)
    capacity = db.Column(db.Integer, unique=False, nullable=False)
    time = db.Column(db.String, unique=False, nullable=False)
    classEnrollment = db.relationship(
        'Enrollment', backref='Classes', lazy=True)

# Enrollment = db.table('Enrollment',
#                       db.Column('id', db.Integer, primary_key=True),
#                       db.column('class_id', db.Integer, db.ForeignKey(
#                           Classes.id)),
#                       db.column('student_id ', db.Integer, db.ForeignKey(
#                           Students.id)),
#                       db.column('grade', db.Integer)
#                       )


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey(
        Classes.id))
    student_id = db.Column(db.Integer, db.ForeignKey(
        Students.id))
    grade = db.Column(db.Integer)


# admin = Admin(name='admin', username='AdminAccount', password='123')
# db.session.add(admin)
# db.session.commit()
# @app.route('/login', methods=['GET', 'POST'])
# @app.route('/studentview')
# @app.route('/teacherview')
# admin page done with flask-admin


class CreatePage(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin.html')


class ReadUsers(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin.html')


class EditPage(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin.html')


class DeleteUser(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin.html')


admin.add_view(CreatePage(name='Create'))
admin.add_view(ReadUsers(name='Read'))
admin.add_view(EditPage(name='Edit'))
admin.add_view(DeleteUser(name='Delete'))

if __name__ == '__main__':
    app.run(debug=True)

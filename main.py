from flask import Flask, json, request, url_for, jsonify
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_login import current_user, login_user, LoginManager, UserMixin, logout_user, login_required
from flask_sqlalchemy.model import Model
from sqlalchemy.orm import query
from sqlalchemy.orm.session import Session
from werkzeug.utils import redirect
from flask_admin.contrib.sqla import ModelView
# from database import db, Students, Teachers, Admin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)
admin = Admin(app)

app.secret_key = 'keep it secret, keep it safe'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    studentConnect = db.relationship(
        'Students', backref='users', lazy=True)
    teachersConnect = db.relationship(
        'Teachers', backref='users', lazy=True)
    adminConnect = db.relationship(
        'Admins', backref='users', lazy=True)

    def check_password(self, password):
        return self.password == password

    def __repr__(self):
        return '%r' % (self.id)


class Students(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        Users.id), nullable=False)
    studentEnrollment = db.relationship(
        'Enrollment', backref='Students', lazy=True)

    def __repr__(self):
        return '%r' % (self.name)


class Teachers(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        Users.id), nullable=False)
    classes = db.relationship('Classes', backref='Teachers', lazy=True)

    def __repr__(self):
        return '%r' % (self.name)


class Admins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(
        Users.id), nullable=False)

    def __repr__(self):
        return '%r' % (self.name)


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

    def __repr__(self):
        return '%r' % (self.courseName)


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey(
        Classes.id))
    student_id = db.Column(db.Integer, db.ForeignKey(
        Students.id))
    grade = db.Column(db.Integer)

    def __repr__(self):
        return '<Enrollment %r>' % (self.id)


db.create_all()

# admin = Admin(name='admin', username='AdminAccount', password='123')
# db.session.add(admin)
# db.session.commit()


admin.add_view(ModelView(Classes, db.session))
admin.add_view(ModelView(Admins, db.session))
admin.add_view(ModelView(Students, db.session))
admin.add_view(ModelView(Teachers, db.session))
admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Enrollment, db.session))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = ''
        password = ''
        username += request.form['username']
        password += request.form['password']

        user = Users.query.filter_by(username=username).first()

        if user is None or user.check_password(password) is None:
            return redirect(url_for('login'))
        else:
            login_user(user)

            userType = Students.query.filter_by(user_id=user.id).first()
            # print(userType.id)
            if userType is None:
                print('Was not a student...checking teacher')
                userType = Teachers.query.filter_by(user_id=user.id).first()
                if userType is None:
                    print('not student or teacher...redirecting to admin')
                    return redirect(url_for('login'))
                else:
                    return render_template('teacher.html', teacher=userType)
            else:
                print('Successfully logging in student')
                # print(user.id)
                return redirect(url_for('student', currentStudentId=userType.id))

    return render_template('login.html')


@ app.route('/teacher/<int:currentTeacherId>', methods=['GET', 'POST'])
@ login_required
def teacher(currentTeacherId):

    q = db.session.query(Classes).filter(
        Classes.teacher_id == currentTeacherId).all()
    print(q)
    classes = []
    for i in q:
        # temp = i.courseName
        # print(temp)
        classes.append(i)
        # break
    teachers = []

    for i in classes:
        # print(i.teacher_id)
        teachers.append(Teachers.query.filter_by(id=i.teacher_id).first())

    # x = db.session.query(Teachers).filter_by(
    #     Teachers.id == Classes.teacher_id).all()

    # classes = Classes.query.filter_by(id=temp).all()
    # print(classes)
    # return render_template('student.html', enrollmentTable=enrollmentTable, classInfo=classes)
    return render_template('teacher.html', classInfo=classes, teachers=teachers)



@ app.route('/student/<int:currentStudentId>', methods=['GET', 'POST'])
@ login_required
def student(currentStudentId):

    # Gets information of student based on id
    currentStudent = Students.query.filter_by(id=currentStudentId).first()

    # Gets all classes
    allClasses = Classes.query.order_by(Classes.id).all()

    # temporary variable
    q = db.session.query(Enrollment).filter(
        Enrollment.student_id == currentStudentId).all()
    # print(q)

    # list that will hold all classes that student is in
    classes = []
    for i in q:
        temp = i.class_id
        # print(temp)
        classes.append(Classes.query.filter_by(id=temp).first())

    # list that will hold name of teachers for that course
    teachers = []
    for i in classes:
        # print(i.teacher_id)
        teachers.append(Teachers.query.filter_by(id=i.teacher_id).first())

    return render_template('student.html', classInfo=classes, teachers=teachers, allClasses=allClasses, student=currentStudent)


@app.route('/register', methods=["POST"])
@ login_required
def register():

    courseId = request.form['submitBtn']
    studentId = request.form['student']

    # Gets class information related to courseID
    currentClassInfo = Classes.query.filter_by(id=courseId).first()
    # print(currentClassInfo.numEnrolled)

    # Checks if student is already enrolled in course
    exists = db.session.query(Enrollment.class_id).filter_by(
        class_id=courseId).first() is not None
    # print(exists)

    # Checks if there is space and if student is enrolled in course
    if(currentClassInfo.numEnrolled < currentClassInfo.capacity and exists == False):

        # Creates new entry and adds it to data base
        newEntry = Enrollment(
            class_id=currentClassInfo.id, student_id=studentId)

        db.session.add(newEntry)
        db.session.commit()

        return jsonify({'response': 'success'})

    elif(exists is True):

        return 'You are already in this course!'
    else:

        return jsonify({'response': 'Class Full!'})


@app.route('/logout', methods=['POST'])
@ login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host="localhost", port=8000, debug=True)

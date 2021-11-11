from flask import Flask, request, url_for
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_login import current_user, login_user, LoginManager, UserMixin
from werkzeug.utils import redirect
# from database import db, Students, Teachers, Admin

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
db = SQLAlchemy(app)
admin = Admin(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
app.secret_key = 'keep it secret, keep it safe'


class Students(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=False, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, unique=False, nullable=False)
    studentEnrollment = db.relationship(
        'Enrollment', backref='Students', lazy=True)

    # def is_authenticated(self, username, password):
    #     if self.username == username and self.password == password:
    #         return True
    #     else:
    #         return False

    # def is_anonymous(self, username):
    #     if self.username != username:
    #         return True
    #     else:
    #         return False

    # def get_id(self):
    #     return self.id

    # def check_password(self, password):
    #     return self.password == password


class Teachers(UserMixin, db.Model):
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

# Flask-Login lecture 18 page 15

@login_manager.user_loader
def load_student(user_id):
    return Students.get_id(user_id)


@login_manager.user_loader
def load_teacher(user_id):
    return Teachers.get_id(user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = ''
        password = ''
        username += request.form['username']
        password += request.form['password']
        permission = request.form['permType']

        if(permission == 'student'):
            user = Students.query.filter_by(username=username).first()
            if(user is None):

                return 'no account found'
            else:
                # login_user(user)
                # return redirect(url_for('student'))
                return render_template('student.html', student=user)
        elif(permission == 'teacher'):
            user = Teachers.query.filter_by(username=username).first()
            if(user is None):

                return 'no account found'
            else:
                # login_user(user)
                print('Logged in Successfully')
                return render_template('teacher.html', teacher=user)

    return render_template('login.html')


@app.route('/student', methods=['GET', 'POST'])
def student():
    return render_template('student.html')


class CreatePage(BaseView):
    @expose('/', methods=['GET', 'POST'])
    def createUser(self):

        if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
            username = ''
            password = ''
            username += request.form['username']
            password += request.form['password']
            name = request.form['name']
            permission = request.form['permType']

            if(permission == 'student'):
                newEntry = Students(username=username,
                                    password=password, name=name)
                db.session.add(newEntry)
                db.session.commit()
            elif(permission == 'teacher'):
                newEntry = Teachers(username=username,
                                    password=password, name=name)
                db.session.add(newEntry)
                db.session.commit()

        return self.render('create.html')


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

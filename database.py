# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from main import app

# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///example.sqlite"
# db = SQLAlchemy(app)


# class Students(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=False, nullable=False)
#     username = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, unique=False, nullable=False)


# class Teachers(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=False, nullable=False)
#     username = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, unique=False, nullable=False)


# class Admin(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)
#     username = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, unique=True, nullable=False)


# class Classes(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     courseName = db.Column(db.String, unique=True, nullable=False)
#     teacher_id = db.Column(db.Integer, db.ForeignKey(
#         'Teachers.id'), unique=True, nullable=False)
#     numEnrolled = db.Column(db.Integer, unique=False, nullable=False)
#     capacity = db.Column(db.Integer, unique=False, nullable=False)
#     time = db.Column(db.String, unique=False, nullable=False)


# class Enrollment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     class_id = db.column(db.Integer, db.ForeignKey(
#         'Classes.id'), unique=True, nullable=False)
#     student_id = db.column(db.Integer, db.ForeignKey(
#         'Students.id'), unique=True, nullable=False)
#     grade = db.column(db.Integer, unique=False, nullable=False)

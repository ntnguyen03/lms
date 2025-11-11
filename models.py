from datetime import datetime
from database import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False, default='student')  # student, teacher
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='user', lazy=True)
    submissions = db.relationship('Submission', backref='user', lazy=True)
    created_courses = db.relationship('Course', backref='teacher', lazy=True)
    logs = db.relationship('Log', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_student(self):
        return self.role == 'student'
    
    def is_teacher(self):
        return self.role == 'teacher'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    enrollments = db.relationship('Enrollment', backref='course', lazy=True)
    assignments = db.relationship('Assignment', backref='course', lazy=True)


class Enrollment(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), primary_key=True)


class Assignment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.DateTime)
    
    # Relationships
    submissions = db.relationship('Submission', backref='assignment', lazy=True)


class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignment.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Float)
    # Optional path to uploaded file (assignment submission)
    file_path = db.Column(db.String(255), nullable=True)


class Log(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)  # login, view_material, submit_assignment
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
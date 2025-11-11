from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, PasswordField, BooleanField, SelectField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, Optional, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileAllowed
from models import User


class LoginForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired()])
    remember_me = BooleanField('Ghi nhớ đăng nhập')
    submit = SubmitField('Đăng nhập')


class RegisterForm(FlaskForm):
    username = StringField('Tên đăng nhập', validators=[DataRequired(), Length(min=4, max=20)])
    password = PasswordField('Mật khẩu', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Xác nhận mật khẩu', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Vai trò', choices=[('student', 'Sinh viên'), ('teacher', 'Giảng viên')], default='student')
    submit = SubmitField('Tạo tài khoản')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Tên đăng nhập đã tồn tại!')


class CourseForm(FlaskForm):
    name = StringField('Tên khóa học', validators=[DataRequired(), Length(min=2, max=200)])
    description = TextAreaField('Mô tả', validators=[Optional()])
    submit = SubmitField('Tạo khóa học')


class AssignmentForm(FlaskForm):
    title = StringField('Tiêu đề bài tập', validators=[DataRequired(), Length(min=2, max=200)])
    deadline = DateTimeField('Hạn nộp', validators=[Optional()])
    submit = SubmitField('Tạo bài tập')


class SubmissionForm(FlaskForm):
    score = FloatField('Điểm số', validators=[Optional()])
    file = FileField('Tệp đính kèm', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'zip', 'txt', 'py', 'ipynb'], 'Chỉ cho phép các định dạng: pdf, docx, zip, txt, py, ipynb'),
        Optional()
    ])
    submit = SubmitField('Nộp bài')
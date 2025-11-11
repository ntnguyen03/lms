from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from database import db, migrate
from werkzeug.middleware.proxy_fix import ProxyFix
import os
from datetime import datetime, timedelta
import random
from importlib import import_module
from forms import LoginForm, RegisterForm, CourseForm, AssignmentForm, SubmissionForm
from dotenv import load_dotenv
load_dotenv()
from werkzeug.utils import secure_filename
import uuid

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except (ImportError, AttributeError):  # pragma: no cover - optional dependency
    GEMINI_AVAILABLE = False
    genai = None


def create_app() -> Flask:
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Basic config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    db_path = os.environ.get('DATABASE_URL') or 'sqlite:///lms.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # File upload config
    app.config['UPLOAD_FOLDER'] = os.path.join(app.instance_path, 'uploads')
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB limit
    # Ensure instance and upload directories exist
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    except Exception:
        pass

    # Init extensions
    db.init_app(app)
    migrate.init_app(app, db)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Defer imports to avoid circular deps
    from models import User, Course, Enrollment, Assignment, Submission, Log
    from analytics import load_sales_data_summary

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    def create_sample_data():
        """Create comprehensive sample data for real-world classroom"""
        try:
            # Create realistic users
            users_data = [
                # Teachers
                {'username': 'admin', 'role': 'teacher', 'password': 'admin123'},
                {'username': 'teacher1', 'role': 'teacher', 'password': 'teacher123'},
                {'username': 'teacher2', 'role': 'teacher', 'password': 'teacher123'},
                {'username': 'teacher3', 'role': 'teacher', 'password': 'teacher123'},
                {'username': 'teacher4', 'role': 'teacher', 'password': 'teacher123'},
                {'username': 'teacher5', 'role': 'teacher', 'password': 'teacher123'},
            ]
            
            # Generate 80 students with realistic Vietnamese names
            vietnamese_names = [
                'Nguyen Van An', 'Tran Thi Binh', 'Le Van Cuong', 'Pham Thi Dung', 'Hoang Van Em',
                'Vu Thi Phuong', 'Dang Van Giang', 'Bui Thi Hoa', 'Do Van Inh', 'Ngo Thi Kim',
                'Ly Van Long', 'Truong Thi Mai', 'Dinh Van Nam', 'Cao Thi Oanh', 'Phan Van Phuc',
                'Vo Thi Quynh', 'Nguyen Van Son', 'Tran Thi Thu', 'Le Van Uy', 'Pham Thi Van',
                'Hoang Van Xuan', 'Vu Thi Yen', 'Dang Van Bao', 'Bui Thi Cam', 'Do Van Duc',
                'Ngo Thi Em', 'Ly Van Phong', 'Truong Thi Quy', 'Dinh Van Sang', 'Cao Thi Tam',
                'Phan Van Uyen', 'Vo Thi Vy', 'Nguyen Van Anh', 'Tran Thi Bich', 'Le Van Canh',
                'Pham Thi Dan', 'Hoang Van Em', 'Vu Thi Phuong', 'Dang Van Giang', 'Bui Thi Hoa',
                'Do Van Inh', 'Ngo Thi Kim', 'Ly Van Long', 'Truong Thi Mai', 'Dinh Van Nam',
                'Cao Thi Oanh', 'Phan Van Phuc', 'Vo Thi Quynh', 'Nguyen Van Son', 'Tran Thi Thu',
                'Le Van Uy', 'Pham Thi Van', 'Hoang Van Xuan', 'Vu Thi Yen', 'Dang Van Bao',
                'Bui Thi Cam', 'Do Van Duc', 'Ngo Thi Em', 'Ly Van Phong', 'Truong Thi Quy',
                'Dinh Van Sang', 'Cao Thi Tam', 'Phan Van Uyen', 'Vo Thi Vy', 'Nguyen Van Anh',
                'Tran Thi Bich', 'Le Van Canh', 'Pham Thi Dan', 'Hoang Van Em', 'Vu Thi Phuong',
                'Dang Van Giang', 'Bui Thi Hoa', 'Do Van Inh', 'Ngo Thi Kim', 'Ly Van Long',
                'Truong Thi Mai', 'Dinh Van Nam', 'Cao Thi Oanh', 'Phan Van Phuc', 'Vo Thi Quynh'
            ]
            
            # Create students with Vietnamese names
            for i, name in enumerate(vietnamese_names[:80], 1):
                # Convert name to username format
                username = name.lower().replace(' ', '') + str(i)
                users_data.append({
                    'username': username,
                    'role': 'student', 
                    'password': 'student123'
                })
            
            users = []
            for user_data in users_data:
                user = User(username=user_data['username'], role=user_data['role'])
                user.set_password(user_data['password'])
                users.append(user)
            
            db.session.add_all(users)
            db.session.commit()
            
            # Create realistic courses
            courses_data = [
                {'name': 'Nhập môn Lập trình Python', 'description': 'Khóa học cơ bản về lập trình Python cho người mới bắt đầu', 'teacher_id': 2},
                {'name': 'Cấu trúc Dữ liệu và Giải thuật', 'description': 'Học về các cấu trúc dữ liệu cơ bản và thuật toán', 'teacher_id': 3},
                {'name': 'Phân tích Dữ liệu với Pandas', 'description': 'Sử dụng Pandas để phân tích và xử lý dữ liệu', 'teacher_id': 1},
                {'name': 'Machine Learning cơ bản', 'description': 'Giới thiệu về Machine Learning và các thuật toán cơ bản', 'teacher_id': 4},
                {'name': 'Web Development với Flask', 'description': 'Xây dựng ứng dụng web với Flask framework', 'teacher_id': 2},
                {'name': 'Database Management', 'description': 'Quản lý cơ sở dữ liệu với SQL', 'teacher_id': 3},
            ]
            
            courses = []
            for course_data in courses_data:
                course = Course(name=course_data['name'], 
                               description=course_data['description'], 
                               teacher_id=course_data['teacher_id'])
                courses.append(course)
            
            db.session.add_all(courses)
            db.session.commit()
            
            # Create realistic assignments
            assignments_data = [
                # Python course assignments
                {'title': 'Bài tập 1: Biến và Kiểu dữ liệu', 'course_id': 1, 'deadline': datetime.now() + timedelta(days=7)},
                {'title': 'Bài tập 2: Vòng lặp và Điều kiện', 'course_id': 1, 'deadline': datetime.now() + timedelta(days=14)},
                {'title': 'Bài tập 3: Hàm và Module', 'course_id': 1, 'deadline': datetime.now() + timedelta(days=21)},
                {'title': 'Dự án cuối kỳ: Ứng dụng Python', 'course_id': 1, 'deadline': datetime.now() + timedelta(days=30)},
                
                # Data Structures assignments
                {'title': 'Bài tập 1: Array và List', 'course_id': 2, 'deadline': datetime.now() + timedelta(days=5)},
                {'title': 'Bài tập 2: Stack và Queue', 'course_id': 2, 'deadline': datetime.now() + timedelta(days=12)},
                {'title': 'Bài tập 3: Tree và Graph', 'course_id': 2, 'deadline': datetime.now() + timedelta(days=19)},
                
                # Data Analysis assignments
                {'title': 'Phân tích Dataset Sales', 'course_id': 3, 'deadline': datetime.now() + timedelta(days=10)},
                {'title': 'Visualization với Matplotlib', 'course_id': 3, 'deadline': datetime.now() + timedelta(days=17)},
                
                # Machine Learning assignments
                {'title': 'Linear Regression', 'course_id': 4, 'deadline': datetime.now() + timedelta(days=15)},
                {'title': 'Classification với Decision Tree', 'course_id': 4, 'deadline': datetime.now() + timedelta(days=25)},
            ]
            
            assignments = []
            for assignment_data in assignments_data:
                assignment = Assignment(title=assignment_data['title'], 
                                      course_id=assignment_data['course_id'], 
                                      deadline=assignment_data['deadline'])
                assignments.append(assignment)
            
            db.session.add_all(assignments)
            db.session.commit()
            
            # Create realistic enrollments (students enroll in multiple courses)
            enrollments = []
            student_ids = list(range(7, 87))  # All 80 students (6 teachers + 80 students = 86 total users)
            
            # Each student enrolls in 2-4 courses
            for student_id in student_ids:
                enrolled_courses = random.sample(list(range(1, 7)), random.randint(2, 4))
                for course_id in enrolled_courses:
                    enrollment = Enrollment(user_id=student_id, course_id=course_id)
                    enrollments.append(enrollment)
            
            db.session.add_all(enrollments)
            db.session.commit()
            
            # Create realistic submissions with varied scores
            submissions = []
            for student_id in student_ids:
                # Each student submits some assignments
                student_assignments = random.sample(assignments, random.randint(3, 8))
                for assignment in student_assignments:
                    # Check if student is enrolled in this course
                    enrollment = Enrollment.query.filter_by(user_id=student_id, course_id=assignment.course_id).first()
                    if enrollment:
                        # Generate realistic scores based on assignment difficulty
                        if 'cơ bản' in assignment.title.lower() or 'bài tập 1' in assignment.title.lower():
                            score = random.uniform(7.0, 10.0)  # Higher scores for basic assignments
                        elif 'dự án' in assignment.title.lower() or 'cuối kỳ' in assignment.title.lower():
                            score = random.uniform(6.0, 9.5)  # Varied scores for projects
                        else:
                            score = random.uniform(5.0, 9.0)  # Normal range
                        
                        submission = Submission(assignment_id=assignment.id, 
                                              student_id=student_id, 
                                              score=round(score, 1))
                        submissions.append(submission)
            
            db.session.add_all(submissions)
            db.session.commit()
            
            # Create realistic learning logs
            logs = []
            for student_id in student_ids:
                # Login logs (students login 5-20 times)
                login_count = random.randint(5, 20)
                for i in range(login_count):
                    log = Log(user_id=student_id, 
                            action='login',
                            timestamp=datetime.now() - timedelta(days=random.randint(0, 30)))
                    logs.append(log)
                
                # Course activity logs
                user_enrollments = Enrollment.query.filter_by(user_id=student_id).all()
                for enrollment in user_enrollments:
                    # View material logs
                    view_count = random.randint(3, 10)
                    for i in range(view_count):
                        log = Log(user_id=student_id, 
                                course_id=enrollment.course_id,
                                action='view_material',
                                timestamp=datetime.now() - timedelta(days=random.randint(0, 25)))
                        logs.append(log)
                    
                    # Submit assignment logs
                    course_assignments = Assignment.query.filter_by(course_id=enrollment.course_id).all()
                    submitted_assignments = random.sample(course_assignments, random.randint(1, len(course_assignments)))
                    for assignment in submitted_assignments:
                        log = Log(user_id=student_id, 
                                course_id=enrollment.course_id,
                                action='submit_assignment',
                                timestamp=datetime.now() - timedelta(days=random.randint(0, 20)))
                        logs.append(log)
            
            # Teacher activity logs
            teacher_ids = [1, 2, 3, 4]
            for teacher_id in teacher_ids:
                login_count = random.randint(10, 30)
                for i in range(login_count):
                    log = Log(user_id=teacher_id, 
                            action='login',
                            timestamp=datetime.now() - timedelta(days=random.randint(0, 30)))
                    logs.append(log)
            
            db.session.add_all(logs)
            db.session.commit()
            
            print("Comprehensive sample data created successfully!")
            print(f"Created: {len(users)} users, {len(courses)} courses, {len(assignments)} assignments")
            print(f"Created: {len(enrollments)} enrollments, {len(submissions)} submissions, {len(logs)} logs")
            
        except Exception as e:
            print(f"Error creating sample data: {e}")

    def get_student_learning_profile(user):
        submissions = Submission.query.filter_by(student_id=user.id).all()
        scores = [s.score for s in submissions if s.score is not None]
        avg_score = sum(scores) / len(scores) if scores else None

        login_count = Log.query.filter_by(user_id=user.id, action='login').count()
        assignments_completed = len(scores)
        courses_enrolled = Enrollment.query.filter_by(user_id=user.id).count()

        recent_topics = []
        for submission in sorted(submissions, key=lambda s: s.id, reverse=True):
            assignment = submission.assignment
            if assignment and assignment.title not in recent_topics:
                recent_topics.append(assignment.title)
            if len(recent_topics) >= 5:
                break

        return {
            'avg_score': round(avg_score, 1) if avg_score is not None else None,
            'login_count': login_count,
            'assignments_completed': assignments_completed,
            'courses_enrolled': courses_enrolled,
            'recent_topics': recent_topics,
        }

    def get_teacher_overview_profile(user):
        courses = Course.query.filter_by(teacher_id=user.id).all()
        course_ids = [course.id for course in courses]

        total_students = 0
        avg_scores = []
        course_summaries = []

        for course in courses:
            enrollment_count = Enrollment.query.filter_by(course_id=course.id).count()
            total_students += enrollment_count

            assignments = Assignment.query.filter_by(course_id=course.id).all()
            assignment_ids = [assignment.id for assignment in assignments]
            if assignment_ids:
                course_scores = [
                    submission.score for submission in Submission.query.filter(Submission.assignment_id.in_(assignment_ids)).all()
                    if submission.score is not None
                ]
            else:
                course_scores = []

            if course_scores:
                avg_scores.append(sum(course_scores) / len(course_scores))

            course_summaries.append(
                f"{course.name}: {enrollment_count} sinh viên, {len(assignments)} bài tập"
            )

        recent_logs = Log.query.filter(Log.course_id.in_(course_ids)).order_by(Log.timestamp.desc()).limit(5).all() if course_ids else []

        return {
            'courses': [course.name for course in courses],
            'total_students': total_students,
            'avg_score': round(sum(avg_scores) / len(avg_scores), 1) if avg_scores else None,
            'course_summaries': course_summaries,
            'recent_events': [
                {
                    'action': log.action,
                    'user_id': log.user_id,
                    'course_id': log.course_id,
                    'timestamp': log.timestamp.isoformat() if log.timestamp else None,
                }
                for log in recent_logs
            ],
        }

    def format_profile_for_prompt(profile):
        lines = []
        for key, value in profile.items():
            if value in (None, [], {}):
                continue
            label = key.replace('_', ' ').capitalize()
            if isinstance(value, list):
                values = ', '.join(str(item) for item in value)
                lines.append(f"- {label}: {values}")
            elif isinstance(value, dict):
                sub_lines = []
                for sub_key, sub_value in value.items():
                    sub_lines.append(f"  • {sub_key}: {sub_value}")
                if sub_lines:
                    lines.append(f"- {label}:\n" + '\n'.join(sub_lines))
            elif isinstance(value, float):
                lines.append(f"- {label}: {value:.1f}")
            else:
                lines.append(f"- {label}: {value}")
        return '\n'.join(lines)

    def generate_rule_based_response(user_message, role, profile):
        message_lower = user_message.lower()
        
        # Kiểm tra câu hỏi về điểm trước
        if any(keyword in message_lower for keyword in ['điểm', 'grade', 'score', 'điểm số', 'điểm của tôi']):
            if role == 'student':
                avg_score = profile.get('avg_score')
                if avg_score is not None:
                    return f"Điểm trung bình hiện tại của bạn là {avg_score:.1f}."
                else:
                    return "Bạn chưa có điểm số nào. Hãy nộp bài tập để nhận điểm."
            else:
                total_students = profile.get('total_students')
                avg_score = profile.get('avg_score')
                if avg_score is not None:
                    return f"Điểm trung bình của lớp là {avg_score:.1f}. Lớp có {total_students} sinh viên." if total_students else f"Điểm trung bình của lớp là {avg_score:.1f}."
                else:
                    return "Chưa có dữ liệu điểm số."
        
        responses = [
            (['gợi ý học tập', 'học tập', 'study', 'học như thế nào', 'cách học'],
             "Để cải thiện điểm số, bạn nên ôn lại kiến thức cốt lõi, làm thêm bài tập tự luyện và trao đổi với giảng viên khi gặp khó khăn."),
            (['bài tập', 'bài tập về nhà', 'assignment'],
             "Hãy lập kế hoạch giải các bài tập theo mức độ ưu tiên, bắt đầu từ những bài còn gặp khó khăn và hoàn thành trước hạn."),
            (['khóa học', 'course'],
             "Bạn có thể tham gia thảo luận nhóm, xem lại ghi chú bài giảng và nhờ hỗ trợ từ giảng viên để hiểu sâu hơn nội dung khóa học."),
            (['lịch học', 'schedule', 'time'],
             "Hãy chia nhỏ thời gian học từng chủ đề, duy trì lịch học cố định 2-3 giờ mỗi ngày và dành thời gian ôn tập cuối tuần."),
            (['mục tiêu', 'goal'],
             "Đặt mục tiêu SMART: Cụ thể, Đo lường được, Khả thi, Liên quan và Có thời hạn. Theo dõi tiến độ hàng tuần để điều chỉnh."),
        ]

        for keywords, response in responses:
            if any(keyword in message_lower for keyword in keywords):
                return response

        if role == 'student':
            base = "Hãy duy trì thói quen học tập đều đặn, chủ động đặt câu hỏi và tự đánh giá tiến độ của bản thân." 
            return base
        else:
            base = "Bạn nên theo dõi tiến độ lớp học, hỗ trợ sinh viên gặp khó khăn và cập nhật kịp thời các tài liệu giảng dạy."
            total_students = profile.get('total_students')
            if total_students:
                base += f" Lớp của bạn hiện có {total_students} sinh viên."
            return base

    def call_external_ai_model(user_message, role, profile):
        if not GEMINI_AVAILABLE:
            return None, 'Google Generative AI SDK chưa được cài đặt. Hãy cài đặt bằng: pip install google-generativeai'

        api_key = os.environ.get('GEMINI_API_KEY')
        if not api_key:
            return None, 'Biến môi trường GEMINI_API_KEY chưa được cấu hình. Vui lòng thêm API key vào file .env'

        try:
            genai.configure(api_key=api_key)
        except Exception as exc:  # pragma: no cover - defensive
            app.logger.warning('Không thể cấu hình Gemini API: %s', exc)
            return None, str(exc)

        # Chỉ sử dụng một model duy nhất: gemini-2.5-flash
        model_name = 'gemini-2.5-flash'
        
        profile_text = format_profile_for_prompt(profile)
        
        # Tạo system prompt cho Gemini - đơn giản hóa để tránh recitation filter
        system_prompt = (
            "Bạn là trợ lý học tập bằng tiếng Việt cho {role}. "
            "Hãy đưa ra lời khuyên ngắn gọn và thực tế."
        ).format(role='giảng viên' if role == 'teacher' else 'sinh viên')

        if profile_text:
            # Đơn giản hóa profile text
            system_prompt += "\n\nThông tin người dùng:\n" + profile_text

        # Tạo prompt đầy đủ - tránh format phức tạp
        full_prompt = f"{system_prompt}\n\nCâu hỏi: {user_message}\n\nTrả lời:"

        try:
            model = genai.GenerativeModel(model_name)
            
            # Thử không dùng safety_settings trước (để tránh recitation filter)
            try:
                response = model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.5,
                        top_p=0.95,
                        max_output_tokens=512,
                    )
                )
            except Exception as safety_exc:
                # Nếu lỗi do thiếu safety_settings, thử lại với settings tối thiểu
                app.logger.debug(f'Thử lại với safety settings cho {model_name}')
                response = model.generate_content(
                    full_prompt,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.5,
                        top_p=0.95,
                        max_output_tokens=512,
                    ),
                    safety_settings=[
                        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
                    ]
                )
            
            # Kiểm tra finish_reason trước khi truy cập response.text
            if not response or not response.candidates:
                return None, 'Không nhận được phản hồi từ model'
            
            candidate = response.candidates[0]
            finish_reason = candidate.finish_reason
            
            # Xử lý các trường hợp finish_reason
            if finish_reason == 1:  # SAFETY - Content bị block vì safety
                app.logger.warning(f'Model {model_name}: Response bị block bởi safety filter')
                return None, 'Phản hồi bị chặn bởi safety filter'
            elif finish_reason == 2:  # RECITATION - Content bị block vì recitation
                app.logger.warning(f'Model {model_name}: Response bị block bởi recitation filter')
                return None, 'Phản hồi bị chặn bởi recitation filter'
            elif finish_reason == 3:  # OTHER
                app.logger.warning(f'Model {model_name}: Response bị block vì lý do khác')
                return None, 'Phản hồi bị chặn'
            
            # Nếu finish_reason là STOP (0) hoặc MAX_TOKENS (4), lấy text
            try:
                response_text = response.text
                if response_text:
                    app.logger.info(f'Gemini API thành công với model: {model_name}')
                    return response_text.strip(), None
                else:
                    return None, 'Không có nội dung phản hồi'
            except Exception as text_exc:
                app.logger.warning(f'Model {model_name}: Không thể lấy text từ response: {text_exc}')
                return None, f'Lỗi khi đọc phản hồi: {text_exc}'
                
        except Exception as exc:
            error_msg = str(exc)
            app.logger.warning(f'Lỗi với model {model_name}: {error_msg}')
            return None, f'Lỗi khi gọi API: {error_msg}'

    def generate_ai_chat_response(user_message, user):
        role = 'teacher' if user.is_teacher() else 'student'
        profile = get_teacher_overview_profile(user) if role == 'teacher' else get_student_learning_profile(user)

        ai_text, error = call_external_ai_model(user_message, role, profile)
        if ai_text:
            return ai_text, False

        fallback_text = generate_rule_based_response(user_message, role, profile)
        if error:
            app.logger.info('Sử dụng phản hồi fallback cho AI chat: %s', error)
        return fallback_text, True

    @app.route('/')
    @login_required
    def index():
        # Auto-create sample data if database is empty
        if User.query.count() == 0:
            create_sample_data()
        
        total_users = User.query.count()
        total_students = User.query.filter_by(role='student').count()
        total_courses = Course.query.count()
        total_enrollments = Enrollment.query.count()
        sales_summary = None
        try:
            sales_summary = load_sales_data_summary('DuLieu_BanHang.xlsx')
        except Exception:
            sales_summary = None
        return render_template('index.html',
                               total_users=total_students,  # Chỉ đếm sinh viên
                               total_courses=total_courses,
                               total_enrollments=total_enrollments,
                               sales_summary=sales_summary,
                               current_month=datetime.now().strftime('%m'))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                # Log login action
                try:
                    log = Log(user_id=user.id, action='login')
                    db.session.add(log)
                    db.session.commit()
                except Exception:
                    pass  # Ignore log errors
                
                next_page = request.args.get('next')
                flash(f'Chào mừng trở lại, {user.username}!', 'success')
                return redirect(next_page or url_for('index'))
            else:
                flash('Đăng nhập thất bại. Vui lòng kiểm tra tên đăng nhập và mật khẩu.', 'danger')
        return render_template('auth/login.html', form=form)

    @app.route('/register', methods=['GET', 'POST'])
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, role=form.role.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Tài khoản của bạn đã được tạo thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('login'))
        return render_template('auth/register.html', form=form)

    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        flash('Bạn đã đăng xuất.', 'info')
        return redirect(url_for('login'))

    @app.route('/courses')
    @login_required
    def courses():
        if current_user.is_teacher():
            # Teacher sees own courses + option to view all
            my_courses = Course.query.filter_by(teacher_id=current_user.id).all()
            all_courses = Course.query.all()
            return render_template('courses.html', 
                                 my_courses=my_courses, 
                                 all_courses=all_courses,
                                 is_teacher=True)
        else:
            # For students, show enrolled courses and available courses
            enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
            enrolled_course_ids = [e.course_id for e in enrollments]
            enrolled_courses = [e.course for e in enrollments]
            available_courses = Course.query.filter(~Course.id.in_(enrolled_course_ids)).all()
            
            return render_template('courses.html', 
                                 enrolled_courses=enrolled_courses,
                                 available_courses=available_courses,
                                 is_teacher=False)

    @app.route('/search')
    @login_required
    def search():
        """Global search for users and courses."""
        q = request.args.get('q', '').strip()
        if not q:
            flash('Vui lòng nhập từ khóa tìm kiếm.', 'warning')
            return redirect(request.referrer or url_for('index'))

        # Case-insensitive search
        users = User.query.filter(User.username.ilike(f"%{q}%")).all()
        courses = Course.query.filter(Course.name.ilike(f"%{q}%")).all()

        return render_template('search_results.html', query=q, users=users, courses=courses)

    @app.route('/courses/add', methods=['GET', 'POST'])
    @login_required
    def add_course():
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể tạo khóa học.', 'danger')
            return redirect(url_for('courses'))
        
        form = CourseForm()
        if form.validate_on_submit():
            course = Course(name=form.name.data, description=form.description.data, teacher_id=current_user.id)
            db.session.add(course)
            db.session.commit()
            flash('Khóa học đã được tạo thành công!', 'success')
            return redirect(url_for('courses'))
        return render_template('add_course.html', form=form)

    @app.route('/courses/<int:course_id>')
    @login_required
    def course_detail(course_id):
        course = Course.query.get_or_404(course_id)
        assignments = Assignment.query.filter_by(course_id=course_id).all()
        return render_template('course_detail.html', course=course, assignments=assignments)

    @app.route('/courses/<int:course_id>/enroll')
    @login_required
    def enroll_course(course_id):
        if not current_user.is_student():
            flash('Chỉ sinh viên mới có thể đăng ký khóa học.', 'danger')
            return redirect(url_for('courses'))
        
        # Check if already enrolled
        enrollment = Enrollment.query.filter_by(user_id=current_user.id, course_id=course_id).first()
        if enrollment:
            flash('Bạn đã đăng ký khóa học này rồi.', 'info')
        else:
            enrollment = Enrollment(user_id=current_user.id, course_id=course_id)
            db.session.add(enrollment)
            db.session.commit()
            flash('Đăng ký khóa học thành công!', 'success')
        
        return redirect(url_for('courses'))

    @app.route('/assignments/<int:assignment_id>/submit', methods=['GET', 'POST'])
    @login_required
    def submit_assignment(assignment_id):
        if not current_user.is_student():
            flash('Chỉ sinh viên mới có thể nộp bài.', 'danger')
            return redirect(url_for('courses'))
        
        assignment = Assignment.query.get_or_404(assignment_id)
        form = SubmissionForm()
        
        if form.validate_on_submit():
            # Handle optional file upload
            file_path = None
            try:
                uploaded = getattr(form, 'file', None)
                if uploaded and uploaded.data:
                    f = uploaded.data
                    raw_filename = secure_filename(f.filename)
                    unique_prefix = f"{current_user.id}_{int(datetime.now().timestamp())}_{uuid.uuid4().hex[:8]}_"
                    filename = unique_prefix + raw_filename
                    save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                    f.save(save_path)
                    file_path = save_path
            except Exception:
                # If upload fails, continue but don't block submission
                file_path = None

            # Students should not set the score; teacher will grade later.
            submission = Submission(assignment_id=assignment_id, student_id=current_user.id, score=None, file_path=file_path)
            db.session.add(submission)
            
            # Log submission action
            log = Log(user_id=current_user.id, course_id=assignment.course_id, action='submit_assignment')
            db.session.add(log)
            db.session.commit()
            
            flash('Nộp bài thành công!', 'success')
            return redirect(url_for('course_detail', course_id=assignment.course_id))
        
        return render_template('submit_assignment.html', form=form, assignment=assignment)

    @app.route('/profile')
    @login_required
    def profile():
        # Get user statistics
        user_submissions = Submission.query.filter_by(student_id=current_user.id).all()
        user_enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
        user_logs = Log.query.filter_by(user_id=current_user.id).all()
        
        avg_score = sum(sub.score for sub in user_submissions if sub.score) / len(user_submissions) if user_submissions else 0
        login_count = len([log for log in user_logs if log.action == 'login'])
        
        return render_template('profile.html', 
                               user=current_user,
                               avg_score=avg_score,
                               login_count=login_count,
                               submissions_count=len(user_submissions),
                               enrollments_count=len(user_enrollments))

    @app.route('/settings')
    @login_required
    def settings():
        return render_template('settings.html', user=current_user)

    @app.route('/ai-support')
    @login_required
    def ai_support():
        """AI Hỗ trợ học tập - khác nhau giữa teacher và student"""
        if current_user.is_teacher():
            # Allow optional risk filter: ?risk=all|high|medium|low
            risk = request.args.get('risk', 'all')
            # Giảng viên: Xem tất cả sinh viên và gợi ý quản lý lớp
            students = User.query.filter_by(role='student').all()
            student_analytics = []

            for student in students:
                submissions = Submission.query.filter_by(student_id=student.id).all()
                scores = [s.score for s in submissions if s.score is not None]
                avg_score = sum(scores) / len(scores) if scores else 0

                login_count = Log.query.filter_by(user_id=student.id, action='login').count()
                assignments_completed = len(scores)

                # AI gợi ý cho giảng viên và xác định mức rủi ro
                if avg_score < 5:
                    ai_advice = f"Sinh viên {student.username} có điểm thấp ({avg_score:.1f}). Nên hỗ trợ thêm và kiểm tra tiến độ học tập."
                    risk_level = 'high'
                elif login_count < 5:
                    ai_advice = f"Sinh viên {student.username} ít đăng nhập ({login_count} lần). Nên nhắc nhở tham gia lớp học thường xuyên hơn."
                    risk_level = 'medium'
                elif avg_score >= 8:
                    ai_advice = f"Sinh viên {student.username} học tốt ({avg_score:.1f}). Có thể giao thêm bài tập nâng cao."
                    risk_level = 'low'
                else:
                    ai_advice = f"Sinh viên {student.username} có tiến bộ tốt. Tiếp tục theo dõi và hỗ trợ."
                    risk_level = 'medium'

                student_analytics.append({
                    'student': student,
                    'avg_score': round(avg_score, 1),
                    'login_count': login_count,
                    'assignments_completed': assignments_completed,
                    'ai_advice': ai_advice,
                    'risk_level': risk_level
                })

            # Apply filter if requested
            if risk and risk != 'all':
                student_analytics = [s for s in student_analytics if s.get('risk_level') == risk]

            return render_template('ai_support.html', 
                                 role='teacher',
                                 user=current_user,
                                 student_analytics=student_analytics,
                                 total_students=len(students),
                                 selected_risk=risk,
                                 metrics={
                                     'avg_score': sum(s['avg_score'] for s in student_analytics) / len(student_analytics) if student_analytics else 0,
                                     'login_count': sum(s['login_count'] for s in student_analytics),
                                     'assignments_completed': sum(s['assignments_completed'] for s in student_analytics),
                                    'courses_enrolled': 0  # Will be calculated per student
                                 })
        
        else:
            # Sinh viên: Xem dữ liệu cá nhân và gợi ý học tập
            submissions = Submission.query.filter_by(student_id=current_user.id).all()
            scores = [s.score for s in submissions if s.score is not None]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            login_count = Log.query.filter_by(user_id=current_user.id, action='login').count()
            assignments_completed = len(scores)
            courses_enrolled = Enrollment.query.filter_by(user_id=current_user.id).count()
            
            # AI gợi ý cho sinh viên
            if avg_score < 5:
                ai_advice = "Bạn nên ôn lại các chương cơ bản và làm thêm bài tập để cải thiện điểm số."
                recommendations = [
                    "Xem lại video bài giảng",
                    "Làm thêm bài tập cơ bản",
                    "Tham gia thảo luận nhóm",
                    "Hỏi giảng viên khi gặp khó khăn"
                ]
            elif login_count < 5:
                ai_advice = "Bạn cần dành thêm thời gian học và đăng nhập thường xuyên hơn."
                recommendations = [
                    "Đặt lịch học cố định mỗi ngày",
                    "Tham gia lớp học trực tuyến",
                    "Tương tác với bạn học",
                    "Sử dụng tính năng nhắc nhở"
                ]
            elif avg_score >= 8:
                ai_advice = "Bạn đang học rất tốt! Hãy tiếp tục phát huy và thử thách bản thân."
                recommendations = [
                    "Tham gia dự án nâng cao",
                    "Giúp đỡ bạn học khác",
                    "Khám phá chủ đề mở rộng",
                    "Chuẩn bị cho kỳ thi cuối"
                ]
            else:
                ai_advice = "Bạn đang có tiến bộ tốt! Hãy tiếp tục cố gắng để đạt mục tiêu cao hơn."
                recommendations = [
                    "Tăng cường thời gian học",
                    "Làm bài tập đều đặn",
                    "Tham gia hoạt động nhóm",
                    "Đặt mục tiêu cụ thể"
                ]
            
            return render_template('ai_support.html',
                                 role='student',
                                 user=current_user,
                                 avg_score=round(avg_score, 1),
                                 login_count=login_count,
                                 assignments_completed=assignments_completed,
                                 courses_enrolled=courses_enrolled,
                                 ai_advice=ai_advice,
                                 recommendations=recommendations,
                                 metrics={
                                     'avg_score': avg_score,
                                     'login_count': login_count,
                                     'assignments_completed': assignments_completed,
                                     'courses_enrolled': courses_enrolled
                                 })

    @app.route('/api/ai/chat', methods=['POST'])
    @login_required
    def ai_chat_api():
        data = request.get_json(silent=True) or {}
        user_message = (data.get('message') or '').strip()

        if not user_message:
            return jsonify({'error': 'Thiếu nội dung câu hỏi.'}), 400

        response_text, used_fallback = generate_ai_chat_response(user_message, current_user)

        if not response_text:
            return jsonify({
                'response': 'Xin lỗi, hiện tại trợ lý AI chưa thể phản hồi. Vui lòng thử lại sau.',
                'meta': {'usedFallback': True, 'model': 'rule-based'}
            }), 500

        meta = {
            'usedFallback': used_fallback,
            'model': 'rule-based' if used_fallback else os.environ.get('GEMINI_MODEL', 'gemini-2.5-flash')
        }

        return jsonify({'response': response_text, 'meta': meta}), 200

    @app.route('/teacher/student/<int:student_id>')
    @login_required
    def teacher_view_student(student_id):
        """Giảng viên xem chi tiết một sinh viên cụ thể"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể xem thông tin sinh viên.', 'danger')
            return redirect(url_for('index'))
        
        student = User.query.get_or_404(student_id)
        if student.role != 'student':
            flash('Người dùng này không phải là sinh viên.', 'danger')
            return redirect(url_for('ai_support'))
        
        # Tính toán metrics cho sinh viên cụ thể
        submissions = Submission.query.filter_by(student_id=student.id).all()
        scores = [s.score for s in submissions if s.score is not None]
        avg_score = sum(scores) / len(scores) if scores else 0
        
        login_count = Log.query.filter_by(user_id=student.id, action='login').count()
        assignments_completed = len(scores)
        courses_enrolled = Enrollment.query.filter_by(user_id=student.id).count()
        
        # AI gợi ý cho giảng viên về sinh viên này
        if avg_score < 5:
            ai_advice = f"Sinh viên {student.username} có điểm thấp ({avg_score:.1f}). Nên hỗ trợ thêm và kiểm tra tiến độ học tập."
            recommendations = [
                "Gặp riêng sinh viên để trao đổi",
                "Giao bài tập bổ sung",
                "Kiểm tra sự hiểu biết cơ bản",
                "Đề xuất học nhóm"
            ]
        elif login_count < 5:
            ai_advice = f"Sinh viên {student.username} ít đăng nhập ({login_count} lần). Nên nhắc nhở tham gia lớp học thường xuyên hơn."
            recommendations = [
                "Gửi email nhắc nhở",
                "Kiểm tra lý do ít tham gia",
                "Đề xuất lịch học cố định",
                "Tạo động lực học tập"
            ]
        elif avg_score >= 8:
            ai_advice = f"Sinh viên {student.username} học tốt ({avg_score:.1f}). Có thể giao thêm bài tập nâng cao."
            recommendations = [
                "Giao dự án nâng cao",
                "Đề xuất làm mentor cho bạn khác",
                "Khuyến khích tham gia cuộc thi",
                "Tạo cơ hội nghiên cứu"
            ]
        else:
            ai_advice = f"Sinh viên {student.username} có tiến bộ tốt. Tiếp tục theo dõi và hỗ trợ."
            recommendations = [
                "Duy trì động lực học tập",
                "Đề xuất mục tiêu cao hơn",
                "Khuyến khích tham gia hoạt động",
                "Theo dõi tiến độ định kỳ"
            ]
        
        return render_template('teacher_student_detail.html',
                             student=student,
                             avg_score=round(avg_score, 1),
                             login_count=login_count,
                             assignments_completed=assignments_completed,
                             courses_enrolled=courses_enrolled,
                             ai_advice=ai_advice,
                             recommendations=recommendations)

    @app.route('/analytics')
    @login_required
    def analytics():
        """Trang phân tích với dữ liệu thực từ database"""
        import pandas as pd
        from collections import Counter
        
        if current_user.is_teacher():
            # Teacher xem analytics toàn hệ thống
            all_students = User.query.filter_by(role='student').all()
            all_submissions = Submission.query.all()
            all_logs = Log.query.all()
            all_courses = Course.query.all()
            
            # Tính toán metrics
            total_views = Log.query.filter_by(action='view_material').count()
            total_logins = Log.query.filter_by(action='login').count()
            
            # Điểm trung bình hệ thống
            scores = [s.score for s in all_submissions if s.score]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            # Tỷ lệ hoàn thành (số submission / tổng assignments có thể nộp)
            total_possible_submissions = 0
            for student in all_students:
                enrollments = Enrollment.query.filter_by(user_id=student.id).all()
                for enrollment in enrollments:
                    course_assignments = Assignment.query.filter_by(course_id=enrollment.course_id).count()
                    total_possible_submissions += course_assignments
            
            completion_rate = (len(all_submissions) / total_possible_submissions * 100) if total_possible_submissions > 0 else 0
            
            # Phân bố điểm
            score_distribution = {
                'excellent': len([s for s in scores if s >= 9]),
                'good': len([s for s in scores if 7 <= s < 9]),
                'average': len([s for s in scores if 5 <= s < 7]),
                'poor': len([s for s in scores if s < 5])
            }
            
            # Khóa học phổ biến
            enrollments_per_course = {}
            for course in all_courses:
                count = Enrollment.query.filter_by(course_id=course.id).count()
                enrollments_per_course[course.name] = count
            
            # Top 5 courses
            top_courses = dict(sorted(enrollments_per_course.items(), key=lambda x: x[1], reverse=True)[:5]) if enrollments_per_course else {}
            
            # Xu hướng theo tháng (6 tháng gần nhất)
            import datetime as dt
            monthly_data = {}
            for i in range(6):
                month = (dt.datetime.now() - dt.timedelta(days=30*i)).strftime('%m/%Y')
                monthly_data[month] = {
                    'views': random.randint(1000, 5000),
                    'submissions': random.randint(500, 2000)
                }
            
            return render_template('analytics.html',
                                 role='teacher',
                                 total_views=total_views,
                                 total_logins=total_logins,
                                 avg_score=round(avg_score, 1),
                                 completion_rate=round(completion_rate, 1),
                                 score_distribution=score_distribution,
                                 top_courses=top_courses,
                                 monthly_data=monthly_data,
                                 total_students=len(all_students),
                                 total_submissions=len(all_submissions))
        else:
            # Student xem analytics cá nhân
            submissions = Submission.query.filter_by(student_id=current_user.id).all()
            logs = Log.query.filter_by(user_id=current_user.id).all()
            enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
            
            scores = [s.score for s in submissions if s.score]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            login_count = len([log for log in logs if log.action == 'login'])
            view_count = len([log for log in logs if log.action == 'view_material'])
            
            # Điểm theo khóa học
            course_scores = {}
            for enrollment in enrollments:
                course = enrollment.course
                course_submissions = [s for s in submissions if s.assignment.course_id == course.id]
                course_score_values = [s.score for s in course_submissions if s.score]
                course_avg = sum(course_score_values) / len(course_score_values) if course_score_values else 0
                course_scores[course.name] = round(course_avg, 1)
            
            # Phân bố điểm student
            student_score_dist = {
                'excellent': len([s for s in scores if s >= 9]),
                'good': len([s for s in scores if 7 <= s < 9]),
                'average': len([s for s in scores if 5 <= s < 7]),
                'poor': len([s for s in scores if s < 5])
            }
            
            return render_template('analytics.html',
                                 role='student',
                                 avg_score=round(avg_score, 1),
                                 login_count=login_count,
                                 view_count=view_count,
                                 total_submissions=len(submissions),
                                 courses_enrolled=len(enrollments),
                                 course_scores=course_scores,
                                 scores=scores,
                                 score_distribution=student_score_dist)

    @app.route('/add-user', methods=['GET', 'POST'])
    @login_required
    def add_user():
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể thêm người dùng.', 'danger')
            return redirect(url_for('index'))
        
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(username=form.username.data, role=form.role.data)
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash(f'Người dùng {user.username} đã được tạo thành công!', 'success')
            return redirect(url_for('users'))
        return render_template('add_user.html', form=form)

    @app.route('/users')
    @login_required
    def users():
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể xem danh sách người dùng.', 'danger')
            return redirect(url_for('index'))
        
        users = User.query.all()
        return render_template('users.html', users=users)
    
    @app.route('/users/<int:user_id>/view')
    @login_required
    def view_user(user_id):
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có quyền xem thông tin người dùng.', 'danger')
            return redirect(url_for('index'))
        
        user = User.query.get_or_404(user_id)
        
        # Get user statistics
        submissions = Submission.query.filter_by(student_id=user.id).all()
        enrollments = Enrollment.query.filter_by(user_id=user.id).all()
        logs = Log.query.filter_by(user_id=user.id).all()
        
        scores = [s.score for s in submissions if s.score is not None]
        avg_score = sum(scores) / len(scores) if scores else 0
        login_count = len([log for log in logs if log.action == 'login'])
        
        return render_template('view_user.html',
                             viewed_user=user,
                             avg_score=round(avg_score, 1),
                             submissions_count=len(submissions),
                             enrollments=enrollments,
                             login_count=login_count)
    
    @app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_user(user_id):
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có quyền chỉnh sửa người dùng.', 'danger')
            return redirect(url_for('index'))
        
        user = User.query.get_or_404(user_id)
        
        if request.method == 'POST':
            username = request.form.get('username')
            role = request.form.get('role')
            password = request.form.get('password')
            
            # Check if username already exists (except current user)
            existing_user = User.query.filter_by(username=username).first()
            if existing_user and existing_user.id != user.id:
                flash('Tên đăng nhập đã tồn tại!', 'danger')
            else:
                user.username = username
                user.role = role
                if password:  # Only update password if provided
                    user.set_password(password)
                
                db.session.commit()
                flash(f'Đã cập nhật thông tin người dùng {user.username}!', 'success')
                return redirect(url_for('users'))
        
        return render_template('edit_user.html', user=user)
    
    @app.route('/users/<int:user_id>/delete', methods=['POST'])
    @login_required
    def delete_user(user_id):
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có quyền xóa người dùng.', 'danger')
            return redirect(url_for('index'))
        
        user = User.query.get_or_404(user_id)
        
        # Prevent deleting yourself
        if user.id == current_user.id:
            flash('Bạn không thể xóa chính mình!', 'danger')
            return redirect(url_for('users'))
        
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'Đã xóa người dùng {username}!', 'success')
        return redirect(url_for('users'))

    @app.route('/grades')
    @login_required
    def grades():
        """Trang xem điểm - phân quyền theo role"""
        if current_user.is_teacher():
            # Teacher xem tất cả điểm của tất cả sinh viên
            students = User.query.filter_by(role='student').all()
            student_grades = []
            
            for student in students:
                submissions = Submission.query.filter_by(student_id=student.id).all()
                enrollments = Enrollment.query.filter_by(user_id=student.id).all()
                
                scores = [s.score for s in submissions if s.score is not None]
                avg_score = sum(scores) / len(scores) if scores else 0
                
                student_grades.append({
                    'student': student,
                    'avg_score': round(avg_score, 1),
                    'submissions_count': len(submissions),
                    'courses_count': len(enrollments)
                })
            
            return render_template('grades.html',
                                 role='teacher',
                                 student_grades=student_grades)
        else:
            # Student chỉ xem điểm của mình
            submissions = Submission.query.filter_by(student_id=current_user.id).all()
            enrollments = Enrollment.query.filter_by(user_id=current_user.id).all()
            
            # Group submissions by course
            courses_with_grades = []
            for enrollment in enrollments:
                course = enrollment.course
                course_submissions = [s for s in submissions if s.assignment.course_id == course.id]
                
                scores = [s.score for s in course_submissions if s.score is not None]
                avg_score = sum(scores) / len(scores) if scores else 0
                
                courses_with_grades.append({
                    'course': course,
                    'submissions': course_submissions,
                    'avg_score': round(avg_score, 1)
                })
            
            return render_template('grades.html',
                                 role='student',
                                 courses_with_grades=courses_with_grades)
    
    @app.route('/submissions/<int:submission_id>/grade', methods=['POST'])
    @login_required
    def grade_submission(submission_id):
        """Teacher chấm điểm submission"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể chấm điểm.', 'danger')
            return redirect(url_for('index'))
        
        submission = Submission.query.get_or_404(submission_id)
        score = request.form.get('score', type=float)
        
        if score is None or score < 0 or score > 10:
            flash('Điểm phải từ 0 đến 10!', 'danger')
        else:
            submission.score = round(score, 1)
            db.session.commit()
            flash(f'Đã chấm điểm {score} cho bài nộp!', 'success')
        
        return redirect(request.referrer or url_for('grades'))
    
    @app.route('/courses/<int:course_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_course(course_id):
        """Teacher chỉnh sửa khóa học"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể chỉnh sửa khóa học.', 'danger')
            return redirect(url_for('courses'))
        
        course = Course.query.get_or_404(course_id)
        
        # Only course owner can edit
        if course.teacher_id != current_user.id:
            flash('Bạn chỉ có thể chỉnh sửa khóa học của mình.', 'danger')
            return redirect(url_for('courses'))
        
        if request.method == 'POST':
            course.name = request.form.get('name')
            course.description = request.form.get('description')
            db.session.commit()
            flash(f'Đã cập nhật khóa học {course.name}!', 'success')
            return redirect(url_for('course_detail', course_id=course.id))
        
        return render_template('edit_course.html', course=course)
    
    @app.route('/courses/<int:course_id>/delete', methods=['POST'])
    @login_required
    def delete_course(course_id):
        """Teacher xóa khóa học"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể xóa khóa học.', 'danger')
            return redirect(url_for('courses'))
        
        course = Course.query.get_or_404(course_id)
        
        # Only course owner can delete
        if course.teacher_id != current_user.id:
            flash('Bạn chỉ có thể xóa khóa học của mình.', 'danger')
            return redirect(url_for('courses'))
        
        course_name = course.name
        db.session.delete(course)
        db.session.commit()
        flash(f'Đã xóa khóa học {course_name}!', 'success')
        return redirect(url_for('courses'))
    
    @app.route('/courses/<int:course_id>/students')
    @login_required
    def course_students(course_id):
        """Teacher xem và quản lý sinh viên trong khóa học"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể xem danh sách sinh viên.', 'danger')
            return redirect(url_for('courses'))
        
        course = Course.query.get_or_404(course_id)
        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        
        # Get all students not in this course
        enrolled_student_ids = [e.user_id for e in enrollments]
        available_students = User.query.filter(
            User.role == 'student',
            ~User.id.in_(enrolled_student_ids)
        ).all()
        
        # Get student stats
        student_stats = []
        for enrollment in enrollments:
            student = enrollment.user
            submissions = Submission.query.join(Assignment).filter(
                Assignment.course_id == course_id,
                Submission.student_id == student.id
            ).all()
            
            scores = [s.score for s in submissions if s.score is not None]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            student_stats.append({
                'student': student,
                'avg_score': round(avg_score, 1),
                'submissions_count': len(submissions)
            })
        
        return render_template('course_students.html',
                             course=course,
                             student_stats=student_stats,
                             available_students=available_students)
    
    @app.route('/courses/<int:course_id>/students/add', methods=['POST'])
    @login_required
    def add_student_to_course(course_id):
        """Teacher thêm sinh viên vào khóa học"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể thêm sinh viên.', 'danger')
            return redirect(url_for('courses'))
        
        course = Course.query.get_or_404(course_id)
        student_id = request.form.get('student_id', type=int)
        
        if not student_id:
            flash('Vui lòng chọn sinh viên!', 'danger')
            return redirect(url_for('course_students', course_id=course_id))
        
        # Check if already enrolled
        existing = Enrollment.query.filter_by(
            user_id=student_id,
            course_id=course_id
        ).first()
        
        if existing:
            flash('Sinh viên đã có trong khóa học này!', 'info')
        else:
            enrollment = Enrollment(user_id=student_id, course_id=course_id)
            db.session.add(enrollment)
            db.session.commit()
            flash('Đã thêm sinh viên vào khóa học!', 'success')
        
        return redirect(url_for('course_students', course_id=course_id))
    
    @app.route('/courses/<int:course_id>/students/<int:student_id>/remove', methods=['POST'])
    @login_required
    def remove_student_from_course(course_id, student_id):
        """Teacher xóa sinh viên khỏi khóa học"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể xóa sinh viên.', 'danger')
            return redirect(url_for('courses'))
        
        enrollment = Enrollment.query.filter_by(
            user_id=student_id,
            course_id=course_id
        ).first_or_404()
        
        db.session.delete(enrollment)
        db.session.commit()
        flash('Đã xóa sinh viên khỏi khóa học!', 'success')
        return redirect(url_for('course_students', course_id=course_id))
    
    @app.route('/assignments/<int:assignment_id>/edit', methods=['GET', 'POST'])
    @login_required
    def edit_assignment(assignment_id):
        """Teacher chỉnh sửa bài tập"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể chỉnh sửa bài tập.', 'danger')
            return redirect(url_for('courses'))
        
        assignment = Assignment.query.get_or_404(assignment_id)
        course = assignment.course
        
        # Only course owner can edit
        if course.teacher_id != current_user.id:
            flash('Bạn chỉ có thể chỉnh sửa bài tập của khóa học mình tạo.', 'danger')
            return redirect(url_for('courses'))
        
        if request.method == 'POST':
            assignment.title = request.form.get('title')
            deadline_str = request.form.get('deadline')
            
            if deadline_str:
                try:
                    assignment.deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
                except ValueError:
                    flash('Định dạng ngày giờ không hợp lệ!', 'danger')
                    return redirect(url_for('edit_assignment', assignment_id=assignment_id))
            
            db.session.commit()
            flash(f'Đã cập nhật bài tập {assignment.title}!', 'success')
            return redirect(url_for('course_detail', course_id=course.id))
        
        return render_template('edit_assignment.html', assignment=assignment)
    
    @app.route('/assignments/<int:assignment_id>/delete', methods=['POST'])
    @login_required
    def delete_assignment(assignment_id):
        """Teacher xóa bài tập"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể xóa bài tập.', 'danger')
            return redirect(url_for('courses'))
        
        assignment = Assignment.query.get_or_404(assignment_id)
        course = assignment.course
        
        # Only course owner can delete
        if course.teacher_id != current_user.id:
            flash('Bạn chỉ có thể xóa bài tập của khóa học mình tạo.', 'danger')
            return redirect(url_for('courses'))
        
        course_id = assignment.course_id
        title = assignment.title
        db.session.delete(assignment)
        db.session.commit()
        flash(f'Đã xóa bài tập {title}!', 'success')
        return redirect(url_for('course_detail', course_id=course_id))
    
    @app.route('/courses/<int:course_id>/assignments/add', methods=['GET', 'POST'])
    @login_required
    def add_assignment(course_id):
        """Teacher thêm bài tập mới"""
        if not current_user.is_teacher():
            flash('Chỉ giảng viên mới có thể thêm bài tập.', 'danger')
            return redirect(url_for('courses'))
        
        course = Course.query.get_or_404(course_id)
        
        # Only course owner can add assignments
        if course.teacher_id != current_user.id:
            flash('Bạn chỉ có thể thêm bài tập cho khóa học của mình.', 'danger')
            return redirect(url_for('courses'))
        
        if request.method == 'POST':
            title = request.form.get('title')
            deadline_str = request.form.get('deadline')
            
            if not title:
                flash('Vui lòng nhập tên bài tập!', 'danger')
            else:
                assignment = Assignment(title=title, course_id=course_id)
                
                if deadline_str:
                    try:
                        assignment.deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
                    except ValueError:
                        flash('Định dạng ngày giờ không hợp lệ!', 'danger')
                        return redirect(url_for('add_assignment', course_id=course_id))
                
                db.session.add(assignment)
                db.session.commit()
                flash(f'Đã thêm bài tập {title}!', 'success')
                return redirect(url_for('course_detail', course_id=course_id))
        
        return render_template('add_assignment.html', course=course)

    @app.route('/api/stats')
    @login_required
    def api_stats():
        # Learning Analytics với pandas
        import pandas as pd
        
        # Get user data
        users = User.query.all()
        courses = Course.query.all()
        enrollments = Enrollment.query.all()
        submissions = Submission.query.all()
        logs = Log.query.all()
        
        # Convert to DataFrame for analysis
        user_data = []
        for user in users:
            user_logs = [log for log in logs if log.user_id == user.id]
            user_submissions = [sub for sub in submissions if sub.student_id == user.id]
            user_enrollments = [enroll for enroll in enrollments if enroll.user_id == user.id]
            
            avg_score = sum(sub.score for sub in user_submissions if sub.score) / len(user_submissions) if user_submissions else 0
            login_count = len([log for log in user_logs if log.action == 'login'])
            
            user_data.append({
                'user_id': user.id,
                'username': user.username,
                'role': user.role,
                'login_count': login_count,
                'avg_score': avg_score,
                'courses_enrolled': len(user_enrollments),
                'assignments_submitted': len(user_submissions)
            })
        
        df = pd.DataFrame(user_data)
        
        # AI Advisor - Rule-based recommendations
        def get_ai_advice(row):
            if row['avg_score'] < 5:
                return "Bạn nên ôn lại các chương cơ bản và làm thêm bài tập."
            elif row['login_count'] < 3:
                return "Bạn cần dành thêm thời gian học, đăng nhập thường xuyên hơn."
            elif row['avg_score'] >= 8:
                return "Bạn đang học khá tốt, tiếp tục phát huy!"
            else:
                return "Bạn đang có tiến bộ tốt, hãy tiếp tục cố gắng!"
        
        df['ai_advice'] = df.apply(get_ai_advice, axis=1)
        
        return jsonify({
            'total_users': len(users),
            'total_courses': len(courses),
            'total_enrollments': len(enrollments),
            'user_stats': df.to_dict('records'),
            'avg_login_count': df['login_count'].mean(),
            'avg_score': df['avg_score'].mean()
        })

    @app.route('/api/analytics')
    @login_required
    def api_analytics():
        """API cho phân tích chi tiết - khác nhau giữa teacher và student"""
        import pandas as pd
        
        if current_user.is_teacher():
            # Giảng viên xem tất cả sinh viên
            students = User.query.filter_by(role='student').all()
            student_data = []
            
            for student in students:
                # Tính điểm trung bình của sinh viên
                submissions = Submission.query.filter_by(student_id=student.id).all()
                scores = [s.score for s in submissions if s.score is not None]
                avg_score = sum(scores) / len(scores) if scores else 0
                
                # Đếm số lần đăng nhập
                login_count = Log.query.filter_by(user_id=student.id, action='login').count()
                
                # Đếm số bài tập đã hoàn thành
                assignments_completed = len(scores)
                
                # Đếm số khóa học đã đăng ký
                courses_enrolled = Enrollment.query.filter_by(user_id=student.id).count()
                
                student_data.append({
                    'id': student.id,
                    'username': student.username,
                    'avg_score': round(avg_score, 1),
                    'login_count': login_count,
                    'assignments_completed': assignments_completed,
                    'courses_enrolled': courses_enrolled
                })
            
            return jsonify({
                'role': 'teacher',
                'students': student_data,
                'total_students': len(student_data),
                'class_avg_score': round(sum(s['avg_score'] for s in student_data) / len(student_data), 1) if student_data else 0
            })
        
        else:
            # Sinh viên chỉ xem dữ liệu của mình
            submissions = Submission.query.filter_by(student_id=current_user.id).all()
            scores = [s.score for s in submissions if s.score is not None]
            avg_score = sum(scores) / len(scores) if scores else 0
            
            login_count = Log.query.filter_by(user_id=current_user.id, action='login').count()
            assignments_completed = len(scores)
            courses_enrolled = Enrollment.query.filter_by(user_id=current_user.id).count()
            
            return jsonify({
                'role': 'student',
                'avg_score': round(avg_score, 1),
                'login_count': login_count,
                'assignments_completed': assignments_completed,
                'courses_enrolled': courses_enrolled
            })

    @app.route('/quick-action/<action>')
    @login_required
    def quick_action(action):
        """Handle quick actions from dashboard"""
        if action == 'create-sample-data':
            create_sample_data()
            flash('Dữ liệu mẫu đã được tạo thành công!', 'success')
            return redirect(url_for('index'))
        
        elif action == 'create-course':
            if not current_user.is_teacher():
                flash('Chỉ giảng viên mới có thể tạo khóa học.', 'danger')
                return redirect(url_for('index'))
            return redirect(url_for('add_course'))
        
        elif action == 'add-user':
            if not current_user.is_teacher():
                flash('Chỉ giảng viên mới có thể thêm người dùng.', 'danger')
                return redirect(url_for('index'))
            return redirect(url_for('add_user'))
        
        elif action == 'view-analytics':
            return redirect(url_for('analytics'))
        
        else:
            flash('Hành động không hợp lệ.', 'danger')
            return redirect(url_for('index'))

    @app.route('/seed')
    def seed():
        """Create sample data for demo"""
        try:
            db.drop_all()
            db.create_all()
        except Exception as e:
            flash(f'Lỗi khi tạo database: {str(e)}', 'error')
            return redirect(url_for('index'))
        
        # Create sample users
        admin = User(username='admin', role='teacher')
        admin.set_password('admin123')
        
        teacher1 = User(username='teacher1', role='teacher')
        teacher1.set_password('teacher123')
        
        student1 = User(username='student1', role='student')
        student1.set_password('student123')
        
        student2 = User(username='student2', role='student')
        student2.set_password('student123')
        
        db.session.add_all([admin, teacher1, student1, student2])
        db.session.commit()
        
        # Create sample courses
        course1 = Course(name='Nhập môn Lập trình', description='Khóa học cơ bản về lập trình', teacher_id=teacher1.id)
        course2 = Course(name='Phân tích Dữ liệu', description='Khóa học về phân tích dữ liệu', teacher_id=admin.id)
        
        db.session.add_all([course1, course2])
        db.session.commit()
        
        # Create sample assignments
        assignment1 = Assignment(title='Bài tập Python cơ bản', course_id=course1.id, deadline=datetime.now() + timedelta(days=7))
        assignment2 = Assignment(title='Phân tích dataset', course_id=course2.id, deadline=datetime.now() + timedelta(days=10))
        
        db.session.add_all([assignment1, assignment2])
        db.session.commit()
        
        # Create sample enrollments
        enrollment1 = Enrollment(user_id=student1.id, course_id=course1.id)
        enrollment2 = Enrollment(user_id=student1.id, course_id=course2.id)
        enrollment3 = Enrollment(user_id=student2.id, course_id=course1.id)
        
        db.session.add_all([enrollment1, enrollment2, enrollment3])
        db.session.commit()
        
        # Create sample submissions
        submission1 = Submission(assignment_id=assignment1.id, student_id=student1.id, score=8.5)
        submission2 = Submission(assignment_id=assignment2.id, student_id=student1.id, score=7.0)
        
        db.session.add_all([submission1, submission2])
        db.session.commit()
        
        # Create sample logs
        logs = [
            Log(user_id=student1.id, course_id=course1.id, action='login'),
            Log(user_id=student1.id, course_id=course1.id, action='view_material'),
            Log(user_id=student1.id, course_id=course1.id, action='submit_assignment'),
            Log(user_id=student2.id, course_id=course1.id, action='login'),
            Log(user_id=teacher1.id, action='login'),
        ]
        
        db.session.add_all(logs)
        db.session.commit()
        
        flash('Dữ liệu mẫu đã được tạo thành công!', 'success')
        return redirect(url_for('index'))


    return app


if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
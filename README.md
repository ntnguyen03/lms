# EduLearn - Hệ thống LMS đơn giản

## Mô tả
Hệ thống quản lý học tập trực tuyến (LMS) được xây dựng với Flask, theo đúng pipeline đã đề xuất.

## Công nghệ sử dụng
- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Chart.js
- **Authentication**: Flask-Login
- **Data Analysis**: Pandas
- **AI**: Rule-based recommendations

## Cấu trúc Database
Theo đúng pipeline đề xuất:

### Bảng chính:
- `users` (id, username, password, role)
- `courses` (id, name, description, teacher_id)
- `enrollments` (user_id, course_id)
- `assignments` (id, course_id, title, deadline)
- `submissions` (id, assignment_id, student_id, score)
- `logs` (id, user_id, course_id, action, timestamp)

## Chức năng chính

### 1. Quản lý người dùng
- ✅ Đăng ký/Đăng nhập với phân quyền (student/teacher)
- ✅ Authentication và session management
- ✅ Password hashing bảo mật

### 2. Quản lý khóa học
- ✅ Giảng viên: tạo khóa học, thêm bài tập
- ✅ Sinh viên: đăng ký khóa học, nộp bài tập
- ✅ Xem chi tiết khóa học và bài tập

### 3. Ghi log học tập
- ✅ Log đăng nhập, xem tài liệu, nộp bài
- ✅ Tracking hoạt động học tập

### 4. Learning Analytics
- ✅ Sử dụng pandas để phân tích dữ liệu
- ✅ Các chỉ số: điểm trung bình, số lần đăng nhập, tiến độ hoàn thành
- ✅ Biểu đồ tương tác với Chart.js

### 5. AI tư vấn học tập (Rule-based)
```python
def advice(score, login_count):
    if score < 5:
        return "Bạn nên ôn lại các chương cơ bản và làm thêm bài tập."
    elif login_count < 3:
        return "Bạn cần dành thêm thời gian học, đăng nhập thường xuyên hơn."
    else:
        return "Bạn đang học khá tốt, tiếp tục phát huy!"
```

## Cài đặt và chạy

### 1. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 2. Chạy ứng dụng
```bash
python app.py
```

### 3. Truy cập ứng dụng
- URL: `http://localhost:5000`
- Tạo dữ liệu mẫu: Truy cập `/seed`

## Tài khoản demo

### Giảng viên:
- Username: `teacher1`
- Password: `teacher123`

### Sinh viên:
- Username: `student1`
- Password: `student123`

### Admin:
- Username: `admin`
- Password: `admin123`

## API Endpoints

### Authentication
- `GET /login` - Trang đăng nhập
- `POST /login` - Xử lý đăng nhập
- `GET /register` - Trang đăng ký
- `POST /register` - Xử lý đăng ký
- `GET /logout` - Đăng xuất

### Courses
- `GET /courses` - Danh sách khóa học
- `GET /courses/add` - Form thêm khóa học
- `POST /courses/add` - Tạo khóa học
- `GET /courses/<id>` - Chi tiết khóa học
- `GET /courses/<id>/enroll` - Đăng ký khóa học

### Assignments
- `GET /assignments/<id>/submit` - Form nộp bài
- `POST /assignments/<id>/submit` - Nộp bài tập

### Analytics
- `GET /analytics` - Trang phân tích
- `GET /api/stats` - API thống kê và AI recommendations

## Tính năng AI

### Rule-based Recommendations
Hệ thống phân tích dữ liệu học tập và đưa ra gợi ý dựa trên:
- Điểm số trung bình
- Số lần đăng nhập
- Tiến độ hoàn thành bài tập

### Learning Analytics
- Thống kê tổng quan
- Biểu đồ tương tác
- Phân tích xu hướng học tập
- Đánh giá rủi ro học tập

## Cấu trúc thư mục
```
chuyen_doi_so/
├── app.py              # Flask application chính
├── models.py           # Database models
├── forms.py            # WTForms
├── analytics.py        # Data analysis với pandas
├── database.py         # Database configuration
├── requirements.txt    # Dependencies
├── templates/         # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── courses.html
│   ├── course_detail.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── ...
└── static/            # CSS, JS, images
```

## Demo và Testing

1. **Tạo dữ liệu mẫu**: Truy cập `/seed`
2. **Đăng nhập**: Sử dụng tài khoản demo
3. **Tạo khóa học**: Giảng viên tạo khóa học
4. **Đăng ký khóa học**: Sinh viên đăng ký
5. **Nộp bài tập**: Sinh viên nộp bài và nhận điểm
6. **Xem analytics**: Phân tích dữ liệu và AI recommendations

## Mở rộng trong tương lai

### ML nâng cao
- Thu thập dữ liệu log + điểm
- Huấn luyện mô hình Logistic Regression
- Dự đoán nguy cơ rớt học
- Gợi ý cá nhân hóa

### Tính năng bổ sung
- File upload cho bài tập
- Chat system
- Notification system
- Mobile app

## Lưu ý
- Hệ thống được thiết kế đơn giản, dễ hiểu và dễ mở rộng
- Phù hợp cho bài tập lớn và demo
- Code được tổ chức theo đúng pipeline đề xuất
- Sẵn sàng để đi thi cuối kỳ
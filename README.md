<h2 align="center">
    <a href="https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin">
    🎓 Faculty of Information Technology (DaiNam University)
    </a>
</h2>
<h2 align="center">
   XÂY DỰNG NỀN TẢNG SỐ HỖ TRỢ HỌC TẬP CHO SINH VIÊN DỰA TRÊN LMS VÀ PHÂN TÍCH DỮ LIỆU
</h2>
<div align="center">
    <p align="center">
        <img src="docs/aiotlab_logo.png" alt="AIoTLab Logo" width="170"/>
        <img src="docs/fitdnu_logo.png" alt="AIoTLab Logo" width="180"/>
        <img src="docs/dnu_logo.png" alt="DaiNam University Logo" width="200"/>
    </p>

[![AIoTLab](https://img.shields.io/badge/AIoTLab-green?style=for-the-badge)](https://www.facebook.com/DNUAIoTLab)
[![Faculty of Information Technology](https://img.shields.io/badge/Faculty%20of%20Information%20Technology-blue?style=for-the-badge)](https://dainam.edu.vn/vi/khoa-cong-nghe-thong-tin)
[![DaiNam University](https://img.shields.io/badge/DaiNam%20University-orange?style=for-the-badge)](https://dainam.edu.vn)

</div>

# 📓📚 XÂY DỰNG NỀN TẢNG SỐ HỖ TRỢ HỌC TẬP CHO SINH VIÊN DỰA TRÊN LMS VÀ PHÂN TÍCH DỮ LIỆU

## 📖 1. Giới thiệu
Hệ thống quản lý học tập trực tuyến (LMS) được xây dựng với Flask, theo đúng pipeline đã đề xuất.

---

## 🔧 2. Công nghệ sử dụng
<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
    <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
    <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
    <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js"/>
</p>

- **Backend**: Flask (Python)
- **Database**: SQLite
- **Frontend**: Bootstrap 5, Chart.js
- **Authentication**: Flask-Login
- **Data Analysis**: Pandas
- **AI**: Rule-based recommendations

---

## 🚀 3. Các chức năng chính

### 1. 👤 Quản lý người dùng
- ✅ Đăng ký/Đăng nhập với phân quyền (student/teacher)
- ✅ Authentication và session management
- ✅ Password hashing bảo mật

### 2. 📚 Quản lý khóa học
- ✅ Giảng viên: tạo khóa học, thêm bài tập
- ✅ Sinh viên: đăng ký khóa học, nộp bài tập
- ✅ Xem chi tiết khóa học và bài tập

### 3. 📝 Ghi log học tập
- ✅ Log đăng nhập, xem tài liệu, nộp bài
- ✅ Tracking hoạt động học tập

### 4. 📊 Learning Analytics
- ✅ Sử dụng pandas để phân tích dữ liệu
- ✅ Các chỉ số: điểm trung bình, số lần đăng nhập, tiến độ hoàn thành
- ✅ Biểu đồ tương tác với Chart.js

### 5. 💡 AI tư vấn học tập (Rule-based)
```python
def advice(score, login_count):
    if score < 5:
        return "Bạn nên ôn lại các chương cơ bản và làm thêm bài tập."
    elif login_count < 3:
        return "Bạn cần dành thêm thời gian học, đăng nhập thường xuyên hơn."
    else:
        return "Bạn đang học khá tốt, tiếp tục phát huy!"
```
📂 4. Cấu trúc thư mục
```Bash

chuyen_doi_so/
├── app.py              # Flask application chính
├── models.py           # Database models
├── forms.py            # WTForms
├── analytics.py        # Data analysis với pandas
├── database.py         # Database configuration
├── requirements.txt    # Dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── courses.html
│   ├── course_detail.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   └── ...
└── static/             # CSS, JS, images
```
## ▶️ 5. Cài đặt và chạy
###1. Cài đặt dependencies
Bash

pip install -r requirements.txt
###2. Chạy ứng dụng
Bash

python app.py
###3. Truy cập ứng dụng
URL: http://localhost:5000

Tạo dữ liệu mẫu: Truy cập /seed

##🧑‍💻 6. Tài khoản demo
Giảng viên:
Username: teacher1

Password: teacher123

Sinh viên:
Username: student1

Password: student123

Admin:
Username: admin

Password: admin123

##🔌 7. API Endpoints
Authentication
GET /login - Trang đăng nhập

POST /login - Xử lý đăng nhập

GET /register - Trang đăng ký

POST /register - Xử lý đăng ký

GET /logout - Đăng xuất

Courses
GET /courses - Danh sách khóa học

GET /courses/add - Form thêm khóa học

POST /courses/add - Tạo khóa học

GET /courses/<id> - Chi tiết khóa học

GET /courses/<id>/enroll - Đăng ký khóa học

Assignments
GET /assignments/<id>/submit - Form nộp bài

POST /assignments/<id>/submit - Nộp bài tập

Analytics
GET /analytics - Trang phân tích

GET /api/stats - API thống kê và AI recommendations

##🤖 8. Tính năng AI
Rule-based Recommendations
Hệ thống phân tích dữ liệu học tập và đưa ra gợi ý dựa trên:

Điểm số trung bình

Số lần đăng nhập

Tiến độ hoàn thành bài tập

Learning Analytics
Thống kê tổng quan

Biểu đồ tương tác

Phân tích xu hướng học tập

Đánh giá rủi ro học tập

##🧪 9. Demo và Testing
Tạo dữ liệu mẫu: Truy cập /seed

Đăng nhập: Sử dụng tài khoản demo

Tạo khóa học: Giảng viên tạo khóa học

Đăng ký khóa học: Sinh viên đăng ký

Nộp bài tập: Sinh viên nộp bài và nhận điểm

Xem analytics: Phân tích dữ liệu và AI recommendations

##🔮 10. Mở rộng trong tương lai
ML nâng cao
Thu thập dữ liệu log + điểm

Huấn luyện mô hình Logistic Regression

Dự đoán nguy cơ rớt học

Gợi ý cá nhân hóa

Tính năng bổ sung
File upload cho bài tập

Chat system

Notification system

Mobile app

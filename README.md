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

# 📓📚 Xây dựng nền tảng số hỗ trợ học tập cho sinh viên dựa trên LMS và phân tích dữ liệu

## 1. Giới thiệu
Hệ thống quản lý học tập trực tuyến (LMS) được xây dựng với Flask, theo đúng pipeline đã đề xuất. Ứng dụng cung cấp các chức năng chính như:
* Quản lý người dùng (phân quyền Student/Teacher).
* Giảng viên tạo và quản lý khóa học, bài tập.
* Sinh viên đăng ký khóa học, nộp bài và xem điểm.
* Tích hợp Learning Analytics (phân tích dữ liệu học tập) với Chart.js.
* Tích hợp AI tư vấn học tập (Rule-based) để đưa ra gợi ý.

## 2. Ngôn ngữ lập trình sử dụng
<p align="center">
    <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
    <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask"/>
    <img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white" alt="SQLite"/>
    <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
    <img src="https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white" alt="Bootstrap"/>
    <img src="https://img.shields.io/badge/Chart.js-FF6384?style=for-the-badge&logo=chartdotjs&logoColor=white" alt="Chart.js"/>
</p>

**Công nghệ sử dụng**
* **Backend**: Flask (Python)
* **Database**: SQLite
* **Frontend**: Bootstrap 5, Chart.js
* **Authentication**: Flask-Login
* **Data Analysis**: Pandas
* **AI**: Rule-based recommendations (Google AI Studio)

## 3. Hình ảnh các chức năng
Giao diện Dashboard
<img width="1904" height="911" alt="Screenshot 2025-11-12 220733" src="https://github.com/user-attachments/assets/58391f1d-f1c5-4421-a201-c2ee03a69854" />
Giao diện quản lý khóa học
<img width="1903" height="912" alt="Screenshot 2025-11-12 221518" src="https://github.com/user-attachments/assets/15877729-5fb7-4ada-b662-c2a0c1081af7" />
Giao diện quản lý điểm số
<img width="1905" height="911" alt="Screenshot 2025-11-12 221551" src="https://github.com/user-attachments/assets/3d8d59fb-b3b4-49bc-b05b-c2d2aa269f97" />
Giao diện chức năng phân tích sinh viên
<img width="1899" height="910" alt="Screenshot 2025-11-12 221627" src="https://github.com/user-attachments/assets/b0d30a47-b212-4217-85a8-fc1d474d7057" />
Giao diện AI hỗ trợ (Giảng viên, Sinh viên)
<img width="1904" height="908" alt="Screenshot 2025-11-12 221635" src="https://github.com/user-attachments/assets/44ff0839-e06b-485a-98c0-53affcefa8e2" />


## 4. Cách chạy chương trình

**1. Cài đặt dependencies**
```bash
pip install -r requirements.txt
```
**2. Chạy ứng dụng**

```Bash

python app.py
```
**3. Truy cập ứng dụng**

URL: http://localhost:5000

Tạo dữ liệu mẫu: Truy cập /seed (hoặc /quick-action/create-sample-data)

**4. Tài khoản demo**

Giảng viên: Username: teacher1 / Password: teacher123

Sinh viên: Username: student1 / Password: student123

Admin: Username: admin / Password: admin123

## 5. Ghi chú

Hệ thống được thiết kế đơn giản, dễ hiểu và dễ mở rộng.

Code được tổ chức theo đúng pipeline đề xuất.

Hệ thống AI ban đầu dựa trên luật (rule-based), có thể mở rộng tích hợp ML nâng cao (ví dụ: Logistic Regression) để dự đoán nguy cơ rớt học, chatbot tích hợp Google Gemini API để trả lời câu hỏi

## 📝 Thông tin cá nhân
- Nguyễn Trường Nam - CNTT 16-03
- Email: truongnam0304@gmail.com
- Phone: 0397367184
© 2025 AIoTLab, Faculty of Information Technology, DaiNam University. All rights reserved.


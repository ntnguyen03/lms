# 🤖 HƯỚNG DẪN SỬ DỤNG GOOGLE GEMINI API

## 📋 Tổng Quan

Hệ thống EduLearn đã được tích hợp với **Google Gemini API** để cung cấp tính năng AI hỗ trợ học tập thông minh. Gemini là mô hình AI mạnh mẽ của Google, hỗ trợ tiếng Việt và có khả năng hiểu ngữ cảnh tốt.

---

## 🔑 Bước 1: Lấy API Key từ Google

### 1.1. Truy cập Google AI Studio

1. Mở trình duyệt và truy cập: **https://aistudio.google.com/**
2. Đăng nhập bằng tài khoản Google của bạn

### 1.2. Tạo API Key

1. Trong Google AI Studio, click vào menu **"Get API key"** (hoặc icon khóa 🔑)
2. Chọn **"Create API key"**
3. Chọn project Google Cloud của bạn (hoặc tạo project mới)
4. Click **"Create API key in new project"** hoặc **"Create API key in existing project"**
5. **Sao chép API key** được tạo (bạn sẽ chỉ thấy một lần, hãy lưu lại ngay!)

### 1.3. Lưu ý Bảo Mật

⚠️ **QUAN TRỌNG**: 
- Không chia sẻ API key với người khác
- Không commit API key lên Git/GitHub
- API key có giới hạn sử dụng miễn phí, sau đó sẽ tính phí

---

## 📦 Bước 2: Cài Đặt Thư Viện

### 2.1. Kiểm tra requirements.txt

Đảm bảo file `requirements.txt` có dòng:
```
google-generativeai>=0.5.0
```

### 2.2. Cài Đặt

Mở terminal/command prompt và chạy:

```bash
pip install google-generativeai
```

Hoặc cài đặt tất cả dependencies:

```bash
pip install -r requirements.txt
```

### 2.3. Kiểm Tra Cài Đặt

Chạy Python và test:

```python
import google.generativeai as genai
print("✅ Google Generative AI đã được cài đặt thành công!")
```

---

## ⚙️ Bước 3: Cấu Hình API Key

### 3.1. Tạo File .env

Trong thư mục gốc của project, tạo file `.env` (nếu chưa có):

```bash
# Windows
type nul > .env

# Linux/Mac
touch .env
```

### 3.2. Thêm API Key vào .env

Mở file `.env` và thêm:

```env
# Google Gemini API Configuration
GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-pro
```

**Thay thế `your_api_key_here`** bằng API key bạn đã lấy ở Bước 1.

### 3.3. Các Model Gemini Có Sẵn

Bạn có thể thay đổi model trong file `.env`. Code sẽ tự động thử các model khác nếu model bạn chọn không hoạt động:

**Model mới nhất (Gemini 2.5) - Khuyến nghị:**
- `gemini-2.5-flash` - ⭐ **Mặc định** - Model mới nhất, nhanh và hiệu quả nhất
- `gemini-flash-latest` - Alias cho gemini-2.5-flash (luôn trỏ đến version mới nhất)
- `gemini-2.5-pro` - Model mạnh nhất, phù hợp cho tác vụ phức tạp và reasoning

**Model cũ (Fallback):**
- `gemini-1.5-flash` - Fallback nếu 2.5 không có
- `gemini-1.5-pro` - Fallback cho tác vụ phức tạp

**Lưu ý**: 
- Hệ thống sẽ tự động thử các model theo thứ tự từ mới nhất đến cũ
- Khuyến nghị dùng `gemini-2.5-flash` hoặc `gemini-flash-latest` để có hiệu suất tốt nhất

### 3.4. Ví Dụ File .env Hoàn Chỉnh

```env
# Flask Configuration
# SECRET_KEY: Dùng để mã hóa session, cookies, flash messages
# Tạo một chuỗi ngẫu nhiên dài (ít nhất 32 ký tự)
# Ví dụ: python -c "import secrets; print(secrets.token_hex(32))"
SECRET_KEY=your-secret-key-here-change-this-to-random-string

# DATABASE_URL: Đường dẫn đến database
# sqlite:///lms.db = dùng SQLite, file database tên là lms.db
# Bạn có thể để mặc định hoặc thay đổi tên file
DATABASE_URL=sqlite:///lms.db

# Google Gemini API
GEMINI_API_KEY=AIzaSyBxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
GEMINI_MODEL=gemini-2.5-flash
```

#### Giải Thích Chi Tiết:

**1. SECRET_KEY là gì?**
- `SECRET_KEY` là một chuỗi bí mật dùng để mã hóa dữ liệu trong Flask
- Dùng cho: session cookies, flash messages, CSRF protection
- ⚠️ **QUAN TRỌNG**: Phải là chuỗi ngẫu nhiên, không được để mặc định trong production
- **Cách tạo SECRET_KEY ngẫu nhiên:**
  ```bash
  # Windows PowerShell
  python -c "import secrets; print(secrets.token_hex(32))"
  
  # Hoặc Python
  python
  >>> import secrets
  >>> secrets.token_hex(32)
  ```
  Kết quả sẽ là một chuỗi dài như: `a1b2c3d4e5f6...` (64 ký tự hex)

**2. DATABASE_URL là gì?**
- `DATABASE_URL` là đường dẫn đến file database
- `sqlite:///lms.db` nghĩa là:
  - `sqlite:///` = sử dụng SQLite (database file đơn giản)
  - `lms.db` = tên file database (sẽ được tạo tự động trong thư mục `instance/`)
- **Bạn có thể:**
  - Để trống → dùng mặc định `sqlite:///lms.db`
  - Hoặc thay đổi tên: `sqlite:///my_database.db`
  - Hoặc dùng PostgreSQL/MySQL: `postgresql://user:pass@localhost/dbname`

**3. Có bắt buộc phải thêm không?**
- **SECRET_KEY**: Nên thêm, nhưng nếu không có, app sẽ dùng `'dev-secret'` (không an toàn cho production)
- **DATABASE_URL**: Không bắt buộc, nếu không có sẽ dùng mặc định `sqlite:///lms.db`
- **GEMINI_API_KEY**: ⚠️ **BẮT BUỘC** nếu muốn dùng tính năng AI

---

## 🚀 Bước 4: Chạy Ứng Dụng

### 4.1. Khởi Động Server

```bash
python app.py
```

### 4.2. Kiểm Tra Kết Nối

1. Mở trình duyệt: `http://localhost:5000`
2. Đăng nhập với tài khoản
3. Vào **"AI Hỗ trợ"** hoặc **"Chat với AI"**
4. Gửi một câu hỏi test, ví dụ: "Làm sao để cải thiện điểm số?"

Nếu AI phản hồi được, bạn đã cấu hình thành công! ✅

---

## 🔍 Bước 5: Kiểm Tra Lỗi

### 5.1. Lỗi "GEMINI_API_KEY chưa được cấu hình"

**Nguyên nhân**: File `.env` không có API key hoặc không được load

**Giải pháp**:
1. Kiểm tra file `.env` có tồn tại trong thư mục gốc
2. Kiểm tra tên biến: `GEMINI_API_KEY` (chính xác, không có khoảng trắng)
3. Đảm bảo đã cài `python-dotenv`: `pip install python-dotenv`

### 5.2. Lỗi "Google Generative AI SDK chưa được cài đặt"

**Nguyên nhân**: Chưa cài thư viện `google-generativeai`

**Giải pháp**:
```bash
pip install google-generativeai
```

### 5.3. Lỗi "404 models/gemini-pro is not found"

**Nguyên nhân**: Tên model không còn được hỗ trợ hoặc không đúng

**Giải pháp**:
1. ✅ **Đã được sửa tự động**: Code sẽ tự động thử các model khác
2. Hoặc cập nhật file `.env`:
   ```env
   GEMINI_MODEL=gemini-2.5-flash
   ```
3. Các model được hỗ trợ (từ mới nhất đến cũ):
   - `gemini-2.5-flash` ⭐ (khuyến nghị - mới nhất)
   - `gemini-flash-latest` (luôn trỏ đến version mới nhất)
   - `gemini-2.5-pro` (cho tác vụ phức tạp)
   - `gemini-1.5-flash` (fallback)
   - `gemini-1.5-pro` (fallback)

### 5.4. Lỗi "API key không hợp lệ"

**Nguyên nhân**: API key sai hoặc đã bị vô hiệu hóa

**Giải pháp**:
1. Kiểm tra lại API key trong Google AI Studio
2. Tạo API key mới nếu cần
3. Đảm bảo không có khoảng trắng thừa trong `.env`

### 5.5. Lỗi "Quota exceeded" hoặc "Rate limit"

**Nguyên nhân**: Đã vượt quá giới hạn sử dụng miễn phí

**Giải pháp**:
1. Kiểm tra quota trong Google Cloud Console
2. Nâng cấp tài khoản hoặc đợi reset quota
3. Tối ưu số lượng request

---

## 📊 Bước 6: Tùy Chỉnh Cấu Hình

### 6.1. Thay Đổi Tham Số AI

Trong file `app.py`, tìm function `call_external_ai_model()` và chỉnh sửa:

```python
generation_config=genai.types.GenerationConfig(
    temperature=0.4,      # Độ sáng tạo (0.0-1.0), thấp = chính xác hơn
    top_p=0.9,            # Độ đa dạng (0.0-1.0)
    max_output_tokens=512, # Số token tối đa (1-8192)
)
```

**Giải thích tham số**:
- **temperature**: 
  - `0.0-0.3`: Phản hồi chính xác, nhất quán (phù hợp cho giáo dục)
  - `0.4-0.7`: Cân bằng (mặc định)
  - `0.8-1.0`: Sáng tạo, đa dạng hơn

- **top_p**: Kiểm soát độ đa dạng từ vựng
- **max_output_tokens**: Giới hạn độ dài phản hồi

### 6.2. Thay Đổi System Prompt

Tìm dòng trong `app.py`:

```python
system_prompt = (
    "Bạn là trợ lý AI bằng tiếng Việt, hỗ trợ {role} trong môi trường giáo dục đại học. "
    "Phản hồi ngắn gọn, súc tích, đưa ra gợi ý thực tế dựa trên dữ liệu học tập khi có."
).format(role='giảng viên' if role == 'teacher' else 'sinh viên')
```

Bạn có thể chỉnh sửa để thay đổi phong cách phản hồi của AI.

---

## 💰 Giá Cả & Giới Hạn

### Miễn Phí (Free Tier)

Google Gemini cung cấp gói miễn phí với giới hạn:
- **60 requests/phút** (RPM)
- **1,500 requests/ngày** (RPD)
- Đủ cho hầu hết các ứng dụng nhỏ và vừa

### Trả Phí

Nếu vượt quá giới hạn miễn phí:
- Xem chi tiết tại: https://ai.google.dev/pricing
- Có thể thiết lập budget alerts trong Google Cloud Console

---

## 🧪 Test API Key

### Script Test Đơn Giản

Tạo file `test_gemini.py`:

```python
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

api_key = os.environ.get('GEMINI_API_KEY')
if not api_key:
    print("❌ GEMINI_API_KEY chưa được cấu hình trong .env")
    exit(1)

try:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("Xin chào, bạn có thể nói tiếng Việt không?")
    print("✅ Kết nối thành công!")
    print(f"📝 Phản hồi: {response.text}")
except Exception as e:
    print(f"❌ Lỗi: {e}")
```

Chạy test:
```bash
python test_gemini.py
```

---

## 📚 Tài Liệu Tham Khảo

- **Google AI Studio**: https://aistudio.google.com/
- **Gemini API Documentation**: https://ai.google.dev/docs
- **Python SDK**: https://github.com/google/generative-ai-python
- **Pricing**: https://ai.google.dev/pricing

---

## 🎯 Tính Năng AI Trong Ứng Dụng

### Cho Sinh Viên:
- ✅ Gợi ý học tập cá nhân hóa
- ✅ Phân tích điểm số và đưa ra lời khuyên
- ✅ Chat trực tiếp với AI trợ lý
- ✅ Đề xuất cải thiện kỹ năng

### Cho Giảng Viên:
- ✅ Phân tích hiệu suất lớp học
- ✅ Gợi ý hỗ trợ sinh viên yếu
- ✅ Đề xuất bài tập nâng cao cho sinh viên giỏi
- ✅ Chat với AI để tư vấn quản lý lớp

---

## 🔒 Bảo Mật

### Best Practices:

1. ✅ **Không commit `.env` lên Git**
   - Thêm `.env` vào `.gitignore`
   - Sử dụng `.env.example` để chia sẻ cấu trúc

2. ✅ **Rotate API Key định kỳ**
   - Thay đổi API key mỗi 3-6 tháng
   - Vô hiệu hóa key cũ khi tạo key mới

3. ✅ **Giới hạn IP (nếu có)**
   - Trong Google Cloud Console, có thể giới hạn IP truy cập

4. ✅ **Monitor Usage**
   - Theo dõi số lượng request trong Google Cloud Console
   - Thiết lập alerts khi gần đạt quota

---

## ❓ FAQ

**Q: API key có hết hạn không?**  
A: Không, nhưng bạn có thể vô hiệu hóa hoặc xóa trong Google Cloud Console.

**Q: Có thể dùng nhiều API key không?**  
A: Có, nhưng trong code hiện tại chỉ dùng một key. Có thể mở rộng để load balancing.

**Q: Làm sao để tăng giới hạn?**  
A: Nâng cấp tài khoản Google Cloud hoặc liên hệ Google support.

**Q: Có thể dùng Gemini offline không?**  
A: Không, Gemini API yêu cầu kết nối internet.

**Q: Model nào tốt nhất cho giáo dục?**  
A: `gemini-2.5-flash` hoặc `gemini-flash-latest` là lựa chọn tốt nhất hiện tại - nhanh, chính xác và hiệu quả. Nếu cần xử lý phức tạp hơn (coding, reasoning), dùng `gemini-2.5-pro`.

---

## 🎉 Hoàn Thành!

Bây giờ bạn đã sẵn sàng sử dụng Google Gemini API trong ứng dụng EduLearn!

Nếu gặp vấn đề, hãy kiểm tra:
1. ✅ API key đã được thêm vào `.env`
2. ✅ Đã cài đặt `google-generativeai`
3. ✅ File `.env` ở đúng thư mục gốc
4. ✅ Không có lỗi trong terminal khi chạy app

**Chúc bạn sử dụng thành công! 🚀**


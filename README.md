# DrugVerify – Pharmaceutical Traceability System 💊

**DrugVerify** is a high-integrity web ecosystem engineered to eliminate pharmaceutical counterfeiting. By bridging the gap between manufacturers and the end consumer, the platform provides a "Single Source of Truth" for medication authenticity.

## 🚀 Technical Highlights
- **Hybrid QR Processing:** Real-time camera scanning (JS) with a fail-safe Python backend pipeline.
- **Computer Vision:** Processes raw byte streams via **OpenCV** and **NumPy** for server-side decoding.
- **Role-Based Access (RBAC):** Secure manufacturer dashboards for product lifecycle management (CRUD).

## 🛠️ Tech Stack
- **Backend:** Python, Django
- **Image Processing:** OpenCV, NumPy, Pillow
- **Frontend:** HTML5, Bootstrap 5, html5-qrcode.js
- **Database:** PostgreSQL / SQLite



## 📥 Installation & Setup
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/yourusername/drugverify.git](https://github.com/yourusername/drugverify.git)
   cd drugverify

```

2. **Install dependencies:**
```bash
pip install -r requirements.txt

```


3. **Set up Database:**
```bash
python manage.py migrate

```


4. **Run Server:**
```bash
python manage.py runserver

```



## 🛡️ Security Features

* **Audit Logging:** Immutable logs for every verification attempt.
* **CSRF & SQLi Protection:** Leverages Django’s security middleware.
* **Secure File Handling:** Direct memory-buffer processing to avoid disk I/O vulnerabilities.


## Author
Abdulakeem Abdulazeez

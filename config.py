class Config:
    SECRET_KEY = 'your-secret-key'  # Đổi thành chuỗi bí mật
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'  # Cơ sở dữ liệu SQLite
    SQLALCHEMY_TRACK_MODIFICATIONS = False

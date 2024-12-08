from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config import Config
from models import db, User, Event
from routes.auth import auth
from routes.events import events
from datetime import datetime
from flask import send_from_directory
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Khởi tạo các thành phần
db.init_app(app)
jwt = JWTManager(app)

# Đăng ký các blueprint
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(events, url_prefix='/api')

# Hàm khởi tạo dữ liệu demo
# def seed_data():
#     if not User.query.first():  # Chỉ thêm nếu chưa có user nào
#         # Tạo user thử nghiệm
#         test_user = User(username="testuser", email="testuser@example.com", password="hashed_password")
#         db.session.add(test_user)

#         # Tạo sự kiện thử nghiệm
#         test_event = Event(
#             title="Team Meeting",
#             description="Discuss the project roadmap",
#             start_time=datetime(2024, 12, 5, 10, 0),
#             end_time=datetime(2024, 12, 5, 11, 0),
#             user_id=1  # ID của test_user
#         )
#         db.session.add(test_event)

#         db.session.commit()
#         print("Demo data has been added!")

CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    if path != "" and os.path.exists(f"frontend/build/{path}"):
        return send_from_directory('frontend/build', path)
    else:
        return send_from_directory('frontend/build', 'index.html')

@app.route('/')
def home():
    return {"message": "Welcome to Work4Fun!"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # seed_data()
    app.run(debug=True)

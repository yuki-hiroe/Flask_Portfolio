from app import db, Admin, app
from werkzeug.security import generate_password_hash

def create_admin():
    with app.app_context():
        # 新しい管理者作成
        admin = Admin(
            username='admin',
            password_hash=generate_password_hash('admin123')
        )
        db.session.add(admin)
        db.session.commit()
        print("New admin created: admin/admin123")


if __name__ == '__main__':
    create_admin()
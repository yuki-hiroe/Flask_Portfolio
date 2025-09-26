from app import db, Admin, app
from werkzeug.security import generate_password_hash


def reset_database():
    with app.app_context():
        # テーブル削除
        db.drop_all()
        print("All tables dropped")

        # テーブル再作成
        db.create_all()
        print("Tables recreated")

        # 管理者作成
        admin = Admin(username='admin')
        password = admin.set_password('admin123')
        hashed_password = generate_password_hash(password)
        db.session.add(hashed_password)
        db.session.commit()
        print("Admin created successfully: admin/admin123")


if __name__ == '__main__':
    reset_database()
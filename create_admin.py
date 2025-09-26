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
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Admin created successfully: admin/admin123")


if __name__ == '__main__':
    reset_database()
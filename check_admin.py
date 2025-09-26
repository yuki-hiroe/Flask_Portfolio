from app import db, Admin, app
from werkzeug.security import generate_password_hash

def check_admins():
    with app.app_context():
        admins = Admin.query.all()
        print(f"Total admin accounts: {len(admins)}")
        for admin in admins:
            print(f"Username: {admin.username}, ID: {admin.id}")
            print(f"Has password: {bool(admin.password_hash)}")

        if not admins:
            print("No admin accounts found!")
        else:
            # 新しい管理者作成
            admin = Admin(
                username='admin',
                password_hash=generate_password_hash('admin123')
            )
            db.session.add(admin)
            db.session.commit()
            print("New admin created: admin/admin123")


if __name__ == '__main__':
    check_admins()

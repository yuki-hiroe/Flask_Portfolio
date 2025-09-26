from app import db, Admin, app

def check_admins():
    with app.app_context():
        admins = Admin.query.all()
        print(f"Total admin accounts: {len(admins)}")
        for admin in admins:
            print(f"Username: {admin.username}, ID: {admin.id}")
            print(f"Has password: {bool(admin.password_hash)}")

        if not admins:
            print("No admin accounts found!")


if __name__ == '__main__':
    check_admins()

from app import init_db, db, Admin

if __name__ == '__main__':
    init_db()

    # 管理者アカウント確認・作成
    admin = Admin.query.filter_by(username='admin').first()
    if not admin:
        admin = Admin(username='admin')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Default admin account created: admin/admin123")
    else:
        print("Admin account already exists")

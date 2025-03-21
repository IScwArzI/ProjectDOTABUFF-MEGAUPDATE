from app import app, db, AdminUser


with app.app_context():

    db.create_all()


    admin = AdminUser(username='admin', password='admin123')
    db.session.add(admin)
    db.session.commit()

    print("Администратор создан: логин 'admin', пароль 'admin123'")
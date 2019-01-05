from app import routes
from app.models import app, db, User
from werkzeug.security import generate_password_hash

 
if __name__ == '__main__':
    print(db)
    # db.drop_all()
    # db.create_all()
    # test_user = User(login="admin", password=generate_password_hash("admin123"))
    # db.session.add(test_user)
    # db.session.commit()
    # print('创建表')
    app.run(debug=True, host='0.0.0.0', port=8001)
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import create_app
from exts import db

from apps.system import models

User_Model = models.User_Model
User_Role = models.USER_Role
UserPersmission = models.UserPersmission

app = create_app()

manager = Manager(app)
Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
@manager.option('-e','--email',dest='email')
def create_cms_user(username, password, email):
    user = User_Model(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("system用户添加成功")

if __name__ == '__main__':
    manager.run()
from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash

class GenderType(object):
    MAN = 1
    WOMAN = 2
    SECRET = 3
    UNKNOW = 4


class UserPersmission(object):
    #255 的二进制方式来表示 1111 1111
    ALL_PERMISSION = 0b11111111
    # 1. 学生
    STUDENT =        0b00000001
    # 2. 老师
    TEACHER =         0b00000010

    #3. 管理员 管理后台  admin
    ADMINER =        0b01000000

    DEVELOP =        0b1000000

    PERMISSION_MAP = {
        STUDENT: (u'学生权限', u'上传测试数据'),
        TEACHER: (u'老师权限', u'管理学生'),
        ADMINER: (u'管理员权限', u'管理系统'),
        DEVELOP: (u'开发者权限', u'开发新功能'),
    }

system_role_user = db.Table(
    'system_role_user',
    db.Column('system_role_id', db.Integer, db.ForeignKey('system_role.id'), primary_key=True),
    db.Column('system_user_id', db.Integer, db.ForeignKey('system_user.id'), primary_key=True)
)


class USER_Role(db.Model):
    __tablename__ = 'system_role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    desc = db.Column(db.String(200),nullable=True)
    create_time = db.Column(db.DateTime, default=datetime.now)
    permissions = db.Column(db.Integer, default=UserPersmission.STUDENT)

    users = db.relationship('User_Model',secondary=system_role_user, backref='roles')

    @property
    def permission_dicts(self):

        all_permissions = self.permissions
        permission_dict_list = []

        # admin
        if all_permissions == UserPersmission.ADMINER:
            permission_dict_list = [{UserPersmission.ADMINER:UserPersmission.PERMISSION_MAP[UserPersmission.ADMINER]}]
            # print(permission_dict_list)
        else:
            for permission, permission_info in UserPersmission.PERMISSION_MAP.items():
                if permission & all_permissions == permission:
                    permission_dict_list.append({permission: permission_info})

        return permission_dict_list


class User_Model(db.Model):
    __tablename__ = 'system_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column(db.String(256), nullable=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    join_time = db.Column(db.DateTime, default=datetime.now)

    # 新增
    is_active = db.Column(db.Boolean, default=True)
    last_login_time = db.Column(db.DateTime, nullable=True)

    realname = db.Column(db.String(20))
    gender = db.Column(db.Integer, default=GenderType.UNKNOW)
    contact = db.Column(db.String(15), nullable=True)

    avatar = db.Column(db.String(100), nullable=True)
    signature = db.Column(db.String(100), nullable=True)



    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)


    def check_password(self, raw_password):
        result = check_password_hash(self.password, raw_password)
        return result

    @property
    def permissions(self):
        if not self.roles:
            return 0

        all_permissions = 0
        for role in self.roles:
            permissions = role.permissions
            all_permissions |= permissions


        return all_permissions

    def has_permission(self, permission):
        all_permissions = self.permissions
        result = all_permissions&permission == permission
        return result

    @property
    def is_developer(self):
        return self.has_permission(UserPersmission.ALL_PERMISSION)


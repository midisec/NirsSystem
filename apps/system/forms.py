from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp
from ..forms import BaseForm


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='非邮箱格式'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()
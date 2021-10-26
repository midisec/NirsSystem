from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Length, Email, EqualTo, Regexp
from ..forms import BaseForm

from ..models import SampleModel
from wtforms import ValidationError
from flask import g


class LoginForm(BaseForm):
    email = StringField(validators=[Email(message='非邮箱格式'), InputRequired(message='请输入邮箱')])
    password = StringField(validators=[Length(6, 20, message='请输入正确格式的密码')])
    remember = IntegerField()


class SampleForm(BaseForm):
    sample_name = StringField(validators=[Length(2,20, message='请输入正确长度的样本名称'), InputRequired(message='请输入样本名称')])
    sample_place = StringField(validators=[Length(2,20, message='请输入正确长度的地点名称'), InputRequired(message='请输入地点名称')])
    collector = StringField(validators=[Length(2,20, message='请输入正确采集人员名称'), InputRequired(message='请输入采集人员名称')])
    sample_time = StringField(validators=[Length(2,20, message='请输入正确日期'), InputRequired(message='请输入样本日期')])


    # def validate_sample_name(self, field):
    #     sample_name = field.data
    #     print("validata:")
    #     print(sample_name)
    #     if (SampleModel.query.filter_by(author_id=g.cms_user.id,sample_name=sample_name).first()):
    #         raise ValidationError('样本名称已经存在了！')
from flask import Blueprint, views, render_template, request, redirect, url_for, session
from .forms import LoginForm
from .models import User_Model
from exts import db, csrf

import config
from datetime import datetime

import pandas as pd
from algorithm.visualization.pyechart2img import *

bp = Blueprint("system", __name__,url_prefix='/system')


@bp.route('/index/')
# @login_required
def index():
    return render_template('system/index.html')


@bp.route('/sample/total')
def sample_total():
    return render_template('system/sample_total.html')


@bp.route('/sample/handle')
def sample_handle():
    return render_template('system/sample_handle.html')


@bp.route('/sample/result')
def sample_result():
    return render_template('system/sample_result.html')


@bp.route('/visualization/')
def visualization():
    return render_template('system/visualization.html')


# 可视化的api
@bp.route("/api/v1/visualization", methods=['POST'])
def api_visualization():
    data = request.form

    file = request.files['file']
    first = data.get('first')
    end = data.get('end')

    data1 = pd.read_csv(file)
    c = line_base(int(first), int(end) + 1, data1)
    return c.dump_options_with_quotes()


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('system/login.html', message=message)

    def post(self):
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data

            user = User_Model.query.filter_by(email=email).first()
            if user and user.check_password(password):
                session[config.SYSTEM_USER_ID] = user.id
                user.last_login_time = datetime.now()

                # 日志，先没加了
                # log_signal.send(username=user.username, email=user.email, method="用户登录")

                db.session.commit()
                if remember:
                    # 过期时间为31天
                    session.permanent = True
                return redirect(url_for('system.index'))
            else:
                return self.get(message='邮箱或密码错误')

        else:
            print(form.errors)
            message = form.get_error()
            return self.get(message=message)


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))

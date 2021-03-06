from flask import Blueprint, views, render_template, request, redirect, url_for, session, jsonify, g, send_file, make_response
from .forms import LoginForm, SampleForm
from .models import User_Model
from ..models import SampleModel
from exts import db, csrf
from utils import restful
from .decorators import login_required, permission_required

import config
from datetime import datetime

from algorithm.visualization.pyechart2img import *
from algorithm.nirspypredictor import NirspyPredictor
from algorithm.nirspycheck import NirspyCheck
from algorithm.visualization.data2imgplot import *


bp = Blueprint("system", __name__,url_prefix='/system')


@bp.route('/index/')
@login_required
def index():
    return render_template('system/index.html')


@bp.route('/sample/total')
@login_required
def sample_total():
    context = {
        'sample_list' : SampleModel.query.filter_by(author_id=g.system_user.id)
    }
    return render_template('system/sample_total.html', **context)


@bp.route('/sample/handle')
@login_required
def sample_handle():
    context = {
        'sample_list' : SampleModel.query.filter_by(author_id=g.system_user.id, state=0)
    }
    return render_template('system/sample_handle.html', **context)


@bp.route('/sample/result')
@login_required
def sample_result():
    context = {
        'sample_list' : SampleModel.query.filter_by(author_id=g.system_user.id, state=1)
    }
    return render_template('system/sample_result.html', **context)


@bp.route('/visualization/')
@login_required
def visualization():
    return render_template('system/visualization.html')


# 提交样本的api
@bp.route('/api/v1/sample_create', methods=['POST'])
@login_required
def api_sample_create():

    data = request.form
    # print(data)
    form = SampleForm(request.form)
    if form.validate():
        sample_name = form.sample_name.data
        sample_place = form.sample_place.data
        collector = form.collector.data
        sample_time = form.sample_time.data

        # print(sample_name, sample_place, collector, sample_time)
        # SampleModel
        sample = SampleModel(sample_name=sample_name, sample_place=sample_place,
                             collector=collector, sample_time=sample_time, author_id=g.system_user.id)
        db.session.add(sample)
        db.session.commit()
        return restful.success()
    else:
        # print(form.get_error())
        return restful.params_error(message=form.get_error())


@bp.route('/api/v1/sample_query', methods=['POST'])
@login_required
def api_sample_query():
    sample_id = request.form['id']
    try:
        sample = SampleModel.query.filter_by(author_id=g.system_user.id, id=sample_id).first()

        data = {"sample_place": sample.sample_place, "collector": sample.collector}
        return restful.restful_result(code=200, message="查询成功", data=data)
    except:
        return restful.params_error("该样本不存在！")


# 数据处理的api
@bp.route("/api/v1/sample_handle", methods=['POST'])
@login_required
def api_sample_handle():
    # data = request.form
    sample_id = request.form['id']
    # predict result
    file = request.files['file']
    data1 = pd.read_csv(file)
    nirspy = NirspyPredictor('default')
    # save the result
    result = nirspy.predict(data1)
    pd.DataFrame(result).to_csv(config.RESULT_PATH + sample_id + ".csv", index=False, header=['result'])
    # old data draw
    plot_url_old_data = draw_pic(data1)

    # pre data draw
    # judgment preprocessing method
    check = NirspyCheck('default')
    pre_way, model_name = check.check()
    plot_url_pre_data = check.draw(data1, pre_way)

    # change sample state
    sample = SampleModel.query.filter_by(author_id=g.system_user.id, id=sample_id).first()
    sample.state = 1
    db.session.commit()

    return jsonify(
        {'code': '200', 'data': {'old': plot_url_old_data, 'pre': plot_url_pre_data}})


@bp.route('/api/v1/sample_download/<sample_id>', methods=['GET'])
@login_required
def api_sample_download(sample_id):

    if SampleModel.query.filter_by(author_id=g.system_user.id, id=sample_id, state=1).first():
        try:
            filename = sample_id + ".csv"
            response = make_response(
                # 测试结果路径
                send_file(filename_or_fp=config.RESULT_PATH + filename, as_attachment=True)
            )
            response.headers["Content-Disposition"] = "attachment; filename={};".format(filename)
            return response
        except:
            return restful.params_error("下载出错")
    else:
        return restful.unauth_error("没有该样本结果")


# 可视化的api
@bp.route("/api/v1/visualization", methods=['POST'])
@login_required
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

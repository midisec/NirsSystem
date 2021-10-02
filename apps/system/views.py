from flask import Blueprint, views, render_template


bp = Blueprint("system", __name__,url_prefix='/system')


class LoginView(views.MethodView):
    def get(self, message=None):
        return render_template('system/login.html', message=message)

    def post(self):
        pass


bp.add_url_rule('/login/', view_func=LoginView.as_view('login'))

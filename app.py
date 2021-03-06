from flask import Flask
import config
from apps.system import bp as system_bp
from apps.common import bp as common_bp
from apps.front import bp as front_bp
from exts import db, csrf


app = Flask(__name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(system_bp)
    app.register_blueprint(common_bp)
    app.register_blueprint(front_bp)

    db.init_app(app)
    csrf.init_app(app)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host="0.0.0.0", port=8081)

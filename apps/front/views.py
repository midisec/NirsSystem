from flask import Blueprint, redirect, url_for


bp = Blueprint("front", __name__)


@bp.route('/')
def index():
    return redirect(url_for('system.login'))
import config
from flask import session, redirect, url_for, g
from functools import wraps


def login_required(func):

    @wraps(func)
    def inner(*args, **kwargs):
        if config.SYSTEM_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('system.login'))

    return inner


def permission_required(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_permission(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('system.index'))
        return inner
    return outter
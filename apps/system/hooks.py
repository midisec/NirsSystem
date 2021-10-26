from .views import bp
from flask import session, g
from .models import User_Model, UserPersmission
import config

@bp.before_request
def before_request():
    if config.SYSTEM_USER_ID in session:
        user_id = session.get(config.SYSTEM_USER_ID)
        user = User_Model.query.get(user_id)
        if user:
            g.system_user = user

@bp.context_processor
def cms_context_processor():
    return {"CMSPermission":UserPersmission}
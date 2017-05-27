from routes import *
from models.document import Document
from models.user import User
from models.auth import Auth
from models.access import Access
from flask.blueprints import Blueprint
from flask import current_app as app

import qiniu
from config import key

q = qiniu.Auth(key.qiniu_access_key, key.qiniu_secret_key)

main = Blueprint('admin', __name__)


@main.route('/document/<user_uuid>')
@admin_required
def document(user_uuid):
    cu = current_user()
    u = User.find_one(uuid=user_uuid)
    u.pi
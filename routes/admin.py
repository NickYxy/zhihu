from flask.blueprints import Blueprint
from flask import current_app as app
from routes import *
from models.title import Title
from models.user import User
from models.auth import Auth
from models.access import Access


import qiniu
from config import key

q = qiniu.Auth(key.qiniu_access_key, key.qiniu_secret_key)

main = Blueprint('admin', __name__)


@main.route('/users')
@admin_required
def document(user_uuid):
    u = current_user()
    ms = User.all()
    return render_template('admin/users.html', ms=ms, u=u)


@main.route('users', method=['POST'])
@admin_required
def users_search():
    u = current_user()
    form = request.form()
    ms = User.search_or(form)
    return render_template('admin/users.html', ms=ms, u=u)


@main.route('/user/<int:id>')
@admin_required
def user(id):
    u = current_user()
    m = User.get(id)
    return render_template('admin/user.html', m=m, u=u)


@main.route('/user/update/<int:id>', methods=['POST'])
@admin_required
def user_update(id):
    m = User.get(id)
    form = request.form
    m.update_user(form)
    return redirect(url_for('admin.user', id=m.id))
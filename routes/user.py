from routes import *
from models.user import User
from decimal import Decimal
from flask import current_app as app
from flask.blueprints import *


main = Blueprint('user', __name__)

Model = User


@main.route('/login')
def index():
    return render_template('user/login.html')


@main.route('/login', methods=['POST'])
def login():
    form = request.form
    username = form.get('username', '')
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        return redirect(url_for('user.index'))
    u = User.find_one(username=username)
    if u is not None and u.validate_login(form):
        session['uid'] = u.id
        return redirect(url_for('index.index'))
    else:
        return redirect(url_for('user.index'))


@main.route('/register')
def register_page():
    return render_template('user/register.html')


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        return redirect(url_for('user.register'))
    status, msgs = User.valid(form)
    if status is True:
        u = User.new(form)
        u.send_email_verify(u.email)
        session['uid'] = u.id
        return redirect(url_for('index.index'))  # TODO 邮件重置密码
    else:
        return redirect(url_for('user.register'))  # TODO 改为flash提示


@main.route('/reset_password/<tb64>', methods=['POST'])
def reset_password(tb64):
    password = request.form.get('password', '')
    if User.forget_password_verify(tb64):
        u = User.get_user_by_tb64(tb64)
        u.reset_password(password)
        session['uid'] = u.id
        return redirect(url_for('index.index'))


@main.route('/profile')
@login_required
def profile():
    cu = current_user()
    return render_template('user/profile.html', u=cu)


@main.route('/profile', methods=['POST'])
@login_required
def profile_update():
    cu = current_user()
    form = request.form
    cu.safe_update_user(form)
    return redirect(url_for('user.profile'))


@main.route('/update_email', methods=['POST'])
@login_required
def update_email():
    u = current_user()
    form = request.form
    new_email = form.get('email', '')
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        return json.dumps({'status': 'error', 'msg': 'captcha error'})
    if User.has(email=new_email) and User.find_one(email=new_email).uuid != u.uuid:
        return json.dumps({'status': 'error', 'msg': 'email exist'})
    if u.validate_login(form):
        u.send_email_verify(new_email)
        return redirect(url_for('user.profile'))
    else:
        return json.dumps({'status': 'error', 'msg': 'password error'})


@main.route('/uploadavatar', methods=['POST'])
@login_required
def avatar():
    u = current_user()
    avatar = request.files['avatar']
    u.update_avatar(avatar)
    return redirect(url_for('.profile'))



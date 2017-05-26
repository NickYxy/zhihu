from routes import *
from models.user import User
from decimal import Decimal
from flask import current_app as app
from flask.blueprints import *
from flask import flash


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
        return redirect(url_for('user.dashboard'))
    else:
        flash('用户名密码错误', 'warning')
        return redirect(url_for('user.index'))


@main.route('/register')
def register_page():
    return render_template('user/register.html')


@main.route('/register', methods=['POST'])
def register():
    form = request.form
    captcha = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        flash('验证码错误', 'warning')
        return redirect(url_for('user.register'))
    status, msgs = User.valid(form)
    if status is True:
        u = User.new(form)
        u.send_email_verify(u.email)
        session['uid'] = u.id
        flash('验证邮件已发送，请查收', 'info')
        return redirect(url_for('user.dashboard'))  # TODO 邮件重置密码
    else:
        for msg in msgs:
            flash(msg, 'warning')
            return redirect(url_for('user.register'))  # TODO 改为flash提示


@main.route('/password/forget')
def forget_password():
    if current_user() is not None:
        return redirect(url_for('user.dashboard'))
    return render_template(url_for('user/forget_password.html'))


@main.route('/reset_password/', methods=['POST'])
def forget_password_send():
    form = request.form
    captcha  = form.get('captcha', '').lower()
    if captcha != session.get('captcha', 'no captcha!'):
        flash('验证码错误', 'warning')
        return redirect(url_for('user.forget_password'))
    r = User.forget_password(form)


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



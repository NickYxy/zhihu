from flask import request
from flask.blueprints import Blueprint
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import url_for
from flask import Response
from flask import session

from models.user import User
from functools import wraps
import json


def current_user():
    uid = int(session.get('uid', -1))
    u = User.get(uid)


def login_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is not None:
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function


def admin_required(f):
    @wraps(f)
    def function(*args, **kwargs):
        if current_user() is None:
            return redirect(url_for('user.index'))
        if not current_user().is_admin():
            return redirect(url_for('user.index'))
        return f(*args, **kwargs)

    return function



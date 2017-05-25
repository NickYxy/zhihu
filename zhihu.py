import logging
from flask import Flask
from flask_script import Manager


app = Flask(__name__)

manager = Manager(app)


@app.route('/login')
def user_login():
    return
# def register_routes(app):
#     from routes.user import main as routes_user
#     app.register_blueprint(routes_user, url_prefix='/user')


def configure_app():
    from config import key
    app.secret_key = key.secret_key
    from config.config import config_dict
    app.config.update(config_dict)
    # 设置 log, 否则输出会被 gunicorn 吃掉
    if not app.debug:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)


def configured_app():
    configure_app()
    return app


@manager.command
def server():
    #config = {'debug': True, 'host': '0.0.0.0', 'port': 8001}
    config = dict(
        debug=True,
        host='0.0.0.0',
        port=8001,
    )
    app.run(**config)


if __name__ == '__main__':
    configure_app()
    manager.run()

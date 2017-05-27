from . import *
from models.title import Title

main = Blueprint('index', __name__)


@main.route('/')
def index():
    if current_user() is not None:
        return redirect(url_for('user.dashboard'))
    return redirect(url_for('demo.index'))
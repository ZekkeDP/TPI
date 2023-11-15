from flask import (
    Blueprint, render_template
)

bp = Blueprint('proyecto', __name__, url_prefix='/')

@bp.route('/', methods=['GET'])

def index():
    return render_template('proyecto/index.html')

@bp.route('/mail', methods=['POST'])
def mail():
    return render_template('proyecto/sent_mail.html')
from flask import render_template, Blueprint, send_from_directory
from flask_user import current_user, login_required

from app.models import Account, CharacterInfo, ActivityLog
from app.schemas import AccountSchema, CharacterInfoSchema

main_blueprint = Blueprint('main', __name__)

account_schema = AccountSchema()
char_info_schema = CharacterInfoSchema()


@main_blueprint.route('/', methods=['GET'])
def index():
    """Home/Index Page"""
    if current_user.is_authenticated:
        account_data = Account.query.filter(Account.id == current_user.id).first()

        return render_template(
            'main/index.html.j2',
            account_data=account_data
        )
    else:
        return render_template('main/index.html.j2')


@main_blueprint.route('/about')
@login_required
def about():
    """About Page"""
    mods = Account.query.filter(Account.gm_level > 0).all()
    online = 0
    chars = CharacterInfo.query.all()
    for char in chars:
        last_log = ActivityLog.query.with_entities(
            ActivityLog.activity
        ).filter(
            ActivityLog.character_id == char.id
        ).order_by(ActivityLog.id.desc()).first()
        print(last_log)
        if last_log:
            if last_log[0] == 0:
                online += 1

    return render_template('main/about.html.j2', mods=mods, online=online)


@main_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static/logo/',
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

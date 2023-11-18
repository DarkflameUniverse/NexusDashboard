from flask import render_template, Blueprint, send_from_directory
from flask_user import current_user, login_required

from app.models import Account, CharacterInfo, ActivityLog

import datetime
import time

main_blueprint = Blueprint('main', __name__)


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
    mods = Account.query.filter(Account.gm_level > 1).order_by(Account.gm_level.desc()).all()
    online = 0
    users = []
    zones = {}
    twodaysago = time.mktime((datetime.datetime.now() - datetime.timedelta(days=2)).timetuple())
    chars = CharacterInfo.query.filter(CharacterInfo.last_login >= twodaysago).all()

    for char in chars:
        last_log = ActivityLog.query.with_entities(
            ActivityLog.activity, ActivityLog.map_id
        ).filter(
            ActivityLog.character_id == char.id
        ).order_by(ActivityLog.id.desc()).first()

        if last_log:
            if last_log[0] == 0:
                online += 1
                if current_user.gm_level >= 8: users.append([char.name, last_log[1]])
                if str(last_log[1]) not in zones:
                    zones[str(last_log[1])] = 1
                else:
                    zones[str(last_log[1])] += 1

    return render_template('main/about.html.j2', mods=mods, online=online, users=users, zones=zones)


@main_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static/logo/',
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

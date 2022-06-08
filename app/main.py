from flask import render_template, Blueprint, send_from_directory, request, session, redirect, current_app
from flask_user import current_user, login_required

from app.models import Account, CharacterInfo, ActivityLog
from app.schemas import AccountSchema, CharacterInfoSchema
from app import scheduler
from zenora import APIClient

main_blueprint = Blueprint('main', __name__)

account_schema = AccountSchema()
char_info_schema = CharacterInfoSchema()

with scheduler.app.app_context():
    client = APIClient(current_app.config['TOKEN'], client_secret=current_app.config['CLIENT_SECRET'])


@main_blueprint.route('/')
def start():

    if current_app.config['DISCORD_INTEGRATION']:
        return redirect(current_app.config['OAUTH_URL'])
    if not current_app.config['DISCORD_INTEGRATION']:
        return redirect('/home')


@main_blueprint.route('/home', methods=['GET'])
def index():
    """Home/Index Page"""
    if current_app.config['DISCORD_INTEGRATION']:
        if 'token' in session:
            if current_user.is_authenticated:
                account_data = Account.query.filter(Account.id == current_user.id).first()

                return render_template(
                    'main/index.html.j2',
                    account_data=account_data, oauth_uri=current_app.config['OAUTH_URL']
                )
            else:
                return render_template('main/index.html.j2', oauth_uri=current_app.config['OAUTH_URL'])
        else:
            return redirect('/')
    if not current_app.config['DISCORD_INTEGRATION']:
        if current_user.is_authenticated:
            account_data = Account.query.filter(Account.id == current_user.id).first()

            return render_template(
                'main/index.html.j2',
                account_data=account_data
            )
        else:
            return render_template('main/index.html.j2')


@main_blueprint.route('/oauth/callback')
def callback():
    code = request.args['code']
    access_token = client.oauth.get_access_token(code, current_app.config['REDIRECT_URI']).access_token
    session['token'] = access_token
    return redirect('/home')


@main_blueprint.route('/about')
@login_required
def about():
    """About Page"""
    mods = Account.query.filter(Account.gm_level > 0).order_by(Account.gm_level.desc()).all()
    online = 0
    chars = CharacterInfo.query.all()
    for char in chars:
        last_log = ActivityLog.query.with_entities(
            ActivityLog.activity
        ).filter(
            ActivityLog.character_id == char.id
        ).order_by(ActivityLog.id.desc()).first()

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

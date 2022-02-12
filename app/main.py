from flask import render_template, Blueprint, redirect,  request, send_from_directory, make_response, send_file, current_app
from flask_user import login_required, current_user
import json, glob, os
from wand import image

from app.models import Account, AccountInvitation, CharacterInfo
from app.schemas import AccountSchema, CharacterInfoSchema
from app.luclient import query_cdclient
from app import gm_level

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
def about():
    """About Page"""
    return render_template('main/about.html.j2')


@main_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static/logo/',
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@main_blueprint.route('/logs')
@gm_level(9)
def logs():
    with open('nexus_dashboard.log', 'r') as file:
        logs = '</br>'.join(file.read().split('\n')[-100:])
    return render_template('main/logs.html.j2', logs=logs)
    return '</br>'.join(all_read_text.splitlines()[-total_lines_wanted:])

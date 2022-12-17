from flask import render_template, Blueprint, request, url_for
from flask_user import login_required
from app.models import CommandLog, ActivityLog, db, Account, CharacterInfo, AuditLog
from datatables import ColumnDT, DataTables
import time
from app import gm_level

log_blueprint = Blueprint('log', __name__)


@log_blueprint.route('/activities', methods=['GET'])
@login_required
@gm_level(8)
def activity():
    return render_template('logs/activity.html.j2')


@log_blueprint.route('/commands', methods=['GET'])
@login_required
@gm_level(8)
def command():
    return render_template('logs/command.html.j2')


@log_blueprint.route('/system')
@gm_level(8)
def system():
    with open('logs/nexus_dashboard.log', 'r') as file:
        logs = '</br>'.join(file.read().split('\n')[-100:])
    return render_template('logs/system.html.j2', logs=logs)


@log_blueprint.route('/audits')
@gm_level(8)
def audit():
    return render_template('logs/audit.html.j2')


@log_blueprint.route('/get_activities', methods=['GET'])
@login_required
@gm_level(8)
def get_activities():
    columns = [
        ColumnDT(ActivityLog.id),               # 0
        ColumnDT(ActivityLog.character_id),     # 1
        ColumnDT(ActivityLog.activity),         # 2
        ColumnDT(ActivityLog.time),             # 3
        ColumnDT(ActivityLog.map_id),           # 4
    ]

    query = db.session.query().select_from(ActivityLog)

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    data = rowTable.output_result()
    for activity in data["data"]:
        char_id = activity["1"]
        activity["1"] = f"""
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('characters.view', id=char_id)}'>
                View Character: {CharacterInfo.query.filter(CharacterInfo.id==char_id).first().name}
            </a>
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('accounts.view', id=CharacterInfo.query.filter(CharacterInfo.id==char_id).first().account_id)}'>
                View Account: {Account.query.filter(Account.id==CharacterInfo.query.filter(CharacterInfo.id==char_id).first().account_id).first().username}
            </a>
        """

        if activity["2"] == 0:
            activity["2"] = "Entered World"
        elif activity["2"] == 1:
            activity["2"] = "Left World"

        activity["3"] = time.ctime(activity["3"])

    return data


@log_blueprint.route('/get_commands', methods=['GET'])
@login_required
@gm_level(8)
def get_commands():
    columns = [
        ColumnDT(CommandLog.id),            # 0
        ColumnDT(CommandLog.character_id),  # 1
        ColumnDT(CommandLog.command),       # 2
    ]

    query = db.session.query().select_from(CommandLog)

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    data = rowTable.output_result()
    for command in data["data"]:
        char_id = command["1"]
        command["1"] = f"""
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('characters.view', id=char_id)}'>
                View Character: {CharacterInfo.query.filter(CharacterInfo.id==command['1']).first().name}
            </a>
        """
        command["1"] += f"""
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('accounts.view', id=CharacterInfo.query.filter(CharacterInfo.id==char_id).first().account_id)}'>
                View Account: {Account.query.filter(Account.id==CharacterInfo.query.filter(CharacterInfo.id==char_id).first().account_id).first().username}
            </a>
        """

    return data


@log_blueprint.route('/get_audits', methods=['GET'])
@login_required
@gm_level(8)
def get_audits():
    columns = [
        ColumnDT(AuditLog.id),            # 0
        ColumnDT(AuditLog.account_id),    # 1
        ColumnDT(AuditLog.action),        # 2
        ColumnDT(AuditLog.date),          # 2
    ]

    query = db.session.query().select_from(AuditLog)

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    data = rowTable.output_result()
    for audit in data["data"]:
        char_id = audit["1"]
        audit["1"] = f"""
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('accounts.view', id=char_id)}'>
                {Account.query.filter(Account.id==audit['1']).first().username}
            </a>
        """

    return data

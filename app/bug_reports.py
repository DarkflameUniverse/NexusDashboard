from flask import render_template, Blueprint, redirect, url_for, request, flash, redirect
from flask_user import login_required, current_user
from app.models import db, BugReport, CharacterInfo
from datatables import ColumnDT, DataTables
from app.forms import ResolveBugReportForm
from app import gm_level
from app.luclient import translate_from_locale

bug_report_blueprint = Blueprint('bug_reports', __name__)


@bug_report_blueprint.route('/<status>', methods=['GET'])
@login_required
def index(status):
    return render_template('bug_reports/index.html.j2', status=status)


@bug_report_blueprint.route('/view/<id>', methods=['GET'])
@login_required
def view(id):
    report = BugReport.query.filter(BugReport.id == id).first()
    if current_user.gm_level < 3:
        chars = CharacterInfo.query.with_entities(CharacterInfo.id).filter(CharacterInfo.account_id == current_user.id).all()
        char_ids = []
        for char in chars:
            char_ids.append(char[0])
        if report.reporter_id not in char_ids:
            return redirect(url_for('bug_reports.index', status=all))
    if report.resoleved_by:
        rb = report.resoleved_by.username
    else:
        rb = ""
    return render_template('bug_reports/view.html.j2', report=report, resolved_by=rb)


@bug_report_blueprint.route('/resolve/<id>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def resolve(id):
    report = BugReport.query.filter(BugReport.id == id).first()
    if report.resolved_time:
        flash("Bug report already resolved!", "danger")
        return redirect(request.referrer if request.referrer else url_for("main.index"))

    form = ResolveBugReportForm()
    if form.validate_on_submit():
        report.resolution = form.resolution.data
        report.resoleved_by_id = current_user.id
        report.resolved_time = db.func.now()
        report.save()
        return redirect(url_for("bug_reports.index", status="unresolved"))

    return render_template('bug_reports/resolve.html.j2', form=form, report=report)


@bug_report_blueprint.route('/get/<status>', methods=['GET'])
@login_required
@gm_level(3)
def get(status):
    columns = [
        ColumnDT(BugReport.id),                 # 0
        ColumnDT(BugReport.reporter_id),        # 1
        ColumnDT(BugReport.body),               # 2
        ColumnDT(BugReport.client_version),     # 3
        ColumnDT(BugReport.other_player_id),    # 4
        ColumnDT(BugReport.selection),          # 5
        ColumnDT(BugReport.submitted),          # 6
        ColumnDT(BugReport.resolved_time),      # 7
    ]

    query = None
    if current_user.gm_level > 0:
        if status == "all":
            query = db.session.query().select_from(BugReport)
        elif status == "resolved":
            query = db.session.query().select_from(BugReport).filter(BugReport.resolved_time != None)
        elif status == "unresolved":
            query = db.session.query().select_from(BugReport).filter(BugReport.resolved_time == None)
        else:
            raise Exception("Not a valid filter")
    else:
        chars = CharacterInfo.query.with_entities(CharacterInfo.id).filter(CharacterInfo.account_id == current_user.id).all()
        char_ids = []
        for char in chars:
            char_ids.append(char[0])
        if status == "all":
            query = db.session.query().select_from(BugReport).filter(BugReport.reporter_id.in_(char_ids))
        elif status == "resolved":
            query = db.session.query().select_from(BugReport).filter(BugReport.reporter_id.in_(char_ids)).filter(BugReport.resolved_time != None)
        elif status == "unresolved":
            query = db.session.query().select_from(BugReport).filter(BugReport.reporter_id.in_(char_ids)).filter(BugReport.resolved_time == None)
        else:
            raise Exception("Not a valid filter")

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    data = rowTable.output_result()
    for report in data["data"]:
        id = report["0"]
        report["0"] = f"""
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('bug_reports.view', id=id)}'>
                View
            </a>
        """

        if report["7"] is not None:
            report["0"] += f"""
                <a role="button" class="btn btn-danger btn btn-block"
                    href='{url_for('bug_reports.resolve', id=id)}'>
                    Resolve
                </a>
            """
        else:
            report["7"] = '''<h1 class="far fa-times-circle text-danger"></h1>'''

        if not report["1"]:
            report["1"] = "None"
        else:
            character = CharacterInfo.query.filter(CharacterInfo.id == int(report["1"])).first()
            if character:
                report["1"] = f"""
                    <a role="button" class="btn btn-primary btn btn-block"
                        href='{url_for('characters.view', id=report['1'])}'>
                        {character.name}
                    </a>
                """
            else:
                report["1"] = "Player Deleted"

        if report["4"] == "0":
            report["4"] = "None"
        else:
            character = CharacterInfo.query.filter(CharacterInfo.id == int(report["4"]) & 0xFFFFFFFF).first()
            if character:
                if current_user.gm_level > 3:
                    report["4"] = f"""
                        <a role="button" class="btn btn-primary btn btn-block"
                            href='{url_for('characters.view', id=(int(report["4"]) & 0xFFFFFFFF))}'>
                            {character.name}
                        </a>
                    """
                else:
                    report["4"] = character.name
            else:
                report["4"] = "Player Deleted"

        report["5"] = translate_from_locale(report["5"][2:-1])

    return data

from flask import render_template, Blueprint, redirect, url_for, request, flash
from flask_user import login_required, current_user
from app.models import db, BugReport, CharacterInfo
from datatables import ColumnDT, DataTables
from app.forms import ResolveBugReportForm
from app import gm_level
from app.luclient import translate_from_locale

bug_report_blueprint = Blueprint('bug_reports', __name__)


@bug_report_blueprint.route('/<status>', methods=['GET'])
@login_required
@gm_level(3)
def index(status):
    return render_template('bug_reports/index.html.j2', status=status)


@bug_report_blueprint.route('/view/<id>', methods=['GET'])
@login_required
@gm_level(3)
def view(id):
    report = BugReport.query.filter(BugReport.id == id).first()
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
        ColumnDT(BugReport.body),               # 1
        ColumnDT(BugReport.client_version),     # 2
        ColumnDT(BugReport.other_player_id),    # 3
        ColumnDT(BugReport.selection),          # 4
        ColumnDT(BugReport.submitted),          # 5
        ColumnDT(BugReport.resolved_time),      # 6
    ]

    query = None
    if status == "all":
        query = db.session.query().select_from(BugReport)
    elif status == "resolved":
        query = db.session.query().select_from(BugReport).filter(BugReport.resolved_time not None)
    elif status == "unresolved":
        query = db.session.query().select_from(BugReport).filter(BugReport.resolved_time is None)
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

        if not report["6"]:
            report["0"] += f"""
            <a role="button" class="btn btn-danger btn btn-block"
                href='{url_for('bug_reports.resolve', id=id)}'>
                Resolve
            </a>
        """

        if report["3"] == "0":
            report["3"] = "None"
        else:
            character = CharacterInfo.query.filter(CharacterInfo.id == int(report["3"]) & 0xFFFFFFFF).first()
            if character:
                report["3"] = f"""
                    <a role="button" class="btn btn-primary btn btn-block"
                        href='{url_for('characters.view', id=(int(report["3"]) & 0xFFFFFFFF))}'>
                        {character.name}
                    </a>
                """
            else:
                report["3"] = "Player Deleted"

        report["4"] = translate_from_locale(report["4"][2:-1])

        if not report["6"]:
            report["6"] = '''<h1 class="far fa-times-circle text-danger"></h1>'''

    return data

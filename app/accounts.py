from flask import render_template, Blueprint, redirect, url_for, request, current_app, flash
from flask_user import login_required, current_user
from datatables import ColumnDT, DataTables
import datetime
from app.models import Account, db
from app.schemas import AccountSchema
from app import gm_level, log_audit
from app.forms import EditGMLevelForm

accounts_blueprint = Blueprint('accounts', __name__)

account_schema = AccountSchema()


@accounts_blueprint.route('/', methods=['GET'])
@login_required
@gm_level(3)
def index():
    return render_template('accounts/index.html.j2')


@accounts_blueprint.route('/view/<id>', methods=['GET'])
@login_required
@gm_level(3)
def view(id):
    account_data = Account.query.filter(Account.id == id).first()
    if account_data:
        return render_template('accounts/view.html.j2', account_data=account_data)
    else:
        return redirect(url_for('main.index'))


@accounts_blueprint.route('/edit_gm_level/<id>', methods=('GET', 'POST'))
@login_required
@gm_level(8)
def edit_gm_level(id):
    if current_user.id == int(id):
        flash("You cannot your own GM Level", "danger")
        return redirect(request.referrer if request.referrer else url_for("main.index"))
    account_data = Account.query.filter(Account.id == id).first()
    if account_data.gm_level >= 8 and current_user.gm_level == 8:
        flash("You cannot edit this user's GM Level", "warning")
        return redirect(request.referrer if request.referrer else url_for("main.index"))

    form = EditGMLevelForm()

    if form.validate_on_submit():
        log_audit(f"Changed ({account_data.id}){account_data.username}'s GM Level from {account_data.gm_level} to {form.gm_level.data}")
        account_data.gm_level = form.gm_level.data
        account_data.save()

        return redirect(url_for('accounts.view', id=account_data.id))

    form.gm_level.data = account_data.gm_level

    return render_template('accounts/edit_gm_level.html.j2', form=form, username=account_data.username)


@accounts_blueprint.route('/lock/<id>', methods=['GET'])
@login_required
@gm_level(3)
def lock(id):
    account = Account.query.filter(Account.id == id).first()
    account.locked = not account.locked
    account.active = not account.locked
    account.save()
    if account.locked:
        log_audit(f"Locked ({account.id}){account.username}")
        flash("Locked Account", "danger")
    else:
        log_audit(f"Unlocked ({account.id}){account.username}")
        flash("Unlocked account", "success")
    return redirect(request.referrer if request.referrer else url_for("main.index"))


@accounts_blueprint.route('/ban/<id>', methods=['GET'])
@login_required
@gm_level(3)
def ban(id):
    account = Account.query.filter(Account.id == id).first()
    account.banned = not account.banned
    account.active = not account.banned
    account.save()
    if account.banned:
        log_audit(f"Banned ({account.id}){account.username}")
        flash("Banned Account", "danger")
    else:
        log_audit(f"Unbanned ({account.id}){account.username}")
        flash("Unbanned account", "success")
    return redirect(request.referrer if request.referrer else url_for("main.index"))


@accounts_blueprint.route('/muted/<id>/<days>', methods=['GET'])
@login_required
@gm_level(3)
def mute(id, days=0):
    account = Account.query.filter(Account.id == id).first()
    if days == "0":
        account.mute_expire = 0
        log_audit(f"Unmuted ({account.id}){account.username}")
        flash("Unmuted Account", "success")
    else:
        muted_intil = datetime.datetime.now() + datetime.timedelta(days=int(days))
        account.mute_expire = muted_intil.timestamp()
        log_audit(f"Muted ({account.id}){account.username} for {days} days")
        flash(f"Muted account for {days} days", "danger")
    account.save()

    return redirect(request.referrer if request.referrer else url_for("main.index"))


@accounts_blueprint.route('/get', methods=['GET'])
@login_required
@gm_level(3)
def get():
    columns = [
        ColumnDT(Account.id),                   # 0
        ColumnDT(Account.username),             # 1
        ColumnDT(Account.email),                # 2
        ColumnDT(Account.gm_level),             # 3
        ColumnDT(Account.locked),               # 4
        ColumnDT(Account.banned),               # 5
        ColumnDT(Account.mute_expire),          # 6
        ColumnDT(Account.created_at),           # 7
        ColumnDT(Account.email_confirmed_at)    # 8
    ]

    query = db.session.query().select_from(Account)

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    data = rowTable.output_result()
    for account in data["data"]:
        account["0"] = f"""
            <a role="button" class="btn btn-primary btn btn-block"
            href='{url_for('accounts.view', id=account["0"])}'>
            View
            </a>
        """
        #        <a role="button" class="btn btn-danger btn btn-block"
        # href='{url_for('acounts.delete', id=account["0"])}'>
        # Delete
        # </a>

        if account["4"]:
            account["4"] = '''<h2 class="far fa-times-circle text-danger"></h2>'''
        else:
            account["4"] = '''<h2 class="far fa-check-square text-success"></h2>'''

        if account["5"]:
            account["5"] = '''<h2 class="far fa-times-circle text-danger"></h2>'''
        else:
            account["5"] = '''<h2 class="far fa-check-square text-success"></h2>'''

        if account["6"]:
            account["6"] = '''<h2 class="far fa-times-circle text-danger"></h2>'''
        else:
            account["6"] = '''<h2 class="far fa-check-square text-success"></h2>'''

        if current_app.config["USER_ENABLE_EMAIL"]:
            if account["8"]:
                account["8"] = '''<h2 class="far fa-check-square text-success"></h2>'''
            else:
                account["8"] = '''<h2 class="far fa-times-circle text-danger"></h2>'''
        else:
            # shift columns to fill in gap of 2
            account["2"] = account["3"]
            account["3"] = account["4"]
            account["4"] = account["5"]
            account["5"] = account["6"]
            account["6"] = account["7"]
            # remove last two columns
            del account["7"]
            del account["8"]

    return data

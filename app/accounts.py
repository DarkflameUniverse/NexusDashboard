from flask import render_template, Blueprint, redirect, url_for, request, current_app, flash
from flask_user import login_required, current_user
from datatables import ColumnDT, DataTables
import bcrypt
import datetime
import secrets
from app.models import (
    Account,
    CharacterInfo,
    ActivityLog,
    Leaderboard,
    Mail,
    Property,
    PropertyContent,
    UGC,
    AuditLog,
    BugReport,
    AccountInvitation,
    db,
    Friends,
    CommandLog,
    CharacterXML
)
from app import gm_level, log_audit
from app.forms import EditGMLevelForm, EditEmailForm
from sqlalchemy import or_, inspect, text, bindparam

accounts_blueprint = Blueprint('accounts', __name__)

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


@accounts_blueprint.route('/edit_email/<id>', methods=('GET', 'POST'))
@login_required
@gm_level(8)
def edit_email(id):
    account_data = Account.query.filter(Account.id == id).first()
    form = EditEmailForm()
    if form.validate_on_submit():
        log_audit(f"Changed ({account_data.id}){account_data.username}'s Email from {account_data.email} to {form.email.data}")
        account_data.email = form.email.data
        account_data.save()
        return redirect(url_for('accounts.view', id=account_data.id))

    form.email.data = account_data.email
    return render_template('accounts/edit_email.html.j2', form=form, username=account_data.username)


@accounts_blueprint.route('/lock/<id>', methods=['GET'])
@login_required
@gm_level(3)
def lock(id):
    account = Account.query.filter(Account.id == id).first()
    if not account.locked:
        account.locked = True
        account.active = False
        log_audit(f"Locked ({account.id}){account.username}")
        flash("Locked Account", "danger")
    else:
        account.locked = False
        account.active = True
        log_audit(f"Unlocked ({account.id}){account.username}")
        flash("Unlocked account", "success")
    account.save()
    return redirect(request.referrer if request.referrer else url_for("main.index"))


@accounts_blueprint.route('/ban/<id>', methods=['GET'])
@login_required
@gm_level(3)
def ban(id):
    account = Account.query.filter(Account.id == id).first()
    if not account.banned:
        account.banned = True
        account.active = False
        log_audit(f"Banned ({account.id}){account.username}")
        flash("Banned Account", "danger")
    else:
        account.banned = False
        account.active = True
        log_audit(f"Unbanned ({account.id}){account.username}")
        flash("Unbanned account", "success")
    account.save()
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


@accounts_blueprint.route('/delete/<id>/', methods=['GET', 'POST'])
@login_required
@gm_level(9)
def delete(id):
    account = Account.query.filter(Account.id == id).first()
    if account is None:
        flash("Account not found", "danger")
        return redirect(url_for("main.index"))
    message = f"Deleted Account ({account.id}){account.username}"
    try:
        _delete_account_data(account)
    except Exception:
        db.session.rollback()
        current_app.logger.exception(f"Failed to delete account {id}")
        flash(f"Failed to delete Account ({account.id}){account.username}", "danger")
        return redirect(url_for("accounts.view", id=id))
    flash(message, "danger")
    log_audit(message)
    return redirect(url_for("main.index"))


def _bulk_delete(query):
    # Bulk deletes bypass the ORM relationship handling, which would otherwise
    # try to NULL out non-nullable foreign keys (e.g. ugc.character_id)
    # instead of deleting the dependent rows.
    query.delete(synchronize_session=False)


def _delete_account_data(account):
    """Delete an account and every row that references it or its characters.

    The DLU schema uses ON DELETE RESTRICT for most of these foreign keys,
    so dependents have to be removed explicitly, children first, and all
    in one transaction so a failure leaves nothing half-deleted.
    """
    char_ids = [
        c.id for c in CharacterInfo.query.with_entities(CharacterInfo.id)
        .filter(CharacterInfo.account_id == account.id).all()
    ]
    clone_ids = [
        c.prop_clone_id for c in CharacterInfo.query.with_entities(CharacterInfo.prop_clone_id)
        .filter(CharacterInfo.account_id == account.id).all()
    ]
    existing_tables = set(inspect(db.engine).get_table_names())

    if char_ids:
        prop_ids = [
            p.id for p in Property.query.with_entities(Property.id).filter(
                or_(Property.owner_id.in_(char_ids), Property.clone_id.in_(clone_ids))
            ).all()
        ]
        ugc_ids = [
            u.id for u in UGC.query.with_entities(UGC.id).filter(
                or_(UGC.account_id == account.id, UGC.character_id.in_(char_ids))
            ).all()
        ]
        # property contents placed on this account's properties, or using its UGC models
        content_filter = []
        if prop_ids:
            content_filter.append(PropertyContent.property_id.in_(prop_ids))
        if ugc_ids:
            content_filter.append(PropertyContent.ugc_id.in_(ugc_ids))
        if content_filter:
            _bulk_delete(PropertyContent.query.filter(or_(*content_filter)))
        if prop_ids:
            _bulk_delete(Property.query.filter(Property.id.in_(prop_ids)))
        if "ugc_modular_build" in existing_tables:
            db.session.execute(
                text("DELETE FROM ugc_modular_build WHERE character_id IN :ids")
                .bindparams(bindparam("ids", expanding=True)),
                {"ids": char_ids}
            )
        if "ignore_list" in existing_tables:
            db.session.execute(
                text("DELETE FROM ignore_list WHERE player_id IN :ids OR ignored_player_id IN :ids")
                .bindparams(bindparam("ids", expanding=True)),
                {"ids": char_ids}
            )
        _bulk_delete(ActivityLog.query.filter(ActivityLog.character_id.in_(char_ids)))
        _bulk_delete(Leaderboard.query.filter(Leaderboard.character_id.in_(char_ids)))
        _bulk_delete(Mail.query.filter(Mail.receiver_id.in_(char_ids)))
        _bulk_delete(CommandLog.query.filter(CommandLog.character_id.in_(char_ids)))
        _bulk_delete(Friends.query.filter(
            or_(Friends.player_id.in_(char_ids), Friends.friend_id.in_(char_ids))
        ))
        _bulk_delete(CharacterXML.query.filter(CharacterXML.id.in_(char_ids)))

    # UGC can reference the account even without a (remaining) character
    _bulk_delete(UGC.query.filter(
        or_(UGC.account_id == account.id, UGC.character_id.in_(char_ids))
        if char_ids else UGC.account_id == account.id
    ))
    if char_ids:
        _bulk_delete(CharacterInfo.query.filter(CharacterInfo.id.in_(char_ids)))

    if "player_cheat_detections" in existing_tables:
        db.session.execute(
            text("DELETE FROM player_cheat_detections WHERE account_id = :id"),
            {"id": account.id}
        )
    if "accounts_rewardcodes" in existing_tables:
        db.session.execute(
            text("DELETE FROM accounts_rewardcodes WHERE account_id = :id"),
            {"id": account.id}
        )
    # This is for GM stuff, it will be permnently delete logs
    _bulk_delete(BugReport.query.filter(BugReport.resoleved_by_id == account.id))
    _bulk_delete(AuditLog.query.filter(AuditLog.account_id == account.id))
    _bulk_delete(AccountInvitation.query.filter(AccountInvitation.invited_by_user_id == account.id))
    _bulk_delete(Account.query.filter(Account.id == account.id))
    db.session.commit()


@accounts_blueprint.route('/pass_reset/<id>', methods=['GET', 'POST'])
@login_required
@gm_level(9)
def pass_reset(id):
    # get the account
    account = Account.query.filter(Account.id == id).first()
    # make a random pass of length 12 using secrets
    raw_pass = secrets.token_urlsafe(12)
    # generate the hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(str.encode(raw_pass), salt)
    # save the has
    account.password = hashed
    account.save()
    # display for the admin to get and log that the action was done
    flash(f"Set password for account {account.username} to {raw_pass}", "success")
    log_audit(f"Reset password for {account.username}")

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

        if not current_app.config["USER_ENABLE_EMAIL"]:
            account["2"] = '''N/A'''

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

        if not current_app.config["USER_ENABLE_EMAIL"]:
            account["8"] = '''<h2 class="far fa-times-circle text-muted"></h2>'''
        elif account["8"]:
            account["8"] = '''<h2 class="far fa-check-square text-success"></h2>'''
        else:
            account["8"] = '''<h2 class="far fa-times-circle text-danger"></h2>'''

    return data

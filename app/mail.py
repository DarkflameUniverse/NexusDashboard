from flask import render_template, Blueprint, redirect, url_for, request, abort, flash, request
from flask_user import login_required, current_user
from app.models import db, Mail, CharacterInfo
from datatables import ColumnDT, DataTables
from app.forms import SendMailForm
from app import gm_level
from app.luclient import translate_from_locale, query_cdclient
import time

mail_blueprint = Blueprint('mail', __name__)


@mail_blueprint.route('/view/<id>', methods=['GET'])
@login_required
def view(id):
    mail = Mail.query.filter(Mail.id == id).first()

    return render_template('mail/view.html.j2', mail=mail)


@mail_blueprint.route('/send', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def send():
    form = SendMailForm()

    if request.method == "POST":
    # if form.validate_on_submit():
        if form.attachment.data != "0" and form.attachment_count.data == 0:
            form.attachment_count.data = 1
        if form.recipient.data == "0":
            for character in CharacterInfo.query.all():
                Mail(
                    sender_id = 0,
                    sender_name = f"[GM] {current_user.username}",
                    receiver_id = character.id,
                    receiver_name = character.name,
                    time_sent = time.time(),
                    subject = form.subject.data,
                    body = form.body.data,
                    attachment_id = 0,
                    attachment_lot = form.attachment.data,
                    attachment_count = form.attachment_count.data
                ).save()
        else:
            Mail(
                sender_id = 0,
                sender_name = f"[GM] {current_user.username}",
                receiver_id = form.recipient.data,
                receiver_name = CharacterInfo.query.filter(CharacterInfo.id == form.recipient.data).first().name,
                time_sent = time.time(),
                subject = form.subject.data,
                body = form.body.data,
                attachment_id = 0,
                attachment_lot = form.attachment.data,
                attachment_count = form.attachment_count.data
            ).save()

        flash("Sent Mail", "success")
        return redirect(url_for('mail.send'))


    recipients = CharacterInfo.query.all()
    for character in recipients:
        form.recipient.choices.append((character.id, character.name))

    items = query_cdclient(
        'Select id, name, displayName from Objects where type = ?',
        ["Loot"]
    )

    for item in items:
        name = translate_from_locale(f'Objects_{item[0]}_name')
        if name == f'Objects_{item[0]}_name':
            name = (item[2] if (item[2] != "None" and item[2] !="" and item[2] != None) else item[1])
        form.attachment.choices.append(
            (
                item[0],
                f'({item[0]}) {name}'
            )
        )


    return render_template('mail/send.html.j2', form=form)


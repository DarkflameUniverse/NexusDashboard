from flask import render_template, Blueprint, redirect, url_for, flash, request
from flask_user import login_required, current_user
from app.models import Mail, CharacterInfo
from app.forms import SendMailForm
from app import gm_level, log_audit
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
        if form.attachment.data != "0" and form.attachment_count.data == 0:
            form.attachment_count.data = 1
        if form.recipient.data == "0":
            log_audit(f"Sending {form.subject.data}: {form.body.data} to All Characters with {form.attachment_count.data} of item {form.attachment.data}")
            for character in CharacterInfo.query.all():
                Mail(
                    sender_id=0,
                    sender_name=f"[GM] {current_user.username}",
                    receiver_id=character.id,
                    receiver_name=character.name,
                    time_sent=time.time(),
                    subject=form.subject.data,
                    body=form.body.data,
                    attachment_id=0,
                    attachment_lot=form.attachment.data,
                    attachment_count=form.attachment_count.data
                ).save()
                log_audit(f"Sent {form.subject.data}: \
                    {form.body.data} to ({character.id}){character.name} \
                    with {form.attachment_count.data} of item {form.attachment.data}")
        else:
            Mail(
                sender_id=0,
                sender_name=f"[GM] {current_user.username}",
                receiver_id=form.recipient.data,
                receiver_name=CharacterInfo.query.filter(CharacterInfo.id == form.recipient.data).first().name,
                time_sent=time.time(),
                subject=form.subject.data,
                body=form.body.data,
                attachment_id=0,
                attachment_lot=form.attachment.data,
                attachment_count=form.attachment_count.data
            ).save()
            log_audit(f"Sent {form.subject.data}: \
                {form.body.data} to ({form.recipient.data}){CharacterInfo.query.filter(CharacterInfo.id == form.recipient.data).first().name} \
                with {form.attachment_count.data} of item {form.attachment.data}")

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
            name = (item[2] if (item[2] != "None" and item[2] != "" and item[2] is not None) else item[1])
        form.attachment.choices.append(
            (
                item[0],
                f'({item[0]}) {name}'
            )
        )

    return render_template('mail/send.html.j2', form=form)

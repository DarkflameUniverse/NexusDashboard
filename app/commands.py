import click
import json
from flask.cli import with_appcontext
import random, string, datetime
from flask_user import current_app
from app import db
from app.models import Account, PlayKey

@click.command("init_db")
@click.argument('drop_tables', nargs=1)
@with_appcontext
def init_db(drop_tables=False):
    """ Initialize the database."""

    print('Initializing Database.')
    if drop_tables:
        print('Dropping all tables.')
        db.drop_all()
    print('Creating all tables.')
    db.create_all()
    print('Database has been initialized.')
    return


@click.command("init_accounts")
@with_appcontext
def init_accounts():
    """ Initialize the accounts."""

    # Add accounts
    print('Creating Admin account.')
    admin_account = find_or_create_account(
        'admin',
        'example@example.com',
        'Nope',
    )


    return


def find_or_create_account(name, email, password, gm_level=9):
    """ Find existing account or create new account """
    account = Account.query.filter(Account.email == email).first()
    if not account:
        key = ""
        for j in range(4):
            key += ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(4)) + '-'
        # Remove last dash
        key = key[:-1]

        play_key = PlayKey(
            key_string=key
        )
        db.session.add(play_key)
        db.session.commit()

        play_key = PlayKey.query.filter(PlayKey.key_string == key).first()
        account = Account(email=email,
                    username=name,
                    password=current_app.user_manager.password_manager.hash_password(password),
                    play_key_id=play_key.id,
                    email_confirmed_at=datetime.datetime.utcnow(),
                    gm_level=gm_level
                )
        play_key.key_uses = 0
        db.session.add(account)
        db.session.add(play_key)
        db.session.commit()
    return # account

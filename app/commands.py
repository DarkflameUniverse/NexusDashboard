import click
import json
from flask.cli import with_appcontext
import random, string, datetime
from flask_user import current_app
from app import db
from app.models import Account, PlayKey, CharacterInfo, Property, PropertyContent, UGC
import pathlib
import zlib

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
    find_or_create_account(
        'admin',
        'example@example.com',
        'Nope',
    )

    return

@click.command("load_property")
@click.argument('zone')
@click.argument('player')
@with_appcontext
def load_property(zone, player):

    char = CharacterInfo.query.filter(CharacterInfo.name == player).first()
    if not char:
        print("Character not Found")
        return 404

    prop = Property.query.filter(Property.owner_id==char.id).filter(Property.zone_id==zone).first()

    if not prop:
        print(f"Property {zone} not claimed by Character: {char.name}")
        return 404

    prop_files = pathlib.Path('property_files/')
    for i in prop_files.glob('**/*'):
        if i.suffix == '.lxfml':
            lxfml = ""
            with open(i, "r") as file:
                lxfml = file.read()
            compressed_lxfml = zlib.compress(lxfml.encode())

            new_ugc = UGC(
                account_id=char.account_id,
                character_id=char.id,
                is_optimized=0,
                lxfml=compressed_lxfml,
                bake_ao=0,
                filename=i.name
            )
            new_ugc.save()

            new_prop_content = PropertyContent(
                id=i.stem,
                property_id=prop.id,
                ugc_id=new_ugc.id,
                lot=14,
                x=0,
                y=0,
                z=0,
                rx=0,
                ry=0,
                rz=0,
                rw=1
            )
            new_prop_content.save()


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



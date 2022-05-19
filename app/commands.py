import click
from flask.cli import with_appcontext
import random
import string
import datetime
from flask_user import current_app
from app import db
from app.models import Account, PlayKey, CharacterInfo, Property, PropertyContent, UGC, Mail
import pathlib
import zlib
from wand import image
from wand.exceptions import BlobError as BE
import app.pylddlib as ldd
from multiprocessing import Pool
from functools import partial
from sqlalchemy import func
import time
import xml.etree.ElementTree as ET
import xmltodict


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


@click.command("fix_clone_ids")
@with_appcontext
def fix_clone_ids():
    """
        Fix incorrect prop_clone_id's
        Remove duplicate properties
            Either the one with most models or most recently claimed
        Retuen Pre-built models via mail
        (May have errors and need to be run multiple times)
    """
    properties = Property.query.all()
    count = 0
    for prop in properties:
        char = CharacterInfo.query.filter(CharacterInfo.id == prop.owner_id).first()
        if char.prop_clone_id != prop.clone_id:
            count += 1
            prop.clone_id = char.prop_clone_id
            prop.save()

    print(f"Fixed {count} props where clone id did not match owner's clone id")

    dupes = 0
    characters = CharacterInfo.query.all()
    for char in characters:
        props = Property.query.with_entities(
            Property.zone_id, func.count(Property.zone_id)
        ).group_by(Property.zone_id).filter(
            Property.owner_id == char.id
        ).all()
        for prop in props:
            if prop[1] != 1:
                dupes += 1
                print(f"found dupe on {char.name}'s {prop[0]}")
                dupe_props = Property.query.filter(
                    Property.owner_id == char.id
                ).filter(
                    Property.zone_id == prop[0]).all()
                dupe_data = []
                # id, content_count
                for dprop in dupe_props:
                    dupe_data.append(
                        [
                            dprop.id,
                            PropertyContent.query.filter(PropertyContent.property_id == dprop.id).count(),
                            dprop.time_claimed
                        ]
                    )
                max_models = max(dupe_data, key=lambda x: x[1])
                if max_models[1] == 0:
                    newest = max(dupe_data, key=lambda x: x[2])
                    for data in dupe_data:
                        if data[2] != newest[2]:
                            Property.query.filter(Property.id == data[0]).first().delete()
                else:
                    for data in dupe_data:
                        if data[1] != max_models[1]:
                            contents = PropertyContent.query.filter(PropertyContent.property_id == dprop.id).all()
                            if contents:
                                for content in contents:
                                    if content.lot == 14:
                                        UGC.query.filter(content.ugc_id).first().delete()
                                        content.delete()
                                    else:
                                        Mail(
                                            sender_id=0,
                                            sender_name="System",
                                            receiver_id=char.id,
                                            receiver_name=char.name,
                                            time_sent=time.time(),
                                            subject="Returned Model",
                                            body="This model was returned to you from a property cleanup script",
                                            attachment_id=0,
                                            attachment_lot=content.lot,
                                            attachment_count=1
                                        ).save()
                                        content.delete()
                            time.sleep(1)
                            Property.query.filter(Property.id == data[0]).first().delete()
    return


@click.command("load_property")
@click.argument('zone')
@click.argument('player')
@with_appcontext
def load_property(zone, player):
    """shoves property data into db"""
    char = CharacterInfo.query.filter(CharacterInfo.name == player).first()
    if not char:
        print("Character not Found")
        return 404

    prop = Property.query.filter(Property.owner_id == char.id).filter(Property.zone_id == zone).first()

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


@click.command("gen_image_cache")
def gen_image_cache():
    """generates image cache"""
    luclient = pathlib.Path('app/luclient/res')
    files = [path for path in luclient.rglob("*.dds") if path.is_file()]

    for file in files:
        cache = get_cache_file(file).with_suffix(".png")
        if not cache.exists():
            try:
                print(f"Convert {file.as_posix()} to {cache}")
                cache.parent.mkdir(parents=True, exist_ok=True)
                with image.Image(filename=str(file.as_posix())) as img:
                    img.compression = "no"
                    img.save(filename=str(cache.as_posix()))
            except BE:
                return print(f"Error on {file}")


@click.command("gen_model_cache")
def gen_model_cache():
    """generate model obj cache"""
    luclient = pathlib.Path('app/luclient/res')
    files = [path for path in luclient.rglob("*.lxfml") if path.is_file()]
    pool = Pool(processes=4)
    pool.map(partial(convert_lxfml_to_obj, lod=0), files)
    pool.map(partial(convert_lxfml_to_obj, lod=1), files)
    pool.map(partial(convert_lxfml_to_obj, lod=2), files)


def convert_lxfml_to_obj(file, lod):
    mtl = get_cache_file(file).with_suffix(f".lod{lod}.mtl")
    if not mtl.exists():
        mtl.parent.mkdir(parents=True, exist_ok=True)
        print(f"Convert LXFML {file.as_posix()} to obj and mtl @ {mtl}")
        try:
            ldd.main(str(file.as_posix()), str(mtl.with_suffix("").as_posix()), lod)  # convert to OBJ
        except Exception as e:
            print(f"ERROR on {file}:\n {e}")
    else:
        # print(f"Already Exists: {file} with LOD {lod}")
        return


def get_cache_file(path):
    """helper"""
    # convert to list so that we can change elements
    parts = list(path.parts)

    # replace part that matches src with dst
    parts[parts.index("luclient")] = "cache"
    del parts[parts.index("res")]

    return pathlib.Path(*parts)


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
        account = Account(
            email=email,
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
    return  # account


@click.command("split_ugc")
@click.argument('path')
def split_ugc(path):
    base = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<LXFML versionMajor="5" versionMinor="0">
<Meta>
    <Application name="LEGO Universe" versionMajor="0" versionMinor="0"/>
    <Brand name="LEGOUniverse"/>
    <BrickSet version="457"/>
</Meta>
<Bricks>
</Bricks>
<RigidSystems>
</RigidSystems>
<GroupSystems>
    <GroupSystem>
    </GroupSystem>
</GroupSystems>
</LXFML>
"""
    # create element tree object
    orig_lxfml = ET.parse(path)

    rigidsystems = orig_lxfml.findall('.//RigidSystem')
    # print(len(rigidsystems))
    rigids_parts = {}
    i = 0
    for rigidsytem in rigidsystems:
        rigids = rigidsytem.findall('.//Rigid')
        rigids_parts[i] = []
        for rigid in rigids:
            rigids_parts[i].extend(rigid.attrib['boneRefs'].split(','))
        i += 1
    # print(rigids_parts)
    groups = orig_lxfml.findall('.//Group')

    # print(len(groups))
    groups_parts = []
    for group in groups:
        groups_parts.append(group.attrib['partRefs'].split(','))
    # print(groups_parts)

    # our output
    models = []
    g = 0
    # get things by group
    if len(groups_parts) > 0:
        for group in groups_parts:
            tmp_model = {"bricks": [], "rigidsystems": [], "group": g}

            for brick in group:
                # find rigids
                rigid = None
                for k, v in rigids_parts.items():
                    if brick in v:
                        tmp_model["rigidsystems"].extend(str(k))
                        tmp_model["bricks"].extend(rigids_parts[k])
                        # delete the rigid so that we do dupe it in the next step
                        del rigids_parts[k]
                        break
            models.append(tmp_model)
        g += 1
    # get stuff by rigids
    if len(rigids_parts) > 0:
        for k, v in rigids_parts.items():
            tmp_model = {"bricks": [], "rigidsystems": []}
            tmp_model["rigidsystems"].extend(str(k))
            tmp_model["bricks"].extend(rigids_parts[k])
            models.append(tmp_model)
    # print(models)

    # make out lxfml files
    output_xmls = []
    if len(models) > 0:
        for model in models:
            new_xml = ET.fromstring(base)
            for key, v in model.items():
                if key == "bricks":
                    bricks = new_xml.find(".//Bricks")
                    for brick in model[key]:
                        # get brick and then add it to our new xml
                        bricks.append(orig_lxfml.find(f".//Brick[@refID='{brick}']"))
                if key == "rigidsystems":
                    new_rigidsystems = new_xml.find(".//RigidSystems")
                    for rigidsystem in model[key]:
                        new_rigidsystems.append(rigidsystems[int(rigidsystem)])
                if key == "group":
                    new_groupsystem = new_xml.find(".//GroupSystem")
                    new_groupsystem.append(groups[v])
            output_xmls.append(new_xml)
    else:
        raise Exception("WHY ARE THERE NO MODELS????")

    for xml in output_xmls:
        rigidsystems = xml.findall('.//RigidSystem')
        rigids_parts = {}
        i = 0
        for rigidsytem in rigidsystems:
            rigids = rigidsytem.findall('.//Rigid')
            for rigid in rigids:
                bricks = rigid.attrib['boneRefs'].split(',')
                transformation = list(map(float, rigid.attrib['transformation'].split(',')))
                print(f"x: {transformation[-3]}")
                print(f"y: {transformation[-2]}")
                print(f"z: {transformation[-1]}")
                for brickID in bricks:
                    brick = xml.find(f".//Bone[@refID='{brickID}']")
                    old_transform = list(map(float, brick.attrib['transformation'].split(',')))
                    old_transform[-1] = old_transform[-1] - transformation[-1]
                    old_transform[-2] = old_transform[-2] - transformation[-2]
                    old_transform[-3] = old_transform[-3] - transformation[-3]
                    new_transform = ','.join(map(str, old_transform))
                    brick.set("transformation", new_transform)

        print(ET.tostring(xml))

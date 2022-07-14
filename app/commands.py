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
import csv
import json
from app.cdclient import (
    ComponentsRegistry,
    RenderComponent,
    ItemComponent,
    Objects,
    ScriptComponent,
)

from app.luclient import translate_from_locale

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

@click.command("parse_lucache")
@with_appcontext
def parse_lucache():
    """Parses lucache csv file dump from nexus hq"""
    unlisted_ids = [146, 147, 938, 1180, 1692, 1715, 1797, 1799, 1824, 1846, 1847, 1848, 1849, 1850, 1872, 1877, 1887, 1928, 1937, 1968, 1970, 1971, 1972, 1974, 1976, 1977, 1978, 1979, 1980, 1981, 1983, 1984, 2189, 2401, 2402, 2403, 2404, 2405, 2406, 2407, 2408, 2416, 2417, 2418, 2420, 2421, 2422, 2423, 2424, 2425, 2426, 2427, 2429, 2430, 2431, 2432, 2433, 2434, 2435, 2436, 2529, 2530, 2553, 2583, 2655, 2656, 2669, 2947, 2948, 3009, 3058, 3068, 3078, 3807, 3812, 3937, 4828, 4874, 4875, 4876, 4877, 4943, 4954, 5839, 5840, 6196, 6218, 6219, 6221, 6433, 6471, 6696, 6821, 6877, 6888, 6889, 6891, 6892, 6893, 6894, 6896, 6897, 6983, 7277, 7551, 7552, 7553, 7554, 7609, 7701, 7713, 7723, 7753, 7754, 7755, 7756, 7760, 7777, 7791, 7824, 7872, 8046, 8053, 8146, 9865, 9866, 9867, 9868, 10126, 10291, 10292, 10293, 10294, 10518, 10630, 10631, 10987, 11511, 11512, 11513, 11514, 11515, 11516, 11517, 11518, 11519, 11520, 11521, 11522, 11523, 11524, 11525, 12096, 12097, 12099, 12100, 12104, 12105, 12111, 12112, 12113, 12324, 12325, 12326, 12553, 12666, 12668, 12670, 12671, 12673, 12674, 12676, 12679, 12680, 12683, 12684, 12685, 12687, 12692, 12694, 12697, 12699, 12701, 12703, 12704, 12713, 12716, 12717, 12727, 12736, 12738, 12739, 12745, 12746, 12750, 12751, 12752, 12757, 12787, 12790, 12791, 12794, 12795, 12799, 12800, 12803, 12887, 12888, 12902, 12904, 12905, 12906, 12907, 12941, 13060, 13061, 13071, 13075, 13076, 13077, 13092, 13093, 13094, 13106, 13118, 13121, 13126, 13127, 13150, 13191, 13192, 13275, 13276, 13277, 13278, 13280, 13295, 13410, 13411, 13510, 13638, 13740, 13742, 13776, 13782, 13905, 13925, 13926, 13927, 13928, 13929, 13930, 13931, 13932, 13953, 13958, 13974, 13996, 13997, 13998, 13999, 14000, 14001, 14002, 14056, 14057, 14058, 14059, 14060, 14061, 14062, 14063, 14064, 14065, 14066, 14067, 14068, 14069, 14070, 14071, 14072, 14073, 14074, 14075, 14076, 14077, 14078, 14079, 14080, 14081, 14090, 14094, 14111, 14135, 14140, 14170, 14171, 14188, 14200, 14202, 14206, 14207, 14208, 14209, 14210, 14211, 14212, 14213, 14228, 14229, 14314, 14428, 14483, 14515, 14522, 14531, 14535, 14536, 14538, 14548, 14554, 14587, 14588, 14589, 14597, 14598, 14599, 14605, 14607, 14608, 14609, 14610, 14611, 14612, 14613, 14614, 14615, 14616, 14617, 14618, 14619, 14620, 14621, 14622, 14623, 14624, 14625, 14626, 14627, 14628, 14629, 14630, 14631, 14632, 14633, 14634, 14635, 14636, 14637, 14638, 14639, 14640, 14641, 14642, 14643, 14644, 14645, 14646, 14647, 14648, 14649, 14650, 14651, 14652, 14653, 14654, 14655, 14656, 14657, 14658, 14659, 14660, 14661, 14662, 14663, 14664, 14665, 14666, 14667, 14668, 14686, 14687, 14688, 14689, 14690, 14704, 14706, 14707, 14716, 14717, 14721, 14722, 14727, 14728, 14729, 14779, 14795, 14799, 14800, 14803, 14815, 14820, 14821, 14822, 14823, 14824, 14825, 14826, 14827, 14831, 14832, 14838, 14839, 15852, 15853, 15854, 15855, 15856, 15857, 15858, 15859, 15860, 15861, 15862, 15863, 15864, 15865, 15885, 15886, 15887, 15888, 15889, 15893, 15894, 15898, 15921, 15923, 15925, 15928, 15930, 15931, 15932, 15933, 15934, 15938, 15939, 15940, 15941, 15942, 15945, 15958, 15962, 15963, 15964, 15965, 15966, 15967, 15968, 15969, 15970, 15971, 15972, 15973, 15981, 15984, 15985, 15986, 15987, 15988, 15989, 15996, 15997, 15998, 15999, 16000, 16001, 16002, 16003, 16004, 16005, 16007, 16008, 16009, 16010, 16011, 16025, 16026, 16027, 16028, 16036, 16039, 16042, 16046, 16051, 16056, 16071, 16072, 16073, 16074, 16075, 16077, 16078, 16079, 16080, 16081, 16089, 16090, 16091, 16092, 16108, 16109, 16110, 16111, 16112, 16113, 16114, 16115, 16116, 16117, 16124, 16125, 16126, 16127, 16128, 16129, 16130, 16137, 16138, 16139, 16140, 16142, 16145, 16167, 16168, 16169, 16170, 16171, 16172, 16173, 16174, 16175, 16176, 16177, 16200, 16201, 16202, 16204, 16212, 16253, 16254, 16418, 16437, 16469, 16479, 16489, 16505, 16641, 16645, 16646, 16648, 16655, 16658, 16659, 16660, 16661, 16662, 16665, 16666, 16667, 16668, 16669, 16670, 16671, 16672, 16673, 16674, 16675, 16676, 16677, 16678, 16679, 16680, 16681, 16685, 16686, 16687, 16688, 16689, 16690, 16691, 16692, 16693, 16694, 16695, 16696, 16697, 16698, 16699, 16700, 16701, 16702, 16703, 16704, 16705, 16706, 16707, 16708, 16709, 16712, 16714, 16717, 16718, 16719, 16720, 16721, 16722, 16724, 16725, 16726, 16727, 16732, 16733, 16734, 16735] # noqa
    with open("lucache.csv") as cache_file:
        csv_reader = csv.reader(cache_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if row[0] == "id":
                continue
            if int(row[0]) in unlisted_ids:
                json_data = json.loads(row[2])
                components = ComponentsRegistry.query.filter(ComponentsRegistry.id == int(row[0])).all()
                obj_type = "Environmental"
                desc = json_data["Description"]
                if desc in ["None", None, ""]:
                    desc = row[1]
                nametag = 0
                npcTemplateID = "null"
                for comp in components:
                    if comp.component_type == 7:  # Item
                        obj_type = "Smashable"
                    if comp.component_type == 11:  # Item
                        obj_type = "Loot"
                    if comp.component_type == 35:  # minifig
                        obj_type = "NPC"
                        npcTemplateID = comp.component_id
                        nametag = 1
                    if comp.component_type == 42:  # b3
                        obj_type = "Behavior"
                    if comp.component_type == 60:  # base combat ai
                        obj_type = "Enemy"
                    if comp.component_type == 73:  # mission giver
                        if obj_type != "NPC":
                            obj_type = "Structure"
                        desc = f"__MG__{desc}"
                if "vendor" in row[1].lower():
                    obj_type = "NPC"
                print(f"""INSERT INTO "Objects" ("id","name","placeable","type","description","localize","npcTemplateID","displayName","interactionDistance","nametag","_internalNotes","locStatus","gate_version","HQ_valid") VALUES ("{row[0]}", "{row[1].replace("_", " ")}", 1, "{obj_type}", "{desc}", 1, {npcTemplateID} , "{json_data["DisplayName"]}", null , {nametag}, "Unlisted Object", 0, null, 1);""")
                if obj_type in ["NPC", "Smashable", "Loot"]:
                    print(f"""        <phrase id="Objects_{row[0]}_name">
            <translation locale="en_US">{row[1]}</translation>
            <translation locale="de_DE">TRASNSLATE UNLISTED</translation>
            <translation locale="en_GB">{row[1]}</translation>
        </phrase>
        <phrase id="Objects_{row[0]}_description">
            <translation locale="en_US">{desc}</translation>
            <translation locale="de_DE">TRASNSLATE UNLISTED</translation>
            <translation locale="en_GB">{desc}</translation>
        </phrase>""")
                # print(f'{row[0]}: {json_data["DisplayName"]}')
                line_count += 1
        # print(f'Processed {line_count} lines.')


@click.command("makeup_unlisted_objects")
@with_appcontext
def makeup_unlisted_objects():
    objs_left = []
    for obj in objs_left:
        obj_type = "Environmental"
        nametag = 0
        name = "Name Missing"
        desc = "null"
        npcTemplateID = "null"
        components = ComponentsRegistry.query.filter(ComponentsRegistry.id == obj).all()
        for comp in components:
            if comp.component_type == 2:  # render
                render = RenderComponent.query.filter(RenderComponent.id == comp.component_id).first()
                if render is not None:

                    if render.render_asset not in [None, ""]:
                        name = render.render_asset.replace("_", " ").split('\\')[-1].split('/')[-1].split('.')[0].lower()
                    if name == "Name Missing":
                        if render.icon_asset not in [None, ""]:
                            name = render.icon_asset.replace("_", " ").split('\\')[-1].split('/')[-1].split('.')[0].lower()
                    name  = name.replace("env ", "").replace("obj ", "").replace("minifig accessory ", "").replace("", "").replace("mf ", "").replace("cre ", "")
                    # print(f"{obj}: {name} :  {alt_name}")
                    obj_type = "Smashable"
                # else:
                    # print(f"{obj}: No Render")
            if comp.component_type == 7:  # destroyable
                obj_type = "Smashable"
            if comp.component_type == 11:  # Item
                item = ItemComponent.query.filter(ItemComponent.id == comp.component_id).first()
                if item.itemType == 24:
                    obj_type = "Mount"
                else:
                    obj_type = "Loot"
            if comp.component_type == 35:  # minifig
                obj_type = "NPC"
                npcTemplateID = comp.component_id
                nametag = 1
            if comp.component_type == 42:  # b3
                obj_type = "Behavior"
            if comp.component_type == 60:  # base combat ai
                obj_type = "Enemy"
            if comp.component_type == 73:  # mission giver
                if obj_type != "NPC":
                    obj_type = "Structure"
                desc = f"__MG__{name}"
        # print(f"""INSERT INTO "Objects" ("id","name","placeable","type","description","localize","npcTemplateID","displayName","interactionDistance","nametag","_internalNotes","locStatus","gate_version","HQ_valid") VALUES ("{obj}", "{name}", 1, "{obj_type}", "{desc}", 1, {npcTemplateID} , "{name}", null , {nametag}, "Unlisted Object", 0, null, 1);""")
        if name != "Name Missing" and obj_type in ["Mount"]:
            print(f"""        <phrase id="Objects_{obj}_name">
            <translation locale="en_US">{name}</translation>
            <translation locale="de_DE">TRASNSLATE UNLISTED</translation>
            <translation locale="en_GB">{name}</translation>
        </phrase>""")


@click.command("gen_new_locales")
@with_appcontext
def gen_new_locales():
    objects = Objects.query.order_by(Objects.id).all()
    for obj in objects:
        if obj.type == "Loot":
            if obj.name not in ["Name Missing", None, "None"] and obj.name[:1] != "m":
                name_to_trans = f"Object_{obj.id}_name"
                name_transed = translate_from_locale(name_to_trans)
                if name_to_trans == name_transed:
                    print(f"""        <phrase id="Objects_{obj.id}_name">
            <translation locale="en_US">{obj.name}</translation>
            <translation locale="de_DE">TRASNSLATE OLD</translation>
            <translation locale="en_GB">{obj.name}</translation>
        </phrase>""")
            if obj.description not in ["None", None, ""]:
                description_to_trans = f"Object_{obj.id}_description"
                description_transed = translate_from_locale(description_to_trans)
                if description_to_trans == description_transed:
                    print(f"""        <phrase id="Objects_{obj.id}_description">
            <translation locale="en_US">{obj.description}</translation>
            <translation locale="de_DE">TRASNSLATE OLD</translation>
            <translation locale="en_GB">{obj.description}</translation>
        </phrase>""")


@click.command("xref_scripts")
@with_appcontext
def xref_scripts():
    """cross refernce scripts dir with script component table"""
    scripts = ScriptComponent.query.all()
    base = 'app/luclient/res/'
    server = 0
    server_total = 0
    client = 0
    client_total = 0
    server_used = 0
    client_used = 0
    used_total = 0
    disk_scripts = [path for path in pathlib.Path('app/luclient/res/scripts').rglob("*.lua") if path.is_file()]

    for script in scripts:
        script_comps = ComponentsRegistry.query.filter(ComponentsRegistry.component_type == 5).filter(ComponentsRegistry.component_id == script.id).all()
        if len(script_comps) > 0:
            used_total += 1
        if script.client_script_name not in [None, ""]:
            cleaned_name = script.client_script_name.replace('\\', '/').lower()
            client_script = pathlib.Path(f"{base}{cleaned_name}")
            client_total += 1
            if not client_script.is_file():
                print(f"Missing Server Script: {client_script.as_posix()}")
                client += 1
                if len(script_comps) > 0:
                    client_used += 1
        if script.script_name not in [None, ""]:
            cleaned_name = script.script_name.replace('\\', '/').lower()
            server_script = pathlib.Path(f"{base}{cleaned_name}")
            server_total += 1
            if not server_script.is_file():
                print(f"Missing Client Script: {server_script.as_posix()}")
                server += 1
                if len(script_comps) > 0:
                    server_used += 1

    print(f"Missing {server}/{server_total} server scripts")
    print(f"Missing {client}/{client_total} client scripts")
    print(f"Missing {server_used}/{used_total} used server scripts")
    print(f"Missing {client_used}/{used_total} used client scripts")
    print(f"Total cdclient scripts {server_total + client_total}\nTotal disk scripts {len(disk_scripts)}")


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

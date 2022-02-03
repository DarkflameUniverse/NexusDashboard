from flask import (
    Blueprint,
    send_file,
    g,
    redirect,
    url_for
)
from flask_user import login_required
from app.models import CharacterInfo
import glob
import os
from wand import image
from wand.exceptions import BlobError as BE
import pathlib

import sqlite3
import xml.etree.ElementTree as ET

luclient_blueprint = Blueprint('luclient', __name__)
locale = {}

@luclient_blueprint.route('/get_dds_as_png/<filename>')
@login_required
def get_dds_as_png(filename):
    if filename.split('.')[-1] != 'dds':
        return (404, "NO")

    cache = f'cache/{filename.split(".")[0]}.png'

    if not os.path.exists(cache):
        root = 'app/luclient/res/'

        path = glob.glob(
            root + f'**/{filename}',
            recursive=True
        )[0]

        with image.Image(filename=path) as img:
            img.compression = "no"
            img.save(filename='app/cache/'+filename.split('.')[0] + '.png')

    return send_file(cache)


@luclient_blueprint.route('/get_dds/<filename>')
@login_required
def get_dds(filename):
    if filename.split('.')[-1] != 'dds':
        return 404

    root = 'app/luclient/res/'

    dds = glob.glob(
        root + f'**/{filename}',
        recursive=True
    )[0]

    return send_file(dds)


@luclient_blueprint.route('/get_icon_lot/<id>')
@login_required
def get_icon_lot(id):

    render_component_id = query_cdclient(
        'select component_id from ComponentsRegistry where component_type = 2 and id = ?',
        [id],
        one=True
    )[0]

    # find the asset from rendercomponent given the  component id
    filename = query_cdclient('select icon_asset from RenderComponent where id = ?',
        [render_component_id],
        one=True
    )[0]

    filename = filename.replace("..\\", "").replace("\\", "/")

    cache = f'app/cache/{filename.split(".")[0]}.png'

    if not os.path.exists(cache):
        root = 'app/luclient/res/'
        try:
            pathlib.Path(os.path.dirname(cache)).resolve().mkdir(parents=True, exist_ok=True)
            with image.Image(filename=f'{root}{filename}'.lower()) as img:
                img.compression = "no"
                img.save(filename=cache)
        except BE:
            return redirect(url_for('luclient.unknown'))

    return send_file(pathlib.Path(cache).resolve())


@luclient_blueprint.route('/get_icon_iconid/<id>')
@login_required
def get_icon_iconid(id):

    filename = query_cdclient(
        'select IconPath from Icons where IconID = ?',
        [id],
        one=True
    )[0]

    filename = filename.replace("..\\", "").replace("\\", "/")

    cache = f'app/cache/{filename.split(".")[0]}.png'

    if not os.path.exists(cache):
        root = 'app/luclient/res/'
        try:
            pathlib.Path(os.path.dirname(cache)).resolve().mkdir(parents=True, exist_ok=True)
            with image.Image(filename=f'{root}{filename}'.lower()) as img:
                img.compression = "no"
                img.save(filename=cache)
        except BE:
            return redirect(url_for('luclient.unknown'))

    return send_file(pathlib.Path(cache).resolve())

@luclient_blueprint.route('/unknown')
@login_required
def unknown():
    filename = "textures/ui/inventory/unknown.dds"

    cache = f'app/cache/{filename.split(".")[0]}.png'

    if not os.path.exists(cache):
        root = 'app/luclient/res/'
        try:
            pathlib.Path(os.path.dirname(cache)).resolve().mkdir(parents=True, exist_ok=True)
            with image.Image(filename=f'{root}{filename}'.lower()) as img:
                img.compression = "no"
                img.save(filename=cache)
        except BE:
            return redirect(url_for('luclient.unknown'))

    return send_file(pathlib.Path(cache).resolve())


def get_cdclient():
    """Connect to CDClient from file system Relative Path

    Args:
        None
    """
    cdclient = getattr(g, '_cdclient', None)
    if cdclient is None:
        cdclient = g._database = sqlite3.connect('app/luclient/res/cdclient.sqlite')
    return cdclient


def query_cdclient(query, args=(), one=False):
    """Run sql queries on CDClient

    Args:
        query   (string)    : SQL query
        args    (list)      : List of args to place in query
        one     (bool)      : Return only on result or all results
    """
    cur = get_cdclient().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def translate_from_locale(trans_string):
    """Finds the string translation from locale.xml

    Args:
        trans_string   (string)    : ID to find translation
    """
    if not trans_string:
        return "INVALID STRING"

    global locale

    locale_data = ""

    if not locale:
        locale_path = "app/luclient/locale/locale.xml"

        with open(locale_path, 'r') as file:
            locale_data = file.read()
        locale_xml = ET.XML(locale_data)
        for item in locale_xml.findall('.//phrase'):
            translation = ""
            for translation_item in item.findall('.//translation'):
                if translation_item.attrib["locale"] == "en_US":
                    translation = translation_item.text

            locale[item.attrib['id']] = translation

    if trans_string in locale:
        return locale[trans_string]
    else:
        return trans_string

def register_luclient_jinja_helpers(app):

    @app.template_filter('get_zone_name')
    def get_zone_name(zone_id):
        return translate_from_locale(f'ZoneTable_{zone_id}_DisplayDescription')

    @app.template_filter('get_skill_desc')
    def get_skill_desc(skill_id):
        return translate_from_locale(f'SkillBehavior_{skill_id}_descriptionUI').replace(
                "%(DamageCombo)", "Damage Combo: "
            ).replace(
                "%(AltCombo)", "<br/>Skeleton Combo: "
            ).replace(
                "%(Description)", "<br/>"
            ).replace(
                "%(ChargeUp)", "<br/>Charge-up: "
            )

    @app.template_filter('parse_lzid')
    def parse_lzid(lzid):
        return[
            (int(lzid) & ((1 << 16) - 1)),
            ((int(lzid) >> 16) & ((1 << 16) - 1)),
            ((int(lzid) >> 32) & ((1 << 30) - 1))
        ]

    @app.template_filter('parse_other_player_id')
    def parse_other_player_id(other_player_id):
        char_id = (int(other_player_id) & 0xFFFFFFFF)
        character = CharacterInfo.query.filter(CharacterInfo.id == char_id).first()
        if character:
            return[character.id, character.name]
        else:
            return None

    @app.template_filter('get_lot_name')
    def get_lot_name(lot_id):
        name = translate_from_locale(f'Objects_{lot_id}_name')
        if name == f'Objects_{lot_id}_name':
            intermed = query_cdclient(
                'select * from Objects where id = ?',
                [lot_id],
                one=True
            )
            if intermed:
                name = intermed[7] if (intermed[7] != "None" and intermed[7] !="" and intermed[7] != None) else intermed[1]
        return name

    @app.template_filter('get_lot_rarity')
    def get_lot_rarity(lot_id):

        render_component_id = query_cdclient(
            'select component_id from ComponentsRegistry where component_type = 11 and id = ?',
            [lot_id],
            one=True
        )[0]

        rarity = query_cdclient('select rarity from ItemComponent where id = ?',
            [render_component_id],
            one=True
        )
        if rarity:
            rarity = rarity[0]
        return rarity

    @app.template_filter('get_lot_desc')
    def get_lot_desc(lot_id):
        desc = translate_from_locale(f'Objects_{lot_id}_description')
        if desc == f'Objects_{lot_id}_description':
            desc = query_cdclient(
                'select description from Objects where id = ?',
                [lot_id],
                one=True
            )[0]
            if desc in ("", None):
                desc = None
        return desc

    @app.template_filter('get_item_set')
    def check_if_in_set(lot_id):
        item_set = query_cdclient(
            'select * from ItemSets where itemIDs like ? or itemIDs like ? or itemIDs like ?',
            [f'{lot_id}%', f'%, {lot_id}%', f'%,{lot_id}%'],
            one=True
        )
        if item_set in ("", None):
            return None
        else:
            return item_set

    @app.template_filter('get_lot_stats')
    def get_lot_stats(lot_id):
        stats = query_cdclient(
            'SELECT imBonusUI, lifeBonusUI, armorBonusUI, skillID, skillIcon FROM SkillBehavior WHERE skillID IN (\
                SELECT skillID FROM ObjectSkills WHERE objectTemplate=?\
                )',
            [lot_id]
        )

        return consolidate_stats(stats)


    @app.template_filter('get_set_stats')
    def get_set_stats(lot_id):
        stats = query_cdclient(
            'SELECT imBonusUI, lifeBonusUI, armorBonusUI, skillID, skillIcon FROM SkillBehavior WHERE skillID IN (\
                SELECT skillID FROM ItemSetSkills WHERE SkillSetID=?\
                )',
            [lot_id]
        )

        return consolidate_stats(stats)

    @app.template_filter('query_cdclient')
    def jinja_query_cdclient(query, items):
        print(query, items)
        return query_cdclient(
            query,
            items,
            one=True
        )[0]

    @app.template_filter('lu_translate')
    def lu_translate(to_translate):
        return translate_from_locale(to_translate)


def consolidate_stats(stats):

    if len(stats) > 1:
        consolidated_stats = {"im": 0,"life": 0,"armor": 0, "skill": []}
        for stat in stats:
            if stat[0]:
                consolidated_stats["im"] += stat[0]
            if stat[1]:
                consolidated_stats["life"] += stat[1]
            if stat[2]:
                consolidated_stats["armor"] += stat[2]
            if stat[3]:
                consolidated_stats["skill"].append([stat[3],stat[4]])


        stats = consolidated_stats
    elif len(stats) == 1:
        stats = {
            "im": stats[0][0] if stats[0][0] else 0,
            "life": stats[0][1] if stats[0][1] else 0,
            "armor": stats[0][2] if stats[0][2] else 0,
            "skill": [[stats[0][3], stats[0][4]]] if stats[0][3] else None,
        }
    else:
        stats = None
    return stats

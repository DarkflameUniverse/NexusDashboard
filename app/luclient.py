from flask import (
    Blueprint,
    send_file,
    g,
    redirect,
    url_for,
    make_response,
    abort
)
from flask_user import login_required
from app.models import CharacterInfo
from app.cdclient import (
    Objects,
    Icons,
    ItemSets,
    ComponentsRegistry,
    ComponentType,
    RenderComponent,
    ItemComponent,
    ObjectSkills,
    SkillBehavior
)
import glob
import os
from wand import image
from wand.exceptions import BlobError as BE
import pathlib
import json

import xml.etree.ElementTree as ET
from sqlalchemy import or_

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
            img.save(filename='app/cache/' + filename.split('.')[0] + '.png')

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
    icon_path = RenderComponent.query.filter(
        RenderComponent.id == ComponentsRegistry.query.filter(
            ComponentsRegistry.component_type == ComponentType.COMPONENT_TYPE_RENDER
        ).filter(ComponentsRegistry.id == id).first().component_id
    ).first().icon_asset

    if icon_path:
        icon_path = icon_path.replace("..\\", "").replace("\\", "/")
    else:
        return redirect(url_for('luclient.unknown'))

    cache = f'app/cache/{icon_path.split(".")[0]}.png'

    if not os.path.exists(cache):
        root = 'app/luclient/res/'
        try:
            pathlib.Path(os.path.dirname(cache)).resolve().mkdir(parents=True, exist_ok=True)
            with image.Image(filename=f'{root}{icon_path}'.lower()) as img:
                img.compression = "no"
                img.save(filename=cache)
        except BE:
            return redirect(url_for('luclient.unknown'))

    return send_file(pathlib.Path(cache).resolve())


@luclient_blueprint.route('/get_icon_iconid/<id>')
@login_required
def get_icon_iconid(id):

    filename = Icons.query.filter(Icons.IconID == id).first().IconPath

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


@luclient_blueprint.route('/ldddb/')
@login_required
def brick_list():
    brick_list = []
    if len(brick_list) == 0:
        suffixes = [".g", ".g1", ".g2", ".g3", ".xml"]
        res = pathlib.Path('app/luclient/res/')
        # Load g files
        for path in res.rglob("*.*"):
            if str(path.suffix) in suffixes:
                brick_list.append(
                    {
                        "type": "file",
                        "name": str(path.as_posix()).replace("app/luclient/res/", "")
                    }
                )
    response = make_response(json.dumps(brick_list))
    response.headers.set('Content-Type', 'application/json')
    return response


@luclient_blueprint.route('/ldddb/', defaults={'req_path': ''})
@luclient_blueprint.route('/ldddb/<path:req_path>')
def dir_listing(req_path):
    # Joining the base and the requested path
    rel_path = pathlib.Path(str(pathlib.Path(f'app/luclient/res/{req_path}').resolve()))
    # Return 404 if path doesn't exist
    if not rel_path.exists():
        return abort(404)

    # Check if path is a file and serve
    if rel_path.is_file():
        return send_file(rel_path)
    else:
        return abort(404)


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


def get_lot_name(lot_id):
    if not lot_id:
        return "Missing"
    name = translate_from_locale(f'Objects_{lot_id}_name')
    if name == f'Objects_{lot_id}_name':
        intermed = Objects.query.filter(Objects.id == lot_id).first()
        if intermed:
            name = intermed.displayName if (intermed.displayName != "None" or intermed.displayName != "" or intermed.displayName == None) else intermed.name
    if not name:
        name = f'Objects_{lot_id}_name'
    return name


def register_luclient_jinja_helpers(app):

    @app.template_filter('get_zone_name')
    def get_zone_name(zone_id):
        if not zone_id:
            return "Missing"
        return translate_from_locale(f'ZoneTable_{zone_id}_DisplayDescription')

    @app.template_filter('get_skill_desc')
    def get_skill_desc(skill_id):
        return translate_from_locale(
            f'SkillBehavior_{skill_id}_descriptionUI'
        ).replace(
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
    def jinja_get_lot_name(lot_id):
        return get_lot_name(lot_id)

    @app.template_filter('get_lot_rarity')
    def get_lot_rarity(lot_id):
        if not lot_id:
            return "Missing"
        rarity = ItemComponent.query.filter(
            ItemComponent.id == ComponentsRegistry.query.filter(
                ComponentsRegistry.component_type == ComponentType.COMPONENT_TYPE_ITEM
            ).filter(ComponentsRegistry.id == id).first().component_id
        ).first().rarity
        return rarity

    @app.template_filter('get_lot_desc')
    def get_lot_desc(lot_id):
        if not lot_id:
            return "Missing"
        desc = translate_from_locale(f'Objects_{lot_id}_description')
        if desc == f'Objects_{lot_id}_description':
            desc = Objects.query.filter(Objects.id == lot_id).first()

            if desc in ("", None):
                desc = None
            else:
                desc = desc.description
                if desc in ("", None):
                    desc = None
        if desc:
            desc = desc.replace('"', "&#8220;")
        return desc

    @app.template_filter('get_item_set')
    def check_if_in_set(lot_id):
        if not lot_id:
            return None
        item_set = ItemSets.query.filter(
            or_(
                ItemSets.itemIDs.like(f'{lot_id}%'),
                ItemSets.itemIDs.like(f'%, {lot_id}%'),
                ItemSets.itemIDs.like(f'%,{lot_id}%')
            )
        ).first()

        if item_set in ("", None):
            return None
        else:
            return item_set

    @app.template_filter('get_lot_stats')
    def get_lot_stats(lot_id):
        if not lot_id:
            return None
        stats = SkillBehavior.query.with_entities(
            SkillBehavior.imBonusUI,
            SkillBehavior.lifeBonusUI,
            SkillBehavior.armorBonusUI,
            SkillBehavior.skillID,
            SkillBehavior.skillIcon
        ).filter(
            SkillBehavior.skillID in ObjectSkills.query.with_entities(
                ObjectSkills.skillID
            ).filter(
                ObjectSkills.objectTemplate == lot_id
            ).all()
        ).all()

        return consolidate_stats(stats)

    @app.template_filter('get_set_stats')
    def get_set_stats(lot_id):
        if not lot_id:
            return "Missing"
        stats = SkillBehavior.query.with_entities(
            SkillBehavior.imBonusUI,
            SkillBehavior.lifeBonusUI,
            SkillBehavior.armorBonusUI,
            SkillBehavior.skillID,
            SkillBehavior.skillIcon
        ).filter(
            SkillBehavior.skillID == ObjectSkills.query.with_entities(
                ObjectSkills.skillID
            ).filter(
                ObjectSkills.objectTemplate == lot_id
            ).all()
        ).all()

        return consolidate_stats(stats)


    @app.template_filter('lu_translate')
    def lu_translate(to_translate):
        return translate_from_locale(to_translate)


def consolidate_stats(stats):

    if stats:
        consolidated_stats = {"im": 0, "life": 0, "armor": 0, "skill": []}
        for stat in stats:
            if stat.imBonusUI:
                consolidated_stats["im"] += stat.imBonusUI
            if stat.lifeBonusUI:
                consolidated_stats["life"] += stat.lifeBonusUI
            if stat.armorBonusUI:
                consolidated_stats["armor"] += stat.armorBonusUI
            if stat.skillID:
                consolidated_stats["skill"].append([stat.skillID, stat.skillIcon])
        stats = consolidated_stats
    else:
        stats = None
    return stats

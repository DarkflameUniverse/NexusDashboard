from flask import render_template, Blueprint, redirect, url_for, request, abort, flash, make_response
from flask_user import login_required, current_user
import json
from datatables import ColumnDT, DataTables
import datetime, time
from app.models import CharacterInfo, CharacterXML, Account, db
from app.schemas import CharacterInfoSchema
from app import gm_level, log_audit
import xmltodict

character_blueprint = Blueprint('characters', __name__)

character_schema = CharacterInfoSchema()

@character_blueprint.route('/', methods=['GET'])
@login_required
@gm_level(3)
def index():
    return render_template('character/index.html.j2')


@character_blueprint.route('/approve_name/<id>/<action>', methods=['GET'])
@login_required
@gm_level(3)
def approve_name(id, action):
    character =  CharacterInfo.query.filter(CharacterInfo.id == id).first()

    if action == "approve":
        log_audit(f"Approved ({character.id}){character.pending_name} from {character.name}")
        flash(
            f"Approved ({character.id}){character.pending_name} from {character.name}",
            "success"
        )
        if character.pending_name:
            character.name = character.pending_name
            character.pending_name = ""
        character.needs_rename = False

    elif action == "rename":
        character.needs_rename = True
        log_audit(f"Marked character ({character.id}){character.name} (Pending Name: {character.pending_name if character.pending_name else 'None'}) as needing Rename")
        flash(
            f"Marked character {character.name} (Pending Name: {character.pending_name if character.pending_name else 'None'}) as needing Rename",
            "danger"
        )

    character.save()
    return redirect(request.referrer if request.referrer else url_for("main.index"))


@character_blueprint.route('/view/<id>', methods=['GET'])
@login_required
def view(id):

    character_data = CharacterInfo.query.filter(CharacterInfo.id == id).first()

    if character_data == {}:
        abort(404)
        return

    if current_user.gm_level < 3:
        if character_data.account_id and character_data.account_id != current_user.id:
            abort(403)
            return
    character_json = xmltodict.parse(
            CharacterXML.query.filter(
                CharacterXML.id==id
            ).first().xml_data,
            attr_prefix="attr_"
        )

    # print json for reference
    # with open("errorchar.json", "a") as file:
    #     file.write(
    #         json.dumps(character_json, indent=4)
    #     )

    # stupid fix for jinja parsing
    character_json["obj"]["inv"]["holdings"] = character_json["obj"]["inv"].pop("items")
    # sort by items slot index
    for inv in character_json["obj"]["inv"]["holdings"]["in"]:
        if "i" in inv.keys() and type(inv["i"]) == list:
            inv["i"] = sorted(inv["i"], key = lambda i: int(i['attr_s']))


    return render_template(
        'character/view.html.j2',
        character_data=character_data,
        character_json=character_json
    )


@character_blueprint.route('/view_xml/<id>', methods=['GET'])
@login_required
@gm_level(9)
def view_xml(id):

    character_data = CharacterInfo.query.filter(CharacterInfo.id == id).first()

    if character_data == {}:
        abort(404)
        return

    character_xml = CharacterXML.query.filter(
                        CharacterXML.id==id
                    ).first().xml_data

    response = make_response(character_xml)
    response.headers.set('Content-Type', 'text/xml')
    return response

@character_blueprint.route('/get_xml/<id>', methods=['GET'])
@login_required
@gm_level(9)
def get_xml(id):

    character_data = CharacterInfo.query.filter(CharacterInfo.id == id).first()

    if character_data == {}:
        abort(404)
        return

    character_xml = CharacterXML.query.filter(
                        CharacterXML.id==id
                    ).first().xml_data

    response = make_response(character_xml)
    response.headers.set('Content-Type', 'attachment/xml')
    response.headers.set(
        'Content-Disposition',
        'attachment',
        filename=f"{character_data.name}.xml"
    )
    return response

@character_blueprint.route('/restrict/<bit>/<id>', methods=['GET'])
@login_required
@gm_level(3)
def restrict(id, bit):

    # restrict to bit 4-6
    if 6 < int(bit) < 3:
        abort(403)
        return

    character_data = CharacterInfo.query.filter(CharacterInfo.id == id).first()

    if character_data == {}:
        abort(404)
        return

    log_audit(f"Updated ({character_data.id}){character_data.name}'s permission map to \
        {character_data.permission_map ^ (1 << int(bit))} from {character_data.permission_map}")

    character_data.permission_map ^= (1 << int(bit))
    character_data.save()

    return redirect(request.referrer if request.referrer else url_for("main.index"))


@character_blueprint.route('/get/<status>', methods=['GET'])
@login_required
@gm_level(3)
def get(status):
    columns = [
        ColumnDT(CharacterInfo.id),                 # 0
        ColumnDT(Account.username),                 # 1
        ColumnDT(CharacterInfo.name),               # 2
        ColumnDT(CharacterInfo.pending_name),       # 3
        ColumnDT(CharacterInfo.needs_rename),       # 4
        ColumnDT(CharacterInfo.last_login),         # 5
        ColumnDT(CharacterInfo.permission_map),     # 6
    ]

    query = None
    if status=="all":
        query = db.session.query().select_from(CharacterInfo).join(Account)
    elif status=="approved":
        query = db.session.query().select_from(CharacterInfo).join(Account).filter((CharacterInfo.pending_name == "") & (CharacterInfo.needs_rename == False))
    elif status=="unapproved":
        query = db.session.query().select_from(CharacterInfo).join(Account).filter((CharacterInfo.pending_name != "") | (CharacterInfo.needs_rename == True))
    else:
        raise Exception("Not a valid filter")

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    data = rowTable.output_result()
    for character in data["data"]:
        id = character["0"]
        character["0"] = f"""
            <div class="d-none">{id}</div>
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('characters.view', id=id)}'>
                View
            </a>
        """

        if not character["4"]:
            character["0"] += f"""
            <a role="button" class="btn btn-danger btn btn-block"
                href='{url_for('characters.approve_name', id=id, action="rename")}'>
                Needs Rename
            </a>
        """

        if character["3"] or character["4"]:
            character["0"] += f"""
            <a role="button" class="btn btn-success btn btn-block"
                href='{url_for('characters.approve_name', id=id, action="approve")}'>
                Approve Name
            </a>
        """

        character["1"] = f"""
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('accounts.view', id=Account.query.filter(Account.username==character["1"]).first().id)}'>
                View {character["1"]}
            </a>
        """

        if character["4"]:
            character["4"] = '''<h1 class="far fa-check-square text-danger"></h1>'''
        else:
            character["4"] = '''<h1 class="far fa-times-circle text-success"></h1>'''

        character["5"] = time.ctime(character["5"])

        perm_map = character["6"]
        character["6"] = ""

        if perm_map & (1 << 4):
            character["6"] += "Restricted Trade</br>"

        if perm_map & (1 << 5):
            character["6"] += "Restricted Mail</br>"

        if perm_map & (1 << 6):
            character["6"] += "Restricted Chat</br>"


    return data


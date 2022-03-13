from flask import (
    render_template,
    Blueprint,
    redirect,
    url_for,
    request,
    abort,
    make_response,
    flash,
    current_app
)
from flask_user import login_required, current_user
from datatables import ColumnDT, DataTables
import time
from app.models import Property, db, UGC, CharacterInfo, PropertyContent, Account
from app.schemas import PropertySchema
from app import gm_level, log_audit
from app.luclient import query_cdclient

import zlib
import app.pylddlib as ldd
import pathlib

property_blueprint = Blueprint('properties', __name__)

property_schema = PropertySchema()


@property_blueprint.route('/', methods=['GET'])
@login_required
@gm_level(3)
def index():
    return render_template('properties/index.html.j2')


@property_blueprint.route('/approve/<id>', methods=['GET'])
@login_required
@gm_level(3)
def approve(id):

    property_data = Property.query.filter(Property.id == id).first()

    property_data.mod_approved = not property_data.mod_approved

    # If we approved it, clear the rejection reason
    if property_data.mod_approved:
        property_data.rejection_reason = ""

    if property_data.mod_approved:
        message = f"""Approved Property
            {property_data.name if property_data.name else query_cdclient(
                'select DisplayDescription from ZoneTable where zoneID = ?',
                [property_data.zone_id],
                one=True
            )[0]}
            from {CharacterInfo.query.filter(CharacterInfo.id==property_data.owner_id).first().name}"""
        log_audit(message)
        flash(
            message,
            "success"
        )
    else:
        message = f"""Unapproved Property
            {property_data.name if property_data.name else query_cdclient(
                'select DisplayDescription from ZoneTable where zoneID = ?',
                [property_data.zone_id],
                one=True
            )[0]}
            from {CharacterInfo.query.filter(CharacterInfo.id==property_data.owner_id).first().name}"""
        log_audit(message)
        flash(
            message,
            "danger"
        )

    property_data.save()

    go_to = ""

    if request.referrer:
        if "view_models" in request.referrer:
            go_to = url_for('properties.view', id=id)
        else:
            go_to = request.referrer
    else:
        go_to = url_for('main.index')

    return redirect(go_to)


@property_blueprint.route('/view/<id>', methods=['GET'])
@login_required
def view(id):

    property_data = Property.query.filter(Property.id == id).first()

    if current_user.gm_level < 3:
        if property_data.owner_id and property_data.owner.account_id != current_user.id:
            abort(403)
            return

    if property_data == {}:
        abort(404)
        return

    return render_template('properties/view.html.j2', property_data=property_data)


@property_blueprint.route('/get/<status>', methods=['GET'])
@login_required
@gm_level(3)
def get(status="all"):
    columns = [
        ColumnDT(Property.id),                  # 0
        ColumnDT(CharacterInfo.name),           # 1
        ColumnDT(Property.template_id),         # 2
        ColumnDT(Property.clone_id),            # 3
        ColumnDT(Property.name),                # 4
        ColumnDT(Property.description),         # 5
        ColumnDT(Property.privacy_option),      # 6
        ColumnDT(Property.mod_approved),        # 7
        ColumnDT(Property.last_updated),        # 8
        ColumnDT(Property.time_claimed),        # 9
        ColumnDT(Property.rejection_reason),    # 10
        ColumnDT(Property.reputation),          # 11
        ColumnDT(Property.zone_id),             # 12
        ColumnDT(Account.username)              # 13
    ]

    query = None
    if status == "all":
        query = db.session.query().select_from(Property).join(CharacterInfo, CharacterInfo.id == Property.owner_id).join(Account)
    elif status == "approved":
        query = db.session.query().select_from(Property).join(
            CharacterInfo, CharacterInfo.id == Property.owner_id
        ).join(Account).filter(Property.mod_approved is True).filter(Property.privacy_option == 2)
    elif status == "unapproved":
        query = db.session.query().select_from(Property).join(
            CharacterInfo, CharacterInfo.id == Property.owner_id
        ).join(Account).filter(Property.mod_approved is False).filter(Property.privacy_option == 2)
    else:
        raise Exception("Not a valid filter")

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    data = rowTable.output_result()
    for property_data in data["data"]:
        id = property_data["0"]

        property_data["0"] = f"""
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('properties.view', id=id)}'>
                View
            </a>
        """

        if not property_data["7"]:
            property_data["0"] += f"""
                <a role="button" class="btn btn-success btn btn-block"
                    href='{url_for('properties.approve', id=id)}'>
                    Approve
                </a>
            """
        else:
            property_data["0"] += f"""
                <a role="button" class="btn btn-danger btn btn-block"
                    href='{url_for('properties.approve', id=id)}'>
                    Unapprove
                </a>
            """

        property_data["1"] = f"""
            <a role="button" class="btn btn-primary btn btn-block"
                href='{url_for('characters.view', id=CharacterInfo.query.filter(CharacterInfo.name==property_data['1']).first().id)}'>
                {property_data["1"]}
            </a>
        """

        if property_data["4"] == "":
            property_data["4"] = query_cdclient(
                'select DisplayDescription from ZoneTable where zoneID = ?',
                [property_data["12"]],
                one=True
            )

        if property_data["6"] == 0:
            property_data["6"] = "Private"
        elif property_data["6"] == 1:
            property_data["6"] = "Best Friends"
        else:
            property_data["6"] = "Public"

        property_data["8"] = time.ctime(property_data["8"])
        property_data["9"] = time.ctime(property_data["9"])

        if not property_data["7"]:
            property_data["7"] = '''<h2 class="far fa-times-circle text-danger"></h2>'''
        else:
            property_data["7"] = '''<h2 class="far fa-check-square text-success"></h2>'''

        property_data["12"] = query_cdclient(
            'select DisplayDescription from ZoneTable where zoneID = ?',
            [property_data["12"]],
            one=True
        )

    return data


@property_blueprint.route('/view_model/<id>/<lod>', methods=['GET'])
@login_required
def view_model(id, lod):
    property_content_data = PropertyContent.query.filter(PropertyContent.id == id).all()

    # TODO: Restrict somehow
    formatted_data = [
        {
            "obj": url_for('properties.get_model', id=property_content_data[0].id, file_format='obj', lod=lod),
            "mtl": url_for('properties.get_model', id=property_content_data[0].id, file_format='mtl', lod=lod),
            "lot": property_content_data[0].lot,
            "id": property_content_data[0].id,
            "pos": [{
                "x": property_content_data[0].x,
                "y": property_content_data[0].y,
                "z": property_content_data[0].z,
                "rx": property_content_data[0].rx,
                "ry": property_content_data[0].ry,
                "rz": property_content_data[0].rz,
                "rw": property_content_data[0].rw
            }]
        }
    ]

    return render_template(
        'ldd/ldd.html.j2',
        content=formatted_data,
        lod=lod
    )


property_center = {
    1150: "(-17, 432, -60)",
    1151: "(0, 455, -110)",
    1250: "(-16, 432,-60)",
    1251: "(0, 455, 100)",
    1350: "(-10, 432, -57)",
    1450: "(-10, 432, -77)"
}


@property_blueprint.route('/view_models/<id>/<lod>', methods=['GET'])
@login_required
def view_models(id, lod):
    property_content_data = PropertyContent.query.filter(
        PropertyContent.property_id == id
    ).order_by(PropertyContent.lot).all()

    consolidated_list = []

    for item in range(len(property_content_data)):
        if any((d["lot"] != 14 and d["lot"] == property_content_data[item].lot) for d in consolidated_list):
            # exiting lot, add rotations
            lot_index = next((index for (index, d) in enumerate(consolidated_list) if d["lot"] == property_content_data[item].lot), None)
            consolidated_list[lot_index]["pos"].append(
                {
                    "x": property_content_data[item].x,
                    "y": property_content_data[item].y,
                    "z": property_content_data[item].z,
                    "rx": property_content_data[item].rx,
                    "ry": property_content_data[item].ry,
                    "rz": property_content_data[item].rz,
                    "rw": property_content_data[item].rw
                }
            )
        else:
            # add new lot
            consolidated_list.append(
                {
                    "obj": url_for('properties.get_model', id=property_content_data[item].id, file_format='obj', lod=lod),
                    "mtl": url_for('properties.get_model', id=property_content_data[item].id, file_format='mtl', lod=lod),
                    "lot": property_content_data[item].lot,
                    "id": property_content_data[item].id,
                    "pos": [{
                        "x": property_content_data[item].x,
                        "y": property_content_data[item].y,
                        "z": property_content_data[item].z,
                        "rx": property_content_data[item].rx,
                        "ry": property_content_data[item].ry,
                        "rz": property_content_data[item].rz,
                        "rw": property_content_data[item].rw
                    }]
                }
            )
    property_data = Property.query.filter(Property.id == id).first()
    return render_template(
        'ldd/ldd.html.j2',
        property_data=property_data,
        content=consolidated_list,
        center=property_center[property_data.zone_id],
        lod=lod
    )


@property_blueprint.route('/get_model/<id>/<file_format>/<lod>', methods=['GET'])
@login_required
def get_model(id, file_format, lod):
    content = PropertyContent.query.filter(PropertyContent.id == id).first()
    if not(0 <= int(lod) <= 2):
        abort(404)
    if content.lot == 14:  # ugc model
        response = ugc(content)[0]
    else:  # prebuilt model
        response = prebuilt(content, file_format, lod)[0]

    response.headers.set('Content-Type', 'text/xml')
    return response


@property_blueprint.route('/download_model/<id>', methods=['GET'])
@login_required
def download_model(id):
    content = PropertyContent.query.filter(PropertyContent.id == id).first()

    if content.lot == 14:  # ugc model
        response, filename = ugc(content)
    else:  # prebuilt model
        response, filename = prebuilt(content, "lxfml")

    response.headers.set('Content-Type', 'attachment/xml')
    response.headers.set(
        'Content-Disposition',
        'attachment',
        filename=filename
    )
    return response


def ugc(content):
    ugc_data = UGC.query.filter(UGC.id == content.ugc_id).first()
    uncompressed_lxfml = zlib.decompress(ugc_data.lxfml)
    response = make_response(uncompressed_lxfml)
    return response, ugc_data.filename


def prebuilt(content, file_format, lod):
    # translate LOT to component id
    # we need to get a type of 2 because reasons
    render_component_id = query_cdclient(
        'select component_id from ComponentsRegistry where component_type = 2 and id = ?',
        [content.lot],
        one=True
    )[0]
    # find the asset from rendercomponent given the  component id
    filename = query_cdclient(
        'select render_asset from RenderComponent where id = ?',
        [render_component_id],
        one=True
    )
    if filename:
        filename = filename[0].split("\\\\")[-1].lower().split(".")[0]
    else:
        return f"No filename for LOT {content.lot}"

    lxfml = pathlib.Path(f'app/luclient/res/BrickModels/{filename.split(".")[0]}.lxfml')
    if file_format == "lxfml":

        with open(lxfml, 'r') as file:
            lxfml_data = file.read()
        response = make_response(lxfml_data)

    elif file_format in ["obj", "mtl"]:
        cache = pathlib.Path(f'app/cache/BrickModels/{filename}.lod{lod}.{file_format}')
        cache.parent.mkdir(parents=True, exist_ok=True)
        try:
            ldd.main(str(lxfml.as_posix()), str(cache.with_suffix("").as_posix()), lod)  # convert to OBJ
        except Exception as e:
            current_app.logger.error(f"ERROR on {cache}:\n {e}")

        with open(str(cache.as_posix()), 'r') as file:
            cache_data = file.read()

        response = make_response(cache_data)

    else:
        raise(Exception("INVALID FILE FORMAT"))

    return response, f"{filename}.{file_format}"

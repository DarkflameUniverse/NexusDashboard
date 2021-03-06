from flask import render_template, Blueprint, redirect, url_for, request, flash, current_app
from flask_user import login_required
from app.models import PetNames, db, CharacterXML, CharacterInfo
from datatables import ColumnDT, DataTables
from app import gm_level, log_audit, scheduler

moderation_blueprint = Blueprint('moderation', __name__)


@moderation_blueprint.route('/<status>', methods=['GET'])
@login_required
@gm_level(3)
def index(status):
    return render_template('moderation/index.html.j2', status=status)


@moderation_blueprint.route('/approve_pet/<id>', methods=['GET'])
@login_required
@gm_level(3)
def approve_pet(id):

    pet_data = PetNames.query.filter(PetNames.id == id).first()

    pet_data.approved = 2
    log_audit(f"Approved pet name {pet_data.pet_name} from {pet_data.owner_id}")
    flash(f"Approved pet name {pet_data.pet_name} from {pet_data.owner_id}", "success")
    pet_data.save()
    return redirect(request.referrer if request.referrer else url_for("main.index"))


@moderation_blueprint.route('/reject_pet/<id>', methods=['GET'])
@login_required
@gm_level(3)
def reject_pet(id):

    pet_data = PetNames.query.filter(PetNames.id == id).first()

    pet_data.approved = 0
    log_audit(f"Rejected pet name {pet_data.pet_name} from {pet_data.owner_id}")
    flash(f"Rejected pet name {pet_data.pet_name} from {pet_data.owner_id}", "danger")
    pet_data.save()
    return redirect(request.referrer if request.referrer else url_for("main.index"))


@moderation_blueprint.route('/get_pets/<status>', methods=['GET'])
@login_required
@gm_level(3)
def get_pets(status="all"):
    columns = [
        ColumnDT(PetNames.id),
        ColumnDT(PetNames.pet_name),
        ColumnDT(PetNames.approved),
        ColumnDT(PetNames.owner_id),
    ]

    query = None
    if status == "approved":
        query = db.session.query().select_from(PetNames).filter(PetNames.approved == 2)
    elif status == "unapproved":
        query = db.session.query().select_from(PetNames).filter(PetNames.approved == 1)
    else:
        query = db.session.query().select_from(PetNames)

    params = request.args.to_dict()

    rowTable = DataTables(params, query, columns)

    data = rowTable.output_result()
    for pet_data in data["data"]:
        id = pet_data["0"]
        status = pet_data["2"]
        if status == 1:
            pet_data["0"] = f"""
            <div class="row">
                <div class="col">
                    <a role="button" class="btn btn-success btn btn-block"
                        href='{url_for('moderation.approve_pet', id=id)}'>
                        Approve
                    </a>
                </div>
                <div class="col">
                    <a role="button" class="btn btn-danger btn btn-block"
                        href='{url_for('moderation.reject_pet', id=id)}'>
                        Reject
                    </a>
                </div>
            </div>
            """
            pet_data["2"] = "Awaiting Moderation"
        elif status == 2:
            pet_data["0"] = f"""
                <a role="button" class="btn btn-danger btn btn-block"
                    href='{url_for('moderation.reject_pet', id=id)}'>
                    Reject
                </a>
            """
            pet_data["2"] = "<span class='text-success'>Approved</span>"
        elif status == 0:
            pet_data["0"] = f"""
                <a role="button" class="btn btn-success btn btn-block"
                    href='{url_for('moderation.approve_pet', id=id)}'>
                    Approve
                </a>
            """
            pet_data["2"] = "<span class='text-danger'>Rejected</span>"

        if pet_data["3"]:
            try:
                pet_data["3"] = f"""
                    <a role="button" class="btn btn-primary btn btn-block"
                        href='{url_for('characters.view', id=pet_data["3"])}'>
                        {CharacterInfo.query.filter(CharacterInfo.id==pet_data['3']).first().name}
                    </a>
                """
            except Exception:
                PetNames.query.filter(PetNames.id == id).first().delete()
                pet_data["0"] = "<span class='text-danger'>Deleted Refresh to make go away</span>"
                pet_data["3"] = "<span class='text-danger'>Character Deleted</span>"
        else:
            pet_data["3"] = "Pending Character Association"

    return data


@scheduler.task("cron", id="pet_name_maintenance", hour="*", timezone="UTC")
def pet_name_maintenance():
    with scheduler.app.app_context():
        # associate pet names to characters
        # current_app.logger.info("Started Pet Name Maintenance")
        unassociated_pets = PetNames.query.filter(PetNames.owner_id == None).all()
        if unassociated_pets:
            current_app.logger.info("Found un-associated pets")
            for pet in unassociated_pets:
                owner = CharacterXML.query.filter(CharacterXML.xml_data.like(f"%<p id=\"{pet.id}\" l=\"%")).first()
                if owner:
                    pet.owner_id = owner.id
                    pet.save()
                else:
                    pet.delete()

        # auto-moderate based on already moderated names
        unmoderated_pets = PetNames.query.filter(PetNames.approved == 1).all()
        if unmoderated_pets:
            current_app.logger.info("Found un-moderated Pets")
            for pet in unmoderated_pets:
                existing_pet = PetNames.query.filter(PetNames.approved.in_([0, 2])).filter(PetNames.pet_name == pet.pet_name).first()
                if existing_pet:
                    pet.approved = existing_pet.approved
                    pet.save()
        # current_app.logger.info("Finished Pet Name Maintenance")

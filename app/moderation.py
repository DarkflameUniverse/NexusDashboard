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
    # Import here to avoid circular imports at module load
    from app.moderation import get_auto_approval_enabled, get_auto_approval_interval
    return render_template(
        'moderation/index.html.j2',
        status=status,
        auto_approval_enabled=get_auto_approval_enabled(),
        auto_approval_interval=get_auto_approval_interval()
    )


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
            # Awaiting moderation
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
            pet_data["2"] = "<span class='text-muted'>Awaiting Moderation </span><h4 class='far fa-times-circle text-muted'></h4>"
        elif status == 2:
            # Approved
            pet_data["0"] = f"""
                <a role="button" class="btn btn-danger btn btn-block"
                    href='{url_for('moderation.reject_pet', id=id)}'>
                    Reject
                </a>
            """
            pet_data["2"] = "<span class='text-success'>Approved </span><h4 class='far fa-check-square text-success'></h4>"
        elif status == 0:
            # Rejected
            pet_data["0"] = f"""
                <a role="button" class="btn btn-success btn btn-block"
                    href='{url_for('moderation.approve_pet', id=id)}'>
                    Approve
                </a>
            """
            pet_data["2"] = "<span class='text-danger'>Rejected </span><h4 class='far fa-times-circle text-danger'></h4>"

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


@moderation_blueprint.route('/approve_all_characters', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def approve_all_characters():
    """Approve all pending character names."""
    # Find characters with pending names or that need rename
    pending_chars = CharacterInfo.query.filter(
        (CharacterInfo.pending_name != "") | (CharacterInfo.needs_rename == True)
    ).all()

    count = 0
    for char in pending_chars:
        if char.pending_name:
            char.name = char.pending_name
            char.pending_name = ""
        char.needs_rename = False
        char.save()
        count += 1

    log_audit(f"Bulk approved {count} character names")
    flash(f"Approved {count} character names", "success")
    return redirect(request.referrer if request.referrer else url_for("moderation.index", status="all"))


@moderation_blueprint.route('/approve_all_pets', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def approve_all_pets():
    """Approve all pending pet names."""
    pending_pets = PetNames.query.filter(PetNames.approved == 1).all()

    count = 0
    for pet in pending_pets:
        pet.approved = 2
        pet.save()
        count += 1

    log_audit(f"Bulk approved {count} pet names")
    flash(f"Approved {count} pet names", "success")
    return redirect(request.referrer if request.referrer else url_for("moderation.index", status="all"))


@moderation_blueprint.route('/approve_all_properties', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def approve_all_properties():
    """Approve all pending properties."""
    from app.models import Property

    pending_props = Property.query.filter(
        Property.mod_approved == False,
        Property.privacy_option == 2,
        Property.rejection_reason == ""
    ).all()

    count = 0
    for prop in pending_props:
        prop.mod_approved = True
        prop.rejection_reason = ""
        prop.save()
        count += 1

    log_audit(f"Bulk approved {count} properties")
    flash(f"Approved {count} properties", "success")
    return redirect(request.referrer if request.referrer else url_for("moderation.index", status="all"))


@moderation_blueprint.route('/approve_all', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def approve_all():
    """Approve all pending items (characters, pets, and properties)."""
    from app.models import Property

    # Characters
    char_count = 0
    pending_chars = CharacterInfo.query.filter(
        (CharacterInfo.pending_name != "") | (CharacterInfo.needs_rename == True)
    ).all()
    for char in pending_chars:
        if char.pending_name:
            char.name = char.pending_name
            char.pending_name = ""
        char.needs_rename = False
        char.save()
        char_count += 1

    # Pets
    pet_count = 0
    pending_pets = PetNames.query.filter(PetNames.approved == 1).all()
    for pet in pending_pets:
        pet.approved = 2
        pet.save()
        pet_count += 1

    # Properties
    prop_count = 0
    pending_props = Property.query.filter(
        Property.mod_approved == False,
        Property.privacy_option == 2,
        Property.rejection_reason == ""
    ).all()
    for prop in pending_props:
        prop.mod_approved = True
        prop.rejection_reason = ""
        prop.save()
        prop_count += 1

    total = char_count + pet_count + prop_count
    log_audit(f"Bulk approved all: {char_count} characters, {pet_count} pets, {prop_count} properties")
    flash(f"Approved {total} items ({char_count} characters, {pet_count} pets, {prop_count} properties)", "success")
    return redirect(request.referrer if request.referrer else url_for("moderation.index", status="all"))


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


# Auto-approval settings constants
AUTO_APPROVAL_ENABLED_KEY = 'auto_approval_enabled'
AUTO_APPROVAL_INTERVAL_KEY = 'auto_approval_interval'
DEFAULT_AUTO_APPROVAL_INTERVAL = 15  # minutes


def get_auto_approval_enabled():
    """Check if auto-approval is enabled."""
    from app.models import DashboardSettings
    value = DashboardSettings.get(AUTO_APPROVAL_ENABLED_KEY, 'false')
    return value.lower() == 'true'


def get_auto_approval_interval():
    """Get auto-approval interval in minutes."""
    from app.models import DashboardSettings
    value = DashboardSettings.get(AUTO_APPROVAL_INTERVAL_KEY, str(DEFAULT_AUTO_APPROVAL_INTERVAL))
    try:
        return int(value)
    except ValueError:
        return DEFAULT_AUTO_APPROVAL_INTERVAL


@moderation_blueprint.route('/toggle_auto_approval', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def toggle_auto_approval():
    """Toggle the auto-approval setting."""
    from app.models import DashboardSettings

    current_state = get_auto_approval_enabled()
    new_state = not current_state
    DashboardSettings.set(AUTO_APPROVAL_ENABLED_KEY, str(new_state).lower())

    log_audit(f"Auto-approval {'enabled' if new_state else 'disabled'}")
    flash(f"Auto-approval {'enabled' if new_state else 'disabled'}", "success" if new_state else "warning")
    return redirect(request.referrer if request.referrer else url_for("moderation.index", status="all"))


@moderation_blueprint.route('/set_auto_approval_interval', methods=['POST'])
@login_required
@gm_level(3)
def set_auto_approval_interval():
    """Set the auto-approval interval in minutes."""
    from app.models import DashboardSettings

    try:
        interval = int(request.form.get('interval', DEFAULT_AUTO_APPROVAL_INTERVAL))
        interval = max(1, min(1440, interval))  # Clamp between 1 minute and 24 hours
    except (ValueError, TypeError):
        interval = DEFAULT_AUTO_APPROVAL_INTERVAL

    DashboardSettings.set(AUTO_APPROVAL_INTERVAL_KEY, str(interval))
    log_audit(f"Set auto-approval interval to {interval} minutes")
    flash(f"Auto-approval interval set to {interval} minutes", "success")
    return redirect(request.referrer if request.referrer else url_for("moderation.index", status="all"))


@scheduler.task("interval", id="auto_approval_task", minutes=15, timezone="UTC")
def auto_approval_task():
    """Scheduled task to auto-approve all pending items if enabled."""
    with scheduler.app.app_context():
        if not get_auto_approval_enabled():
            return

        from app.models import Property

        current_app.logger.info("Running auto-approval task")

        # Characters
        char_count = 0
        pending_chars = CharacterInfo.query.filter(
            (CharacterInfo.pending_name != "") | (CharacterInfo.needs_rename == True)
        ).all()
        for char in pending_chars:
            if char.pending_name:
                char.name = char.pending_name
                char.pending_name = ""
            char.needs_rename = False
            char.save()
            char_count += 1

        # Pets
        pet_count = 0
        pending_pets = PetNames.query.filter(PetNames.approved == 1).all()
        for pet in pending_pets:
            pet.approved = 2
            pet.save()
            pet_count += 1

        # Properties
        prop_count = 0
        pending_props = Property.query.filter(
            Property.mod_approved == False,
            Property.privacy_option == 2,
            Property.rejection_reason == ""
        ).all()
        for prop in pending_props:
            prop.mod_approved = True
            prop.rejection_reason = ""
            prop.save()
            prop_count += 1

        if char_count or pet_count or prop_count:
            current_app.logger.info(
                f"Auto-approved: {char_count} characters, {pet_count} pets, {prop_count} properties"
            )

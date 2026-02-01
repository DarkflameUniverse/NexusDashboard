from flask import render_template, Blueprint, send_from_directory
from flask_user import current_user, login_required

from app.models import Account, CharacterInfo, ActivityLog, PetNames, Property

import datetime
import time

main_blueprint = Blueprint('main', __name__)


def get_pending_items():
    """Get pending items for admin dashboard."""
    pending_items = []

    # Pending character names
    pending_chars = CharacterInfo.query.filter(
        (CharacterInfo.pending_name != "") | (CharacterInfo.needs_rename == True)
    ).limit(10).all()
    for char in pending_chars:
        pending_items.append({
            'type': 'Character',
            'name': char.pending_name if char.pending_name else char.name,
            'id': char.id
        })

    # Pending pet names
    pending_pets = PetNames.query.filter(PetNames.approved == 1).limit(10).all()
    for pet in pending_pets:
        pending_items.append({
            'type': 'Pet',
            'name': pet.pet_name,
            'id': pet.id
        })

    # Pending properties
    pending_props = Property.query.filter(
        Property.mod_approved == False,
        Property.privacy_option == 2,
        Property.rejection_reason == ""
    ).limit(10).all()
    for prop in pending_props:
        pending_items.append({
            'type': 'Property',
            'name': prop.name if prop.name else f"Property #{prop.id}",
            'id': prop.id
        })

    return pending_items[:25]  # Limit total to 25


def get_pending_counts():
    """Get counts of pending items for admin dashboard."""
    char_count = CharacterInfo.query.filter(
        (CharacterInfo.pending_name != "") | (CharacterInfo.needs_rename == True)
    ).count()

    pet_count = PetNames.query.filter(PetNames.approved == 1).count()

    prop_count = Property.query.filter(
        Property.mod_approved == False,
        Property.privacy_option == 2,
        Property.rejection_reason == ""
    ).count()

    return {
        'characters': char_count,
        'pets': pet_count,
        'properties': prop_count,
        'total': char_count + pet_count + prop_count
    }


@main_blueprint.route('/', methods=['GET'])
def index():
    """Home/Index Page"""
    if current_user.is_authenticated:
        account_data = Account.query.filter(Account.id == current_user.id).first()

        # For admin users, also get pending items
        pending_items = None
        pending_counts = None
        if current_user.gm_level >= 3:
            pending_items = get_pending_items()
            pending_counts = get_pending_counts()

        return render_template(
            'main/index.html.j2',
            account_data=account_data,
            pending_items=pending_items,
            pending_counts=pending_counts
        )
    else:
        return render_template('main/index.html.j2')


@main_blueprint.route('/about')
@login_required
def about():
    """About Page"""
    mods = Account.query.filter(Account.gm_level > 1).order_by(Account.gm_level.desc()).all()
    online = 0
    users = []
    zones = {}
    twodaysago = time.mktime((datetime.datetime.now() - datetime.timedelta(days=2)).timetuple())
    chars = CharacterInfo.query.filter(CharacterInfo.last_login >= twodaysago).all()

    for char in chars:
        last_log = ActivityLog.query.with_entities(
            ActivityLog.activity, ActivityLog.map_id
        ).filter(
            ActivityLog.character_id == char.id
        ).order_by(ActivityLog.id.desc()).first()

        if last_log:
            if last_log[0] == 0:
                online += 1
                if current_user.gm_level >= 8: users.append([char.name, last_log[1]])
                if str(last_log[1]) not in zones:
                    zones[str(last_log[1])] = 1
                else:
                    zones[str(last_log[1])] += 1

    return render_template('main/about.html.j2', mods=mods, online=online, users=users, zones=zones)


@main_blueprint.route('/favicon.ico')
def favicon():
    return send_from_directory(
        'static/logo/',
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

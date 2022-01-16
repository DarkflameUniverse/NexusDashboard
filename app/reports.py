from flask import render_template, Blueprint, redirect, url_for, request, abort, flash, request
from flask_user import login_required, current_user
from app.models import db, CharacterInfo, Account, CharacterXML, ItemReports
from app import gm_level, scheduler
import datetime, xmltodict

reports_blueprint = Blueprint('reports', __name__)

@reports_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def index():
    items = ItemReports.query.distinct(ItemReports.date).group_by(ItemReports.date).all()

    return render_template('reports/index.html.j2', items=items)

@reports_blueprint.route('/items/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def items_by_date(date):
    items = ItemReports.query.filter(ItemReports.date==date).order_by(ItemReports.count.desc()).all()
    return render_template('reports/items/by_date.html.j2', items=items, date=date)


@scheduler.task("cron", id="gen_item_report", hour=3)
def gen_item_report():
    char_xmls = CharacterXML.query.join(
                    CharacterInfo,
                    CharacterInfo.id==CharacterXML.id
                ).join(
                    Account,
                    CharacterInfo.account_id==Account.id
                ).filter(Account.gm_level < 3).all()
    date = datetime.date.today().strftime('%Y-%m-%d')
    for char_xml in char_xmls:
        character_json = xmltodict.parse(
            char_xml.xml_data,
            attr_prefix="attr_"
        )
        for inv in character_json["obj"]["inv"]["items"]["in"]:
            if "i" in inv.keys() and type(inv["i"]) == list and (int(inv["attr_t"])==0 or int(inv["attr_t"])==0):
                for item in inv["i"]:
                    entry = ItemReports.query.filter(
                                ItemReports.item == int(item["attr_l"]) and \
                                ItemReports.date == date
                            ).first()
                    if entry:
                        entry.count = entry.count + int(item["attr_c"])
                        entry.save()
                    else:
                        new_entry = ItemReports(
                            item=int(item["attr_l"]),
                            count=int(item["attr_c"]),
                            date=date
                        )
                        new_entry.save()

    return "Done"

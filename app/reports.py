from flask import render_template, Blueprint, current_app
from flask_user import login_required
from app.models import CharacterInfo, Account, CharacterXML, Reports
from app.luclient import get_lot_name
from app import gm_level, scheduler
from sqlalchemy.orm import load_only
import datetime
import xmltodict
import random

reports_blueprint = Blueprint('reports', __name__)


@reports_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def index():
    reports_items = Reports.query.distinct(
        Reports.date
    ).filter(
        Reports.report_type == "items"
    ).group_by(Reports.date).options(load_only(Reports.date)).all()

    reports_currency = Reports.query.distinct(
        Reports.date
    ).filter(
        Reports.report_type == "currency"
    ).group_by(Reports.date).options(load_only(Reports.date)).all()

    reports_uscore = Reports.query.distinct(
        Reports.date
    ).filter(
        Reports.report_type == "uscore"
    ).group_by(Reports.date).options(load_only(Reports.date)).all()

    return render_template(
        'reports/index.html.j2',
        reports_items=reports_items,
        reports_currency=reports_currency,
        reports_uscore=reports_uscore,
    )


@reports_blueprint.route('/items/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def items_by_date(date):
    data = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "items").first().data
    return render_template('reports/items/by_date.html.j2', data=data, date=date)


@reports_blueprint.route('/items/graph', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def items_graph():
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
    entries = Reports.query.filter(
        Reports.report_type == "items"
    ).filter(Reports.date >= thirty_days_ago).all()
    # transform data for chartjs
    labels = []
    items = dict()
    datasets = []
    # get stuff ready
    for entry in entries:
        labels.append(entry.date.strftime("%m/%d/%Y"))
        for key in entry.data:
            items[key] = get_lot_name(key)
    # make it
    for key, value in items.items():
        data = []
        for entry in entries:
            if key in entry.data.keys():
                data.append(entry.data[key])
            else:
                data.append(0)
        color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        datasets.append({
            "label": value,
            "data": data,
            "backgroundColor": color,
            "borderColor": color
        })

    return render_template(
        'reports/graph.html.j2',
        labels=labels,
        datasets=datasets,
        name="Item"
    )

@reports_blueprint.route('/currency/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def currency_by_date(date):
    data = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "currency").first().data
    return render_template('reports/currency/by_date.html.j2', data=data, date=date)


@reports_blueprint.route('/currency/graph', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def currency_graph():
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
    entries = Reports.query.filter(
        Reports.report_type == "currency"
    ).filter(Reports.date >= thirty_days_ago).all()
    characters = CharacterInfo.query.options(load_only(CharacterInfo.name)).all()
    labels = []
    datasets = []
    # get stuff ready
    for entry in entries:
        labels.append(entry.date.strftime("%m/%d/%Y"))
    for character in characters:
        data = []
        for entry in entries:
            if character.name in entry.data.keys():
                data.append(entry.data[character.name])
            else:
                data.append(0)
        color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        datasets.append({
            "label": character.name,
            "data": data,
            "backgroundColor": color,
            "borderColor": color
        })
    return render_template(
        'reports/graph.html.j2',
        labels=labels,
        datasets=datasets,
        name="Currency"
    )


@reports_blueprint.route('/uscore/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def uscore_by_date(date):
    data = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "uscore").first().data
    return render_template('reports/uscore/by_date.html.j2', data=data, date=date)


@reports_blueprint.route('/uscore/graph', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def uscore_graph():
    thirty_days_ago = datetime.date.today() - datetime.timedelta(days=30)
    entries = Reports.query.filter(
        Reports.report_type == "uscore"
    ).filter(Reports.date >= thirty_days_ago).all()
    characters = CharacterInfo.query.options(load_only(CharacterInfo.name)).all()
    labels = []
    datasets = []
    # get stuff ready
    for entry in entries:
        labels.append(entry.date.strftime("%m/%d/%Y"))
    for character in characters:
        data = []
        for entry in entries:
            if character.name in entry.data.keys():
                data.append(entry.data[character.name])
            else:
                data.append(0)
        color = "#" + ''.join([random.choice('ABCDEF0123456789') for i in range(6)])
        datasets.append({
            "label": character.name,
            "data": data,
            "backgroundColor": color,
            "borderColor": color
        })
    return render_template(
        'reports/graph.html.j2',
        labels=labels,
        datasets=datasets,
        name="U-Score"
    )


@scheduler.task("cron", id="gen_item_report", hour=23, timezone="UTC")
def gen_item_report():
    with scheduler.app.app_context():
        try:
            current_app.logger.info("Start Item Report Generation")

            date = datetime.date.today().strftime('%Y-%m-%d')
            report = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "items").first()

            # Only one report per day
            if report is not None:
                current_app.logger.info(f"Item Report Already Generated for {date}")
                return

            char_xmls = CharacterXML.query.join(
                CharacterInfo,
                CharacterInfo.id == CharacterXML.id
            ).join(
                Account,
                CharacterInfo.account_id == Account.id
            ).filter(Account.gm_level < 3).all()

            report_data = {}

            for char_xml in char_xmls:
                try:
                    character_json = xmltodict.parse(
                        char_xml.xml_data,
                        attr_prefix="attr_"
                    )
                    for inv in character_json["obj"]["inv"]["items"]["in"]:
                        if "i" in inv.keys() and type(inv["i"]) == list and (int(inv["attr_t"]) == 0 or int(inv["attr_t"]) == 1):
                            for item in inv["i"]:
                                if item["attr_l"] in report_data:
                                    report_data[item["attr_l"]] = report_data[item["attr_l"]] + int(item["attr_c"])
                                else:
                                    report_data[item["attr_l"]] = int(item["attr_c"])
                except Exception as e:
                    current_app.logger.error(f"REPORT::ITEMS - ERROR PARSING CHARACTER {char_xml.id}")
                    current_app.logger.error(f"REPORT::ITEMS - {e}")

            new_report = Reports(
                data=report_data,
                report_type="items",
                date=date
            )

            new_report.save()
            current_app.logger.info(f"Generated Item Report for {date}")
        except Exception as e:
            current_app.logger.critical(f"REPORT::ITEMS - {e}")
        return


@scheduler.task("cron", id="gen_currency_report", hour=23, timezone="UTC")
def gen_currency_report():
    with scheduler.app.app_context():
        try:
            current_app.logger.info("Start Currency Report Generation")

            date = datetime.date.today().strftime('%Y-%m-%d')
            report = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "currency").first()

            # Only one report per day
            if report is not None:
                current_app.logger.info(f"Currency Report Already Generated for {date}")
                return

            characters = CharacterXML.query.join(
                CharacterInfo,
                CharacterInfo.id == CharacterXML.id
            ).join(
                Account,
                CharacterInfo.account_id == Account.id
            ).filter(Account.gm_level < 3).all()

            report_data = {}

            for character in characters:
                try:
                    character_json = xmltodict.parse(
                        character.xml_data,
                        attr_prefix="attr_"
                    )
                    report_data[CharacterInfo.query.filter(CharacterInfo.id == character.id).first().name] = int(character_json["obj"]["char"]["attr_cc"])
                except Exception as e:
                    current_app.logger.error(f"REPORT::CURRENCY - ERROR PARSING CHARACTER {character.id}")
                    current_app.logger.error(f"REPORT::CURRENCY - {e}")

            new_report = Reports(
                data=report_data,
                report_type="currency",
                date=date
            )

            new_report.save()
            current_app.logger.info(f"Generated Currency Report for {date}")
        except Exception as e:
            current_app.logger.critical(f"REPORT::CURRENCY - {e}")
        return


@scheduler.task("cron", id="gen_uscore_report", hour=23, timezone="UTC")
def gen_uscore_report():
    with scheduler.app.app_context():
        try:
            current_app.logger.info("Start U-Score Report Generation")

            date = datetime.date.today().strftime('%Y-%m-%d')
            report = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "uscore").first()

            # Only one report per day
            if report is not None:
                current_app.logger.info(f"U-Score Report Already Generated for {date}")
                return

            characters = CharacterXML.query.join(
                CharacterInfo,
                CharacterInfo.id == CharacterXML.id
            ).join(
                Account,
                CharacterInfo.account_id == Account.id
            ).filter(Account.gm_level < 3).all()

            report_data = {}

            for character in characters:
                try:
                    character_json = xmltodict.parse(
                        character.xml_data,
                        attr_prefix="attr_"
                    )
                    report_data[CharacterInfo.query.filter(CharacterInfo.id == character.id).first().name] = int(character_json["obj"]["char"]["attr_ls"])
                except Exception as e:
                    current_app.logger.error(f"REPORT::U-SCORE - ERROR PARSING CHARACTER {character.id}")
                    current_app.logger.error(f"REPORT::U-SCORE - {e}")

            new_report = Reports(
                data=report_data,
                report_type="uscore",
                date=date
            )

            new_report.save()
            current_app.logger.info(f"Generated U-Score Report for {date}")
        except Exception as e:
            current_app.logger.critical(f"REPORT::U-SCORE - {e}")
        return

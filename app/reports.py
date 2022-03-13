from flask import render_template, Blueprint, current_app
from flask_user import login_required
from app.models import CharacterInfo, Account, CharacterXML, Reports
from app import gm_level, scheduler
import datetime
import xmltodict

reports_blueprint = Blueprint('reports', __name__)


@reports_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def index():
    reports = Reports.query.distinct(Reports.date).group_by(Reports.date).all()
    return render_template('reports/index.html.j2', reports=reports)


@reports_blueprint.route('/items/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def items_by_date(date):
    data = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "items").first().data
    return render_template('reports/items/by_date.html.j2', data=data, date=date)


@reports_blueprint.route('/currency/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def currency_by_date(date):
    data = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "currency").first().data
    return render_template('reports/currency/by_date.html.j2', data=data, date=date)


@reports_blueprint.route('/uscore/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def uscore_by_date(date):
    data = Reports.query.filter(Reports.date == date).filter(Reports.report_type == "uscore").first().data
    return render_template('reports/uscore/by_date.html.j2', data=data, date=date)


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
                    current_app.logger.error(f"REPORT::CURRENCY - ERROR PARSING CHARACTER {char_xml.id}")
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
                    current_app.logger.error(f"REPORT::U-SCORE - ERROR PARSING CHARACTER {char_xml.id}")
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

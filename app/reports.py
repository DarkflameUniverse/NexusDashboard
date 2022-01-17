from flask import render_template, Blueprint, redirect, url_for, request, abort, flash, request
from flask_user import login_required, current_user
from app.models import db, CharacterInfo, Account, CharacterXML, Reports
from app import gm_level, scheduler
import datetime, xmltodict, json

reports_blueprint = Blueprint('reports', __name__)

@reports_blueprint.route('/', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def index():
    reports = Reports.query.distinct(Reports.date).group_by(Reports.date).all()
    print(gen_item_report())
    print(gen_currency_report())
    return render_template('reports/index.html.j2', reports=reports)

@reports_blueprint.route('/items/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def items_by_date(date):
    data = Reports.query.filter(Reports.date==date).filter(Reports.report_type=="items").first().data
    return render_template('reports/items/by_date.html.j2', data=data, date=date)

@reports_blueprint.route('/currency/by_date/<date>', methods=['GET', 'POST'])
@login_required
@gm_level(3)
def currency_by_date(date):
    data = Reports.query.filter(Reports.date==date).filter(Reports.report_type=="currency").first().data
    return render_template('reports/currency/by_date.html.j2', data=data, date=date)


@scheduler.task("cron", id="gen_item_report", hour=23)
def gen_item_report():
    with scheduler.app.app_context():
        date = datetime.date.today().strftime('%Y-%m-%d')
        report = Reports.query.filter(Reports.date==date).filter(Reports.report_type=="items").first()

        # Only one report per day
        if report != None:
            return f"Item Report Already Generated for {date}"

        char_xmls = CharacterXML.query.join(
                        CharacterInfo,
                        CharacterInfo.id==CharacterXML.id
                    ).join(
                        Account,
                        CharacterInfo.account_id==Account.id
                    ).filter(Account.gm_level < 3).all()

        report_data={}

        for char_xml in char_xmls:
            character_json = xmltodict.parse(
                char_xml.xml_data,
                attr_prefix="attr_"
            )
            for inv in character_json["obj"]["inv"]["items"]["in"]:
                if "i" in inv.keys() and type(inv["i"]) == list and (int(inv["attr_t"])==0 or int(inv["attr_t"])==0):
                    for item in inv["i"]:
                        if item["attr_l"] in report_data:
                            report_data[item["attr_l"]] = report_data[item["attr_l"]] + int(item["attr_c"])
                        else:
                            report_data[item["attr_l"]] = int(item["attr_c"])

        new_report = Reports(
            data=report_data,
            report_type="items",
            date=date
        )

        new_report.save()

        return f"Generated Item Report for {date}"


@scheduler.task("cron", id="gen_currency_report", hour=23)
def gen_currency_report():
    with scheduler.app.app_context():
        date = datetime.date.today().strftime('%Y-%m-%d')
        report = Reports.query.filter(Reports.date==date).filter(Reports.report_type=="currency").first()

        # Only one report per day
        if report != None:
            return f"Currency Report Already Generated for {date}"

        characters = CharacterXML.query.join(
                        CharacterInfo,
                        CharacterInfo.id==CharacterXML.id
                    ).join(
                        Account,
                        CharacterInfo.account_id==Account.id
                    ).filter(Account.gm_level < 3).all()

        report_data={}

        for character in characters:
            character_json = xmltodict.parse(
                character.xml_data,
                attr_prefix="attr_"
            )
            report_data[CharacterInfo.query.filter(CharacterInfo.id==character.id).first().name] = int(character_json["obj"]["char"]["attr_cc"])

        new_report = Reports(
            data=report_data,
            report_type="currency",
            date=date
        )

        new_report.save()

        return f"Generated Currency Report for {date}"

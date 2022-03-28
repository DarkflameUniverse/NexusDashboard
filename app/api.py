from flask import Blueprint, current_app, request

api_blueprint = Blueprint('api', __name__)


@api_blueprint.route('/web', methods=['GET', 'POST'])
def web():
    current_app.logger.info(f"API::WEB [DATA] {request.data}")
    return


@api_blueprint.route('/game', methods=['GET', 'POST'])
def game():
    current_app.logger.info(f"API::GAME [DATA] {request.data}")
    return


@api_blueprint.route('/game_content', methods=['GET', 'POST'])
def game_content():
    current_app.logger.info(f"API::GAME CONTENT [DATA] {request.data}")
    return


@api_blueprint.route('/metrics_data_service', methods=['GET', 'POST'])
def metrics_data_service():
    current_app.logger.info(f"API::METRICS DATA SERVICE [DATA] {request.data}")
    return


from app import create_app

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Extend the Flask shell context."""
    return {'app': app}


if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0')
else:
    import logging
    from logging.handlers import RotatingFileHandler
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    file_handler = RotatingFileHandler('nexus_dashboard.log', maxBytes=1024 * 1024 * 100, backupCount=20)
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(gunicorn_logger.level)

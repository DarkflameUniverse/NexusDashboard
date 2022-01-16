
from app import create_app

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Extend the Flask shell context."""
    return {'app': app}


if __name__ == '__main__':
    with app.app_context():
        app.run(host='0.0.0.0')


from flask import Flask

from blueprints.index.index import bp_index
from blueprints.login.login import bp_login


def create_app() -> Flask:
    """"""

    # Create the application
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(bp_index)
    app.register_blueprint(bp_login)

    # Return the application
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
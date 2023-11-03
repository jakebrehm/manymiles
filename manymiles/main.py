from flask import Flask

from blueprints.login.login import bp_login


def create_app() -> ...:
    """"""

    app = Flask(__name__)
    
    app.register_blueprint(bp_login)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
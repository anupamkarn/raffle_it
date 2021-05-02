import os
from datetime import datetime, timedelta
from flask import Flask


"""
This function is raffle's application factory.
We are initializing everything starting from configs
to instantiating Flask's instance. We can prevent ourselves
from creating global Flask's instance in every module down
the line. 
"""


def create_app():
    app = Flask(__name__)
    # some default configurations that app will use
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path)
    )
    # overrides the default configuration with values taken from the
    # config.py file in the instance folder if it exists.
    app.config.from_pyfile('config.py', silent=True)

    @app.route('/')
    def profile():
        return 'Welcome to raffle services'

    # Registering db
    from . import db
    db.init_app(app)

    # Registering blueprint of ticket_service
    from . import ticket_service
    app.register_blueprint(ticket_service.bp)

    return app


    



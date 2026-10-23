from flask import Flask

def create_app():
    ''' Create and configure an instance of the Flask application. '''

    # Create the Flase application, and set the instance folder.
    app = Flask(__name__, instance_relative_config=True)

    # Load settings from the congig class(object):
    app.config.from_object('app.config.Config')

    # Register routes
    from app.routes import main_bp
    app.register_blueprint(main_bp)


    return app

            
import flask
# from flask.ext.sqlalchemy import SQLAlchemy
# from flask.ext.login import LoginManager
import os

#print os.getcwd()
app = flask.Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////%s/data.db'%os.getcwd()
app.secret_key = 'thisisarandomstring007becauseilovejamesbond'
app.config['SESSION_TYPE'] = 'filesystem'
# db = SQLAlchemy(app)

# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'

parse_credentials = {
	"application_id": "9nhyJ0OEkfqmGygl44OAYfdFdnapE27d9yj9UI5x",
	"rest_api_key": "xsipM4oBX3sRx415UsWPXHCuuTPhetfmmrubRiPx",
	"master_key": "46qAOhvwQx7KutQ7Y5f2BXjp3AahWLxEh5RqQu16",
}

from flask import Flask

app = Flask(__name__, static_url_path='/static')
from app import views
from credentials import fb_credentials,twitter_credentials

#app.secret_key = 'thisisarandomstring007becauseilovejamesbond'
app.config['SECRET_KEY'] = 'thisisarandomstring007becauseilovejamesbond'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': fb_credentials['app_id'],
        'secret': fb_credentials['app_secret']
    },
    'twitter': {
        'id': twitter_credentials['consumer_key'],
        'secret': twitter_credentials['consumer_secret']
    }
}


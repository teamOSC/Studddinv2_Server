from functools import wraps
from flask import g, request, redirect, url_for, session

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
    	oauth_token = session.get('oauth_token', None)
        if oauth_token is None:
            return redirect(url_for('register', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def is_loggedin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
    	oauth_token = session.get('oauth_token', None)
        if oauth_token is not None and oauth_token[0] is not None:
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function
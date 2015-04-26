from credentials import parse_credentials
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
from parse_rest.user import User
import json

register(parse_credentials["application_id"], parse_credentials["rest_api_key"])

class UserManager():

	def login_twitter(self, details):
		if not User.Query.filter(username=details['screen_name']):
			print "hello"
			User.signup(
				username=details['screen_name'], 
				password='123456',
				NAME=details['name'],
				# cover=details['profile_background_image_url_https'],
				# image=details['profile_image_url']
			)
		else:
			pass

class Post(Object):
    pass

    #def __init__(self, post_content, user_id, **kwargs)
    #    self.post_content = post_content
    #    self.user_id = user_id


class Comment(Object):
    pass


class Feed(Object):
    pass


class Listings(Object):
    pass


class Notes(Object):
    pass

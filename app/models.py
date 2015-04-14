from credentials import parse_credentials
from parse_rest.connection import register
from parse_rest.datatypes import Object, GeoPoint
from parse_rest.user import User

register(parse_credentials["application_id"], parse_credentials["rest_api_key"])


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
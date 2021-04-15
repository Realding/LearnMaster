from flask import current_app
from ..models.models import User
from .restful_resource import RestfulApi, RestfulResource

user_resource = RestfulResource(User)
api = RestfulApi(current_app)
api.add_resource(user_resource, '/user/')

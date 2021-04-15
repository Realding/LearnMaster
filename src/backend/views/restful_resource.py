from datetime import datetime
from typing import NamedTuple

from flask import make_response
from flask_restful import Resource, Api, reqparse, inputs, abort, marshal, fields
from sqlalchemy import Integer, String, Boolean, Text, DateTime
from ..models.db import db
from inspect import signature
from functools import partial
from itertools import chain


class RestfulApi:
    """
        封装 Restful Api
    """

    def __init__(self, app):
        self.app = app
        self.api = Api(self.app)

    def add_resource(self, api_resource, url):
        dict_id_api = {
            'get': lambda _self, _id: api_resource.get_by_id(_self, _id),
            'put': lambda _self, _id: api_resource.put_by_id(_self, _id),
            'delete': lambda _self, _id: api_resource.delete_by_id(_self, _id)
        }
        dict_list_api = {
            'get': lambda _self: api_resource.get_all(_self),
            'post': lambda _self: api_resource.post(_self),
        }
        print(api_resource.name)
        id_resource_class = type("IdResource", (Resource,), dict_id_api)
        list_resource_class = type("ListResource", (Resource,), dict_list_api)

        # print(list_resource_class)
        # print(dir(list_resource_class().get(1)))

        self.api.add_resource(id_resource_class, url + '<int:_id>')
        self.api.add_resource(list_resource_class, url)


parser_dict = {
    Integer: int,
    String: str,
    Boolean: inputs.boolean,
    DateTime: inputs.datetime,
    Text: str,
}

marshal_dict = {
    Integer: fields.Integer,
    String: fields.String,
    Boolean: fields.Boolean,
    DateTime: fields.DateTime,
    Text: fields.String,
}


class RestfulResource:
    """
        封装 Restful Resource
        通过定义在 models 的参数，生成默认的 RESTful Api
    """

    def __init__(self, model):
        self.model = model
        self.name = self.model.__table__.name
        self.parser = reqparse.RequestParser()
        self.fields = {}
        self.add_parser()
        self.add_fields()

    def add_parser(self):
        # 添加请求参数
        for field in self.model.input_fields:
            columns = self.model.__table__.columns
            if field in columns:
                # print(columns[field].unique)
                parser_type = parser_dict.get(type(columns[field].type))
            else:
                parser_type = str
            # print(field, parser_type)
            if parser_type is None:
                raise Exception('Unknown Column Type: {} <{}>'.format(columns[field].type, columns[field]))
            self.parser.add_argument(field, parser_type)

    def add_fields(self):
        # 添加返回参数
        for key in self.model.return_fields:
            v = self.model.__table__.columns.get(key)
            self.fields[key] = marshal_dict.get(type(v.type))
        # print(self.fields)

    def get_by_id(self, _self, _id):
        obj = self.model.query.get(_id)
        if obj is None:
            abort(404)
        return marshal(obj, self.fields)

    def delete_by_id(self, _self, _id):
        obj = self.model.query.get(_id)
        db.session.delete(obj)
        db.session.commit()
        return '', 204

    def put_by_id(self, _self, _id):
        args = self.parser.parse_args(strict=True)
        print("put ", args)
        obj = self.model.query.get(_id)
        for k, v in args.items():
            if v:
                if self.check_unique(k, v) in [obj, False]:
                    obj.__setattr__(k, v)
                else:
                    return "Unique argument {}:{} has been used.".format(k, args[k]), 400
        db.session.commit()
        return marshal(obj, self.fields)

    def get_all(self, _self):
        objs = self.model.query.all()
        # print(objs)
        # print(objs._asdict())
        # response = make_response(marshal(objs, self.fields)[0])
        # response.headers['Content-Type'] = 'text/plain;charset=UTF-8'
        # return response
        return marshal(objs, self.fields)

    def post(self, _self):
        args = self.parser.parse_args()
        print("post", args)
        # 检查唯一性
        for k in args:
            if self.check_unique(k, args[k]):
                return "Unique argument {}:{} has been used.".format(k, args[k]), 400

        obj = self.model(**args)
        db.session.add(obj)
        db.session.commit()
        return marshal(obj, self.fields)

    def check_unique(self, k, v):
        columns = self.model.__table__.columns
        uni_arg = {}
        if v and k in columns and columns[k].unique:
            uni_arg[k] = v
            # print(uni_arg)
            uni_obj = self.model.query.filter_by(**uni_arg).first()
            # print(uni_obj)
            if uni_obj:
                return uni_obj
        return False

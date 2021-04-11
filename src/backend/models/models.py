# 数据模型
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from .db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True)
    phone = db.Column(db.String(11), unique=True)
    signature = db.Column(db.String(256))
    is_admin = db.Column(db.Boolean)
    create_time = db.Column(db.DateTime)
    login_time = db.Column(db.DateTime)
    articles = db.relationship('Article', backref='user', lazy='dynamic')

    # password attribute
    # getter
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __init__(self, username, password, email=None, phone=None):
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.is_admin = False
        self.create_time = datetime.now()
        self.login_time = datetime.now()

    default_fields = [
        "id",
        "username",
        "signature",
    ]

    detail_fields = [
        "phone",
        "email",
        "is_admin",
        "create_time",
        "login_time"
    ]

    def __repr__(self):
        return '<User {}_{}>'.format(self.username, self.id)


tags = db.Table('tags',
                db.Column('tag_id', db.Integer, db.ForeignKey('tag.id')),
                db.Column('article_id', db.Integer, db.ForeignKey('article.id'))
                )


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    content = db.Column(db.Text)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    is_private = db.Column(db.Boolean)
    tags = db.relationship('Tag', secondary=tags,
                           backref=db.backref('articles', lazy='dynamic'))

    def __init__(self, title, author_id, content, category_id=None, is_private=None):
        self.title = title
        self.author_id = author_id
        self.content = content
        self.create_time = datetime.now()
        self.update_time = datetime.now()
        self.category_id = category_id
        self.is_private = is_private

    default_fields = [
        "id",
        "title",
        "content",
        "create_time",
        "update_time",
        "author_id",
        "tags",
    ]

    def __repr__(self):
        return '<Article {}>'.format(self.title)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    articles_number = db.Column(db.Integer)
    articles = db.relationship('Article', backref='category', lazy='dynamic')

    def __init__(self, name):
        self.name = name
        self.articles_number = 0

    def __repr__(self):
        return '<Category {}>'.format(self.name)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(128), unique=True, nullable=False)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Tag {}>'.format(self.name)

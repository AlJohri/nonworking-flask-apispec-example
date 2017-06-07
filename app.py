#!/usr/bin/env python3

import os

from flask import Flask
from apispec import APISpec
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_apispec import FlaskApiSpec

app = Flask(__name__)
app.config.update({
    'SQLALCHEMY_DATABASE_URI': os.environ['DATABASE_URL'],
    'SQLALCHEMY_TRACK_MODIFICATIONS': False,
    'APISPEC_SPEC': APISpec(
        title='app',
        version='v1',
        plugins=['apispec.ext.marshmallow'],
    ),
    'APISPEC_SWAGGER_URL': '/docs/',
})

docs = FlaskApiSpec(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@app.route("/")
def root():
    return "Hello World"

class Template(db.Model):

    __tablename__ = "templates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    namespace = db.Column(db.String(80))
    content = db.Column(db.String(120))

    def __init__(self, name, namespace, content):
        self.name = name
        self.namespace = namespace
        self.content = content

    def __repr__(self):
        return f"<Template {self.namespace} {self.name}>"

from marshmallow import Schema, fields

class TemplateSchema(Schema):
    class Meta:
        fields = ('id', 'name', 'namespace', 'content')

from flask_classful import FlaskView
from flask_apispec import use_kwargs, marshal_with, ResourceMeta

class TemplateResource(FlaskView, metaclass=ResourceMeta):
    route_base = '/templates/'
    trailing_slash = True

    @marshal_with(TemplateSchema(many=True))
    def index(self):
        return Template.query.all()

    @marshal_with(TemplateSchema)
    def get(self, template_id):
        template = Template.query.filter(Template.id == template_id).one()
        return template

TemplateResource.register(app)

# docs.register(TemplateResource)
# docs.register(TemplateResource, endpoint='TemplateResource')
# docs.register(TemplateResource, endpoint='TemplateResource:get')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
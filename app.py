from flask import Flask
from peewee import *
from domain_monitor import set_common_name_endings

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')


# create a peewee database instance -- our models will use this database to
# persist information
db = SqliteDatabase('domain_monitor.db')


# define a base model class that specifies which database to use.
# this way, any subclasses will automatically use the correct database.
class BaseModel(Model):
    class Meta:
        database = db


# create a domain model to specify its fields and represent our domain table declaratively
class Firm(BaseModel):
    firm_name = CharField()
    email_address = CharField(null=True)
    known_domain = CharField(null=True)


# connect to database
db.connect(reuse_if_open=True)


set_common_name_endings(app.config['COMMON_NAME_ENDINGS'])


# create the tables. By default, Peewee will determine if the tables already exist, and conditionally create them
db.create_tables([Firm])

import views

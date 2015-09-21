import os
basedir = os.path.abspath(os.path.dirname(__file__))

OPENID_PROVIDERS = [
{'name': 'Google', 'url':'https://www.google.com/accounts/o8/id'},
{'name': 'Yahoo', 'url':'https://me.yahoo.com'},
{'name': 'Flickr', 'url':'http://www.flickr.com/<username>'}]

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'fizz_buzz.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')


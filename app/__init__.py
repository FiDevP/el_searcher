from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from elasticsearch import Elasticsearch


# создание экземпляра приложения
app = Flask(__name__)
app.config.from_object('config.DevelopementConfig')

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None

# инициализирует расширения
db = SQLAlchemy(app)
migrate = Migrate(app, db)


# import views
from . import views
from . import search
# from . import admin_views

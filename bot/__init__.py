from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bot.variables import DBPath
from flask_apscheduler import APScheduler

app = Flask(__name__)
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()
app.config['SQLALCHEMY_DATABASE_URI'] = DBPath
db = SQLAlchemy(app)

import bot.bot
from bot.models import DuplicateReport

migrate = Migrate(app, db)
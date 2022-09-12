from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from bot.variables import DBPath

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DBPath
db = SQLAlchemy(app)

import bot.bot
from bot.models import DuplicateReport

migrate = Migrate(app, db)
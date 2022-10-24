import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from social_graph.app.vk_session import VkSession

app = Flask(__name__)

app_session = VkSession()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

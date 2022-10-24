import os

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from social_graph.app.vk_session import VkSession

app = Flask(__name__)

app_session = VkSession()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kdrdfagntluhbd:400c53c53e9e1f0e6f082c609f65929845bbd183f59f359ce22368bee43b58eb@ec2-52-23-131-232.compute-1.amazonaws.com:5432/d4ec5vo65efgag'
db = SQLAlchemy(app)

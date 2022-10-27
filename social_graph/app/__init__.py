import os

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask

from social_graph.app.vk_session import VkSession

app = Flask(__name__)

app_session = VkSession()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://fonhqoavpqasjt:226cfdbe5427c0d6d5e346ddbda2f2f49b785d3ff8' \
                                        '0b95d997a0684daa8cbeb7@ec2-44-199-9-102.compu' \
                                        'te-1.amazonaws.com:5432/dn0gdbcvibf1t'

app.config['JSON_AS_ASCII'] = False

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)
db_session = Session()

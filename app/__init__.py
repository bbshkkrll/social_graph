import json
import os
from functools import partial

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import Flask

from app.modules.vk_session import VkSession
from app.models import Base

app = Flask(__name__)

app_session = VkSession()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'].replace('postgres', 'postgresql')
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']

app.config['JSON_AS_ASCII'] = False

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], json_serializer=partial(json.dumps, ensure_ascii=False),
                       client_encoding='utf8')

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
db_session = Session()

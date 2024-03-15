from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import os

from sqlalchemy import Column, DateTime, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime

Base = declarative_base()


engine = create_engine(
    'cockroachdb://neohack:CectGfJj0TEhKlvUmN_0hQ@neo-hack-vacantion-14064.8nj.gcp-europe-west1.cockroachlabs.cloud:26257/neohack-vacation-website',
    connect_args={'sslmode': "allow"}, echo=True)

Session = sessionmaker(bind=engine)
session = Session()


def get_all_orders():
    all_orders = session.query(Order).all()
    return all_orders


print(get_all_orders())
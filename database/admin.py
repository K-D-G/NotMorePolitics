from singletons import*
from sqlalchemy_utils import UUIDType
from flask_login import UserMixin
import uuid

db=Database.get()

class Admin(db.Model, UserMixin):
    __tablename__='admins'

    id=db.Column(db.Integer, primary_key=True)
    #id=db.Column(UUIDType(binary=False), primary_key=True) #Convert to for MySQL: https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
    username=db.Column(db.Text, unique=False, nullable=False)
    password=db.Column(db.Text, unique=False, nullable=False)

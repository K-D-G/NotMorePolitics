from singletons import*
from sqlalchemy_utils import UUIDType
import uuid

db=Database.get()

class Author(db.Model):
    __tablename__='authors'
    __searchable__=['id', 'name']
    id=db.Column(db.Integer, primary_key=True)
    #id=db.Column(UUIDType(binary=False), primary_key=True) #Convert to for MySQL: https://stackoverflow.com/questions/183042/how-can-i-use-uuids-in-sqlalchemy
    name=db.Column(db.Text, unique=False, nullable=False)

    def __init__(self, name):
        self.name=name

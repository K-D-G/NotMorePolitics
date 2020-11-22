from singletons import*

db=Database.get()

class Author(db.Model):
    __searchable__=['name']
    id=db.Column(db.Text, primary_key=True)
    name=db.Column(db.Text, unique=False, nullable=False)

    def __init__(self, name):
        self.name=name

DEBUG=True

'''
if DEBUG:
    PORT=5000
else:
    PORT=80
'''
NAME="NotMorePolitics"
PORT=5000 if DEBUG else 80
BASE_URL='http://127.0.0.1:5000' if DEBUG else '' #Add production URL
DATABASE_RELATIVE_PATH='database/database.db'
DATABASE_PATH=f'sqlite:///{DATABASE_RELATIVE_PATH}'
SQLALCHEMY_TRACK_MODIFICATIONS=True #Tell SQLAlchemy that we don't want to know when things are committed
SECRET_KEY=b'\xf5\xba67\x10a?H\x18\xb20w\xd8\x06\x8f\xc9\x9a\xe1\xe4A\xc6?w\xcf'

RESULTS_LIMIT=10

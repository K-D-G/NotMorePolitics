from singletons import*

db=Database.get()

class Article(db.Model):
    __tablename__='articles'
    __searchable__=['title', 'category', 'subject', 'summary']

    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.Text, unique=False, nullable=False)
    category=db.Column(db.Text, unique=False, nullable=False) #Auth-Right etc
    subject=db.Column(db.Text, unique=False, nullable=False) #One word of what the topic is. For example: capitalism
    summary=db.Column(db.Text, unique=False, nullable=False)
    reads=db.Column(db.Integer, unique=False, nullable=False)
    author_id=db.Column(db.Integer, unique=False, nullable=False)

    def __init__(title, category, subject, summary, author_id):
        self.title=title
        self.category=category
        self.subject=subject
        self.summary=summary
        self.author_id=author_id

    def __repr__(self):
        return f'<Article: {id}, {title}, {author_id}>'

    def get_article_body(self):
        return open(f'database/articles/{self.id}/{self.id}.html').read()

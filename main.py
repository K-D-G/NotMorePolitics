from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_elasticquery
import whooshalchemy.flask_whooshalchemy as whooshalchemy
from sqlalchemy import func
from singletons import*
from constants import*
from database.author import*
from database.article import*
import markdown
import json

#SQLAlchemy deals with SQL injection for us so we don't need to worry
app=FlaskApp.get()
database=Database.get()
whooshalchemy.whoosh_index(app, Article)

LIMIT=10

@app.route('/static', methods=["GET"])
def static_serve():
    return send_from_directory('templates/static', request.args.get('path'))

@app.route('/database-articles', methods=["GET"])
def database_serve_articles():
    return send_from_directory('templates/articles', request.args.get('path'))
@app.route('/database-authors', methods=["GET"])
def database_serve_authors():
    return send_from_directory('templates/authors', request.args.get('path'))

@app.route('/')
def index():
    return render_template('static/html/index.html')

@app.route('/authors')
def authors():
    try:
        page_number=int(request.args.get('page_number'))
        if page_number>0:
            page_number-=1 #So that we count properly
    except:
        page_number=0
    if request.args.get('name'):
        authors=Author.query.whoosh_search(request.args.get('name'))
        max=authors.count()
        if page_number*LIMIT>max+(LIMIT-1):
            return redirect(f'/authors?name={request.args.get("name")}&page_number={max/LIMIT}')
        if max-LIMIT<page_number*LIMIT<max+(LIMIT-1):
            no_next=True
        else:
            no_next=False
        authors=authors.offset(page_number*LIMIT).limit(LIMIT).all()
    else:
        max=Author.query.count()
        if page_number*LIMIT>max+(LIMIT-1):
            return redirect(f'/authors?page_number={max/LIMIT}')
        if max-LIMIT<page_number*LIMIT<max+(LIMIT-1):
            no_next=True
        else:
            no_next=False
        authors=Author.query.offset(page_number*LIMIT).limit(LIMIT).all()
    return render_template('static/html/authors.html', authors=authors, query=request.args.get('name'), page_number=page_number, no_next=no_next)

@app.route('/authors/<string:id>')
def load_author(id):
    author=Author.query.filter_by(id=id).first()
    if not author:
        return redirect('/404')
    return render_template('static/html/author.html', author_id=author.id, author_name=author.name)

@app.route('/articles')
def articles():
    try:
        page_number=int(request.args.get('page_number'))
        if page_number>0:
            page_number-=1
    except:
        page_number=0
    query=None
    if request.args.get('category'):
        query=Article.query.filter_by(category=request.args.get('category'))
    if request.args.get('author'):
        query=query.filter_by(author=request.args.get('author'))
    if request.args.get('search'):
        query=query.whoosh_search(request.args.get('search'))
    if not query:
        query=Article.query

    no_next=True

    articles=query.offset(page_number*LIMIT).limit(LIMIT).all()

    #Fix/Update the search functions on author and here
    #Then do other stuff
    #Socialism is where the government does stuff

    category=request.args.get('category') if request.args.get('category') else ''

    author_names=[]
    for i in range(len(articles)):
        author_names.append(Article.query.filter_by(id=articles[i].id).first())
    return render_template('static/html/articles.html', current_category=category, no_next=no_next, page_number=page_number, articles=articles, author_names=author_names)

@app.route('/articles/<string:id>')
def load_article(id):
    article=Article.query.filter_by(id=id).first()
    if not article:
        return redirect('/404')
    return render_template(f'static/html/article.html', article_id=article.id, article_title=article.title)

@app.route('/about')
def about():
    return render_template('static/html/about.html')

@app.route('/policies/<string:name>')
def policies(name):
    return render_template(f'static/html/policy.html', policy_name=name)

@app.errorhandler(404)
def not_found(e):
    return render_template('static/html/error_pages/404.html'), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('static/html/error_pages/500.html'), 500

#============TEMPORARY==========#
@app.route('/todo')
def todo():
    with open('README.md', 'r', encoding='utf-8') as f:
        return markdown.markdown(f.read())
#============TEMPORARY==========#

if __name__=='__main__':
    db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5000)

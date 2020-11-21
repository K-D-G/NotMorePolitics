from flask import Flask, render_template, request, send_from_directory, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy_elasticquery
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
        name=request.args.get('name')
        page_number=int(requests.arg.get('page_number'))
    except:
        return redirect('/404')
    if name:
        arg='{"filter": {"or": {"name": {"like": "%s"}}}}'%name
        authors=sqlalchemy_elasticquery.elastic_query(Author, arg).offset(page_number).limit(10).all()
    else:
        authors=Author.query.offset(page_number).limit(10).all()
    return render_template('static/html/authors.html', authors=authors)

@app.route('/authors/<string:id>')
def load_author(id):
    author=Author.query.filter_by(id=id).first()
    if not author:
        return redirect('/404')
    return render_template('static/html/author.html', author_id=author.id, author_name=author.name)

@app.route('/articles')
def articles():
    '''
    category=request.args.get('category')
    if category:
        articles=Article.query.filter_by(category=category).order_by(func.random()).limit(10).all()
    else:
        articles=Article.query.limit(10).all()
    '''
    try:
        query={}
        if request.args.get('title'):
            query['title']={'like':request.args.get('title')}
        if request.args.get('category'):
            query['category']={'like':request.args.get('category')}
        if request.args.get('subject'):
            query['subject']={'like':request.args.get('subject')}
        if request.args.get('author'):
            query['author_id']=Author.query.filter_by(name=request.args.get('author')).first()
        empty_query=(query=={})
        arg={'filter':{'or':query}}
        page_number=int(requests.arg.get('page_number'))
    except:
        return redirect('/404')

    if not empty_query:
        articles=sqlalchemy_elasticquery.elastic_query(Article, json.dumps(arg)).offset(page_number).limit(10).all()
    else:
        articles=Article.query.offset(page_number).limit(10).all()

    author_names=[]
    for i in range(len(articles)):
        author_names.append(Article.query.filter_by(id=articles[i].id).first())
    return render_template('static/html/articles.html', articles=articles, author_names=author_names)

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

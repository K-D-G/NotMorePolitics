from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy_elasticquery
import whooshalchemy.flask_whooshalchemy as whooshalchemy
from sqlalchemy import func
from singletons import*
from constants import*
from database.author import*
from database.article import*
from database.admin import*
import utils
import markdown
import json
import random

#SQLAlchemy deals with SQL injection for us so we don't need to worry
app=FlaskApp.get()
database=Database.get()
login_manager=FlaskLogin.get()
#whooshalchemy.whoosh_index(app, Article)
#whooshalchemy.whoosh_index(app, Author)

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
    articles=Article.query.order_by(Article.reads).limit(RESULTS_LIMIT).all()
    return render_template('static/html/index.html', articles=articles)

@app.route('/authors')
def authors():
    try:
        page_number=int(request.args.get('page_number'))
    except:
        page_number=1
    if request.args.get('name'):
        authors=Author.query.whoosh_search(request.args.get('name'))
    else:
        authors=Author.query
    authors=authors.paginate(page_number, RESULTS_LIMIT, True)
    return render_template('static/html/authors.html', authors=authors.items, query=request.args.get('name'), page_number=page_number, no_next=(len(authors.items)<RESULTS_LIMIT))

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
    except:
        page_number=1
    articles=Article.query
    if request.args.get('category'):
        articles=Article.query.filter_by(category=request.args.get('category'))
    if request.args.get('search'):
        articles=articles.whoosh_search(request.args.get('search'))
    articles=articles.paginate(page_number, RESULTS_LIMIT, True)

    category=request.args.get('category') if request.args.get('category') else ''

    author_names=[]
    for i in range(len(articles.items)):
        author_names.append(Article.query.filter_by(id=articles[i].id).first())
    return render_template('static/html/articles.html', current_category=category, no_next=(len(articles.items)<RESULTS_LIMIT), page_number=page_number, articles=articles.items, author_names=author_names)

@app.route('/articles/<string:id>')
def load_article(id):
    article=Article.query.filter_by(id=id).first()
    if not article:
        return redirect('/404')
    article.reads+=1
    db.session.commit()
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


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        return redirect(url_for('admin'))
    if request.method=='POST':
        username=request.form['username']
        password=request.form['password']

        admin=Admin.query.filter_by(username=username).first()
        admins=Admin.query.all()
        if admin and utils.check_password(password, admin.password):
            login_user(admin)
            return redirect(url_for('admin'))
        flash({'type':'danger', 'message':'Invalid credentials'})
        return redirect(url_for('admin_login'))
    return render_template('static/html/admin/admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin():
    return render_template('static/html/admin/admin.html', user=current_user)

@login_manager.user_loader
def load_user(id):
    if id is not None:
        return Admin.query.get(int(id))
    return None

@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('admin_login'))

def add_admin(username, password):
    db.session.add(Admin(username=username, password=utils.hash_password(password)))
    db.session.commit()

#============TEMPORARY==========#
@app.route('/todo')
def todo():
    with open('README.md', 'r', encoding='utf-8') as f:
        return markdown.markdown(f.read())
#============TEMPORARY==========#

def add_example_data():
    names=['Bob', 'Kieran', 'People', 'Jeff']
    for i in names:
        db.session.add(Author(name=i, email=i+str(random.randint(0, 100))+'@example.com'))
    db.session.commit()

if __name__=='__main__':
    db.create_all()
    add_admin('Kieran', '1234')
    add_example_data()
    whooshalchemy.whoosh_index(app, Article)
    whooshalchemy.whoosh_index(app, Author)
    app.run(debug=DEBUG, host='0.0.0.0', port=PORT)

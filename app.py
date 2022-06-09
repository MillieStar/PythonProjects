from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

#
# app=Flask(__name__,template_folder='./templates')
'''
werkzeug

jinja2
xtension:
SQLalchemy - database
migrate - move db
mail
WTF - form
script
Login
RESTful - REST API
bootstrap - twitter Bootstrap
Moment
'''

# create app
app = Flask(__name__)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'  # 3-path 4-abs path
db = SQLAlchemy(app)


# model db
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True, )
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='N/A')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post ' + str(self.id)


# add data
# all_posts=[
#     {
#         'title':'Post 1',
#         'content':'This is the content of post 1. Lalala.',
#         'author':'Manni'
#     },
#     {
#         'title': 'Post 2',
#         'content': 'This is the content of post 2. Lalala.',
#
#     }
# ]

# template
@app.route('/')
def index():
    # return '<h1>Home Page</h1>'
    return render_template('index.html')


# data to html
@app.route('/posts', methods=['GET', 'POST'])
def posts():
    # check guard
    if request.method == 'POST':
        # read from form, send to db
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)  # current session
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)


# define url
# @app.route('/') #local host
@app.route('/home/users/<string:name>/posts/<int:id>')  # local host
def hello_world(name, id):
    # return 'Hello World!'
    return 'Hello, ' + name + ', your id is: ' + str(id)


# get
@app.route('/onlyget', methods=['GET'])
# @app.route('/onlyget', methods=['GET','POST'])
def get_req():
    return 'You can only get this webpage. 4'


# delete
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


# edit
@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':

        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)
        # auto update


# new_post
@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


if __name__ == '__main__':
    app.run(debug=True)

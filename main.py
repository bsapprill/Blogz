from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:asdf@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1000))

    def __init__(self,name,content):
        self.title = name
        self.content = content

@app.route('/blogs', methods=['POST', 'GET'])
def displayBlog():
    if not request.args.get('id'):
        blogs = BlogPost.query.all()
        return render_template('blogs.html', blogs=blogs)
    else:
        blog = BlogPost.query.filter_by(id=request.args.get('id')).first()
        return render_template('blogView.html.', blog=blog)

@app.route('/newBlog', methods=['POST', 'GET'])
def newBlogPost():
    if request.method == 'POST':
        title = request.form['titleInput']
        body = request.form['newBlogPost']

        titleInvalid = False
        bodyInvalid = False
        
        if title == "" or body == "":
            if title == "":
                titleInvalid = True
            if body == "":
                bodyInvalid = True
        else:
            newPost = BlogPost(title,body)
            db.session.add(newPost)
            db.session.commit()
            return redirect('/blogs?id='+str(newPost.id))

        return render_template("/newBlog.html", title=title, content=body, error1=titleInvalid,
                                error2=bodyInvalid)

    else:
        return render_template('/newBlog.html')

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('base.html')

if __name__ == '__main__':
    app.run()
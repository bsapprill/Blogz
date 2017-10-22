from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:asdf@localhost:8889/Blogz'
app.config['SQLALCHEMY_ECHO'] = True

app.secret_key = 'y337kGcys&zP3B'

db = SQLAlchemy(app)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(1000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self,name,content, owner):
        self.title = name
        self.content = content
        self.owner = owner

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120),unique=True)
    password = db.Column(db.String(120))
    blogs = db.relationship('BlogPost', backref='owner')
    
    def __init__(self,username,password):
        self.username = username
        self.password = password

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
    
    owner = User.query.filter_by(username=session['username']).first()

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
            newPost = BlogPost(title,body,owner)
            db.session.add(newPost)
            db.session.commit()
            return redirect('/blogs?id='+str(newPost.id))

        return render_template("/newBlog.html", title=title, content=body, error1=titleInvalid,
                                error2=bodyInvalid)

    else:
        return render_template('/newBlog.html')

@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        passwordCheck = request.form['passwordVerify']

        validUsernameBool = True
        validPasswordBool = True
        validVerifyBool = True

        if username == "" or not validInputString(username):
            validUsernameBool = False

        if password == "" or not validInputString(password):
            validPasswordBool = False

        if passwordCheck != password or passwordCheck == "":
            validVerifyBool = False

        if not validUsernameBool or not validPasswordBool or not validVerifyBool:
            return render_template("signup.html", error1 = validUsernameBool,                                                    
                                                  error2 = validPasswordBool, 
                                                  error3 = validVerifyBool)
        else:
            session['username']=username

            newUser = User(username,password)
            db.session.add(newUser)
            db.session.commit()

            return redirect("/newBlog")

    else:
        return render_template("signup.html")

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']

        invalidUser = True
        invalidPassword = True

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            session['username'] = username
            return redirect('/newBlog')
        elif not user:
            return render_template('login.html', error1=invalidUser)
        elif user and user.password != password:
            return render_template('login.html', error1=invalidPassword)
        #else:
    else:
        return render_template('login.html')

#@app.route('/index')

@app.route('/logout', methods=['POST'])
def logout():
    #delete username
    del session['email']
    return redirect('/blogs')

@app.route('/', methods=['POST', 'GET'])
def index():
    return redirect('/login')

def validInputString(inputString):
    stringLength = len(inputString)

    validStringBool = True

    if stringLength < 3 or stringLength > 20:
        validStringBool = False
    elif ' ' in inputString:
        validStringBool = False

    return validStringBool

if __name__ == '__main__':
    app.run()
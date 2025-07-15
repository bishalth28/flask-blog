from flask import Flask, render_template, request, url_for, redirect, session, flash
import json, os

app = Flask(__name__)
app.secret_key = os.urandom(24)

if os.path.exists('user.json'):
    with open('user.json') as f:
        users = json.load(f)
else:
    users = {}

if os.path.exists('posts.json'):
    with open('posts.json') as f:
        posts = json.load(f)
else:
    posts = {}

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home ():
    if 'username' not in session:
        flash("please login")
        return redirect(url_for('login'))
    
    return render_template('home.jinja2',posts=posts)
1
@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return render_template("login.jinja2", error = "Invalid credentials")
        
    return render_template('login.jinja2')

@app.route('/signup', methods = ['GET','POST'])
def signup():
    if request.method == "POST":
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        if username in users:
            flash("Username already exists!", "error")
            return render_template("signup.jinja2")

        users[username] ={
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'password': password  
        }
        with open('user.json', 'w') as f:
            json.dump(users, f, indent=4)

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for('login'))

    return render_template("signup.jinja2")



@app.route ('/post/<int:post_id>')
def post(post_id):
    post=posts.get(str(post_id))
    if not post:
        return render_template('error.jinja2', message=f'A post with id {post_id} was not found.')
    return render_template('post.jinja2', post=post)

@app.route ('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/create', methods = ['GET', 'POST'])
def create():
    if 'username' not in session:
        flash("please login")
        return redirect(url_for('login'))

    if request.method == 'POST':
        title = request.form.get('title')
        tag = request.form.get('tag')
        description = request.form.get('description')

        post_id = str(len(posts))
        posts[post_id]={'post_id':int(post_id), 'title':title, 'tag':tag, 'description':description}

        with open('posts.json', 'w') as f:
            json.dump(posts, f, indent=4)

        flash("Post Created Successfully")
        return redirect(url_for('post',post_id = post_id))
    else:
        return render_template('create.jinja2')

if __name__ == '__main__':
    app.run(debug=True)
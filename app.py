from flask import Flask, render_template

app = Flask(__name__)

posts = {
    0:{
        'title':'Hello Bishal',
        'content':'This is my first blog post'
    }
}

@app.route('/')
def home ():
    return 'hello World'

@app.route ('/post/<int:post_id>')
def post(post_id):
    post=posts.get(post_id)
    if not post:
        return render_template('404.jinja2', message=f'A post with id {post_id} was not found.')
    return render_template('post.jinja2', post=post)

@app.route('/post/form')
def form():
    return render_template('create.jinja2')

if __name__ == '__main__':
    app.run(debug=True)
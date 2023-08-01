"""Blogly application."""

from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.app_context().push()
connect_db(app)
# db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "MOKEY"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route("/")
def list_users():
    """List users and show add button."""
    users= User.query.all()
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("list.html", users=users, posts=posts)

@app.route("/add-user", methods= ["GET"])
def add_more_users_form():
    """Shows the form to add more users"""

    return render_template("user/add-user.html")

@app.route("/add-user", methods= ["POST"])
def add_more_users(): 
    """Send new user info to db"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img = request.form['img-url']

    user = User(first_name=first_name, last_name=last_name, image_url=img or None)
    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route("/users/<int:user_id>")
def show_user_detail(user_id):
    """Shows user info detail and allows you to edit"""

    user = User.query.get_or_404(user_id)
    return render_template('user/user-detail.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_and_delete_user_form(user_id):
    """Shows form to edit user info"""

    user = User.query.get_or_404(user_id)
    return render_template('user/user-edit.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Shows you the form to edit user info"""
    user = User.query.get_or_404(user_id)
    new_user= User(
        first_name = request.form['first-name'],
        last_name = request.form['last-name'],
        image_url = request.form['img-url'] or None)

    db.session.add(new_user)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes users from the database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

#------------------------- POST RELATED ROUTES -------------------------------#

@app.route('/users/<int:user_id>/posts/new', methods=['GET'])
def add_new_post_form(user_id):
    """Show add post form"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('post/add-post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_new_post(user_id):
    """Adds post to database for a specific user"""
    
    title = request.form['post-title']
    content = request.form['post-content']
    tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post = Post(title=title, content=content, user_id=user_id, tags=tags)
    db.session.add(post)
    db.session.commit()
    
    flash(f"Post '{post.title}' has been added")

    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post_detail(post_id):
    """Shows post detail and option to edit or delete it"""

    post = Post.query.get_or_404(post_id)
    return render_template('post/post-detail.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['GET'])
def post_edit_form(post_id):
    """Shows post edit form"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()

    return render_template('post/post-edit.html', post=post, tags=tags)

@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def post_edit(post_id):
    """Shows post edit form"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['post-title']
    post.content = request.form['post-content']
    tag_ids = [int(tag_id) for tag_id in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    post.tags = tags
    
    db.session.add(post)
    db.session.commit()
    # import pdb
    # pdb.set_trace()
    flash(f"Post '{post.title}' edited.")

    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def post_delete(post_id):
    """Delete post and redirect the user profile"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title}' deleted.")

    return redirect(f'/users/{post.user_id}')


# ------------------------------ Tag related routes -----------------------------------------#

@app.route('/tags')
def list_all_tags():
    """List all tags"""

    tags = Tag.query.all()
    return render_template('tag/list.html', tags= tags)

@app.route('/tags/<int:tag_id>')
def tag_detail(tag_id):
    """Show tag deatil"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag/detail.html', tag= tag)

@app.route('/tags/new', methods=['GET'])
def add_tag_form():
    """Shows form to add more tags"""
    posts = Post.query.all()
    return render_template('tag/add.html', posts=posts)
    
@app.route('/tags/new', methods=['POST'])
def add_tag():
    """Send new tag to db"""

    tag_name = request.form['tag-name']
    tag = Tag(name=tag_name)

    post_ids = [int(post_id) for post_id in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag.posts = posts

    db.session.add(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' added.")
    return redirect('/tags')
    
@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def tag_edit_form(tag_id):
    """Shows tag edit form"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tag/edit.html', tag=tag, posts=posts)

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def tag_edit(tag_id):
    """Shows tag edit form"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['tag-name']

    post_ids = [int(post_id) for post_id in request.form.getlist('posts')]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    tag.posts = posts
    
    db.session.add(tag)
    db.session.commit()
    
    flash(f"Tag '{tag.name}' edited.")

    return redirect(f'/tags/{tag.id}')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def tag_delete(tag_id):
    """Deletes tags"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")
    return redirect('/tags')

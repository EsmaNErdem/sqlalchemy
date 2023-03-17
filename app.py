"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User

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

    users = User.query.all()
    return render_template("list.html", users = users)

@app.route("/add-user", methods= ["GET"])
def add_more_users_form():
    """Shows the form to add more users"""

    return render_template("add-user.html")

@app.route("/add-user", methods= ["POST"])
def add_more_users(): 
    """Send user info to db"""

    first_name = request.form['first-name']
    last_name = request.form['last-name']
    img = request.form['img-url']

    user = User(first_name=first_name, last_name=last_name, image_url=img)
    db.session.add(user)
    db.session.commit()

    return redirect('/')

@app.route("/users/<int:user_id>")
def show_user_detail(user_id):
    """Shows user info detail and allows you to edit"""

    user = User.query.get_or_404(user_id)
    return render_template('user-detail.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["GET"])
def edit_and_delete_user_form(user_id):
    """Shows you the form to edit user info"""

    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def update_user(user_id):
    """Shows you the form to edit user info"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first-name']
    user.last_name = request.form['last-name']
    user.image_url = request.form['img-url']

    db.session.add(user)
    db.session.commit()
    
    return redirect(f'/users/{user.id}')

@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Deletes users from the database"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/')

# with app.app_context():
#     db.create_all()



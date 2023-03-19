"""Models for Blogly."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db =  SQLAlchemy()
default_img = 'https://upload.wikimedia.org/wikipedia/commons/9/99/Sample_User_Icon.png'

def connect_db(app):
    """Connecting the database"""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Creating User Model"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                    autoincrement=True)
    first_name = db.Column(db.Text,
                     nullable=False)
    last_name = db.Column(db.Text,
                     nullable=False)
    image_url = db.Column(db.Text,
                     nullable=False, default = default_img)
    
    posts=db.relationship('Post', backref='user')

    @property
    def get_full_name(self):
        """Return users fullname"""

        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        """Show info"""

        u = self
        return f"<User {u.first_name} {u.last_name} with {u.id}id >"
    
class Post(db.Model):
    """Creating Post Model"""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                    autoincrement=True)
    title = db.Column(db.Text,
                     nullable=False)
    content = db.Column(db.Text,
                     nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        """Show info"""

        u = self
        return f"<Post id:{u.id} title:{u.title} content:{u.content} created_at:{u.created_at} user_id:{u.user_id}>"
    @property
    def friendly_time(self):
        """Convert datetime to human readable text"""

        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")

    
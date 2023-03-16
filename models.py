"""Models for Blogly."""

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
                     nullable=False,)
    last_name = db.Column(db.Text,
                     nullable=False,)
    image_url = db.Column(db.Text,
                     nullable=False, default = default_img)
    @property
    def get_full_name(self):
        """Return users fullname"""

        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        """Show info"""

        u = self
        return f"<User {u.first_name} {u.last_name} with {u.id}id >"
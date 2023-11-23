"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False, index=True)
    last_name = db.Column(db.String(50),
                     nullable=False, index=True)
    image_url = db.Column(db.String(450), 
                     default='default_profile.jpg')

class Post(db.Model):
    """Posts from users."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                      nullable = False)
    content = db.Column(db.String(255),
               nullable = False)
    created_at = db.Column(db.DateTime, 
                           default=datetime.utcnow)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'))
    
    users = db.relationship('User', backref='posts')
    tags = db.

class Tag(db.Model):
    """Tags."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship('Tag', secondary='posttag', backref='tag')

class PostTag(db.Model):
    __tablename__ = 'post_tag'
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'), primary_key=True)

    __table_args__ = (
        db.UniqueConstraint('post_id', 'tag_id'),
    )
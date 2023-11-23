"""Blogly application."""

from flask import Flask, request, redirect, render_template
from models import db, connect_db, User, Post, Tag, PostTag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = 'blogly-secret-key'
debug = DebugToolbarExtension(app)


@app.before_first_request
def create_tables():
    """Create all tables."""
    db.create_all()

@app.route('/')
def home():
    """Redirect to list of users."""

    return redirect('/users')

@app.route('/users')
def list_users():
    """Show all users. Make these links to view the detail page for the user. Have a link here to the add-user form.
    """
    users = User.query.all()
    return render_template("users.html", users=users)

@app.route('/users/new')
def add_user():
    """Show an add form for users."""

    return render_template('user_form.html')

@app.route('/users/new', methods=["POST"])
def user_added():
    """Process the add form, adding a new user and going back to /users."""

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<int:user_id>')
def user_details(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    posts = user.posts
    return render_template("user_details.html", user=user, posts=posts)

@app.route("/users/<int:user_id>/edit")
def edit_page(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)

@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Process the edit form, returning the user to the /users page."""
    edited_user = User.query.get_or_404(user_id)
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    image_url = request.form["image_url"]

    edited_user = User(first_name = first_name, last_name = last_name, image_url = image_url)

    db.session.add(edited_user)
    db.session.commit()
    return redirect('/users')

@app.route('/delete/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    """Delete the user."""

    deleted_user = User.query.get_or_404(user_id)

    delete_user = User.query.filter_by(user_id = user_id).delete()
    
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def post_form(user_id):
    """Show form to add a post for that user."""
    user = User.query.get_or_404(user_id)
    return render_template('post_form.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """Handle add form; add post and redirect to the user detail page."""

    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["content"]

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    added_post = Post(title=title, content=content, user=user, tags=tags)

    db.session.add(added_post)
    db.session.commit()
    
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """Show a post."""

    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_form(post_id):
    """Show form to edit a post, and to cancel (back to user page)."""

    post = Post.query.get_or_404(post_id)
    return render_template('edit_post.html', post=post)




@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view"""
    edited_post = Post.query.get_or_404(post_id)

    title = request.form['title']
    content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    edited_post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()


    edited_post = Post(title=title, content=content)

    db.session.add(edited_post)
    db.session.commit()

    return redirect('/users')

@app.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Delete the post."""

    deleted_post = User.query.get_or_404(post_id)

    delete_post = User.query.filter_by(user_id =post_id).delete()
    
    db.session.commit()
    return redirect('/users')

@app.route('/tags')
def list_tags():
    """Lists all tags, with links to the tag detail page."""
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/new')
def add_tag():
    """Show an add form for tags."""

    return render_template('tag_form.html')

@app.route('/tags/new', methods=["POST"])
def tag_added():
    """Process the add form, adding a new tag and going back to /tags."""

    name = request.form["name"]

    new_tag = User(name = name)

    db.session.add(new_tag)
    db.session.commit()

    return redirect('/tags')

@app.route('/tag/<int:tag>')
def tag_details(tag_id):
    """Show detail about a tag. Have links to edit form and to delete."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag_details.html', tag=tag)

@app.route("/tags/<int:tag_id>/edit")
def edit_tag(tag_id):
    """Show the edit page for a tag."""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edited_tag(tag_id):
    """Process the edit form, returning the user to the /tags page."""
    edited_tag = Tag.query.get_or_404(tag_id)
    name = request.form["name"]
    
    edited_tag = Tag(name = name)
    db.session.add(edited_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_user(tag_id):
    """Delete the tag."""

    deleted_tag = Tag.query.get_or_404(tag_id)

    delete_tag = Tag.query.filter_by(tag_id = tag_id).delete()
    
    db.session.commit()
    return redirect('/tags')





if __name__ == '__main__':
    app.run(debug=True)
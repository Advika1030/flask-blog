#routes.py

import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort, current_app
from datetime import datetime
from flaskBlog import app, db, bcrypt
from flaskBlog.form import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RSVPForm
from flaskBlog.models import User,Post, RSVP
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Mail, Message


@app.route("/")
@app.route("/home")
def home():
    posts = Post.query.all()
    return render_template('home.html', posts = posts)

@app.route("/about")
def about():
    return render_template('about.html', title = 'About')

@app.route("/register", methods = ['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit(): #flash message
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8') #hashing the password
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to login','success')
        return redirect(url_for('login'))
    return render_template('register.html', title = 'Register', form = form)

@app.route("/login", methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user,remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password','danger')
    return render_template('login.html', title = 'Login', form = form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_picture(form_picture):
    if form_picture:
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path,'static/profile_pics', picture_fn)

        output_size = (125,125)
        i = Image.open(form_picture)
        i.thumbnail(output_size)
        i.save(picture_path)

        return picture_fn


@app.route("/account", methods = ['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename = 'profile_pics/'+current_user.image_file)
    return render_template('account.html', title = 'Account', image_file = image_file, form = form)


@app.route("/post/new", methods = ['GET','POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!','success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title = 'New Post', form = form, legend = 'New Post')


# ...
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    rsvp_form = RSVPForm()
    
    #counting rsvp's
    rsvp_count = RSVP.query.filter_by(post_id=post_id).count()

    if rsvp_form.validate_on_submit():
        if not RSVP.query.filter_by(user_id=current_user.id, post_id=post_id).first():
            rsvp = RSVP(user_id=current_user.id, post_id=post_id)
            db.session.add(rsvp)
            db.session.commit()
            flash('You have RSVP\'d to the event.', 'success')
        else:
            flash('You have already RSVP\'d to this event.', 'warning')

    return render_template('post.html', title=post.title, post=post, rsvp_form=rsvp_form, rsvp_count=rsvp_count)



@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    # Check if the current user is the author of the post
    if post.author != current_user:
        abort(403)  # HTTP 403 Forbidden

    # Delete the post and its associated RSVPs
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/rsvp/<int:post_id>", methods=['POST'])
@login_required
def rsvp_post(post_id):
    post = Post.query.get_or_404(post_id)
    rsvp_form = RSVPForm()

    if rsvp_form.validate_on_submit():
        # Check if the user has already RSVP'd for the event
        if not RSVP.query.filter_by(user_id=current_user.id, post_id=post_id).first():
            rsvp = RSVP(user_id=current_user.id, post_id=post_id)
            db.session.add(rsvp)
            db.session.commit()
            flash('You have RSVP\'d to the event', 'success')

        else:
            flash('You have already RSVP\'d to this event.', 'warning')


        

    return render_template('post.html', title=post.title, post=post, rsvp_form=rsvp_form)





#....

@app.route("/your_events")
@login_required
def your_events():
    rsvps = RSVP.query.filter_by(user_id=current_user.id).all()
    return render_template('your_events.html', title='Your Events', rsvps=rsvps)



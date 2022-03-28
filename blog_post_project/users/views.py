from flask import render_template, url_for, redirect, request, Blueprint
from flask_login import login_user,current_user,logout_user,login_required
from blog_post_project import db
from blog_post_project.models import User, BlogPost
from blog_post_project.users.forms import LoginForm,RegistrationForm,UpdateUserForm
from blog_post_project.users.picture_handler import add_profile_pic

users = Blueprint('users',__name__)

@users.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,username=form.username.data,password=form.password.data)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('users.registered'))
    return render_template('register.html',form=form)

@users.route('/registered')
def registered():
    return render_template('registered.html')

@users.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    pass_message=''
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user is not None and user.check_password(form.password.data):
            login_user(user)

            next = request.args.get('next')

            if next == None or not next[0]=='/':
                next = url_for('core.index')
            return redirect(next)

        elif not user.check_password(form.password.data):
            pass_message = "Incorrect password."


    return render_template('login.html',form=form,pass_message=pass_message)

@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('core.index'))

@users.route('/account',methods=['GET','POST'])
@login_required
def account():
    form = UpdateUserForm()

    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        return redirect(url_for('users.account'))
    
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
 
    return render_template('account.html',form=form)

@users.route("/<username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template('user_blog_posts.html', blog_posts=blog_posts, user=user)
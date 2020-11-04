from . import main
from ..requests import get_quotes
from flask import render_template, request, redirect, url_for,abort
from flask_login import login_required,current_user
from ..models import User,Blog_post,Comment,Subscribe
from .forms import UpdateProfile, BlogForm,SubscribeForm,CommentForm
from .. import db,photos
from ..email import mail_message

@main.route('/', methods=['GET','POST'])
def index():
    '''
    View root page function that returns the index page and its data
    '''
    #Getting random Quotes
    random_quotes=get_quotes()
    print(random_quotes)
    title = "Home- Gee's Blog_me post"
    #Getting blogs from all users
    blogs = Blog_post.get_all_blog()
    form = SubscribeForm()
    if form.validate_on_submit():
        email = form.email.data
        
        new_subscriber=Subscribe(email=email)
        new_subscriber.save_subscriber()
        
        mail_message("Subscribed to Blog_me post","email/welcome_subscriber",new_subscriber.email,subscriber=new_subscriber)
    
    return render_template('index.html',title=title,random_quotes=random_quotes, blogs=blogs, subscriber_form=form) 




@main.route('/user/<uname>')
def profile(uname):
    user = User.query.filter_by(username=uname).first()
    
    if user is None:

        abort(404)
    bloglist = Blog_post.get_blog(user.username)

    return render_template('profile/profile.html', user=user, bloglist=bloglist)


@main.route('/user/<uname>/update',methods=['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username=uname).first()

    if user is None:

        abort(404)

    form = UpdateProfile()
    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()
        
        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form=form)






@main.route('/delete/<int:id>' ,methods=['GET',"POST"])
@login_required
def delete(id):
    blog=Blog_post.query.filter_by(id=id).first()
    Blog_post.delete_blog(blog)
    
    return redirect(url_for('main.profile',uname=current_user.username))


@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',uname=uname))

@main.route('/blog/new/<uname>', methods=['GET','POST'])
@login_required
def new_blog(uname):
    user = User.query.filter_by(username=uname).first()
    form = BlogForm()
    if form.validate_on_submit():
        title = form.title.data
        category=form.category.data
        blog_content = form.blog_post.data
        
        new_blog = Blog_post(user =current_user.username, title= title, blog_content=blog_content,category=category)
        category = form.category.data
        db.session.add(new_blog)
        db.session.commit()
        
        subscribers= Subscribe.query.all()
        
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,user =user)
        
        return redirect(url_for('.profile',uname=user.username))    
    title = 'new blog'
    
    return render_template('blogs.html',form = form,title=title)
        

@main.route('/comment/<int:id>' , methods = ['GET' , 'POST'])
def comment(id):
    form = CommentForm()
    comment = Comment.get_blog_comment(id)
    if form.validate_on_submit():
        comment = form.description.data
        new_comment = Comment(comment = comment,user = current_user.username,blog_id = id)
        new_comment.save_comments()
        return redirect(url_for('.comment',id = id ))
    return render_template('comment.html',commentForm = form,comment = comment)
   

@main.route('/subscribe', methods=['GET','POST'])
@login_required
def subscriber():
    subscriber=SubscribeForm()
    if subscriber_form.validate_on_submit():
         
        subscriber= Subscriber(email=subscriber_form.email.data,name = subscriber_form.name.data)
        
        
        db.session.add(subscriber)
        db.session.commit()
       
        
        mail_message("Hello Welcome To Blog_me","email/welcome_subscriber",subscriber.email,subscriber=subscriber)
    subscriber = Blog_post.query.all()

    return render_template('subscribe.html',subscriber=subscriber,subscriber_form=subscriber_form,blog=blog)
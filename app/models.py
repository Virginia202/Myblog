from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


class Quote:
    '''
    Quote class to define the quote objects
    '''
    def __init__(self,id,author,quote):
        self.id=id
        self.author=author
        self.quote=quote
        

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255))
    email = db.Column(db.String(),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    pass_word = db.Column(db.String(255))
    
    
    @property
    def password(self):
        raise AttributeError('You cannot read the password attribute')
    
    
    @password.setter
    def password(self,password):
        self.pass_word = generate_password_hash(password)
        
    def verify_password(self,password):
        return check_password_hash(self.pass_word,password)

    def __repr__(self):
        return f'User {self.username}'
    
class Blog_post(db.Model):
    __tablename__ = 'blog'
    
    id = db.Column(db.Integer,primary_key = True)
    
    title = db.Column(db.String)
    user = db.Column(db.String)
    blog_content = db.Column(db.String)
    date_posted = db.Column(db.DateTime,default=datetime.utcnow)
    category = db.Column(db.String)
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
        
    
    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_blog(cls,name):
        blogs = Blog_post.query.filter_by(user=name).all()
        return blogs
    
    @classmethod
    def get_all_blog(cls):
        blog_list = Blog_post.query.all()
        return blog_list
    
    def __repr__(self):
        return f'Blog_post{self.blog_content}'
    
    
class Comment(db.Model):
    __tablename__='comment'
    
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer)
    user = db.Column(db.String)
    posted = db.Column(db.DateTime,default = datetime.utcnow)
    blog_content = db.Column(db.String)
    description = db.Column(db.Text)
    
    
    def save_comments(self):
        db.session.add(self)
        db.session.commit()
    
    @classmethod    
    def get_blog_comment(cls,id):
        comment = Comment.query.filter_by(blog_id=id)
        return comment
        
        
    def delete_blog(self):
        db.session.delete(self)
        db.session.commit()    

    def __repr__(self):
        return f"Comment : id:{self.id} comment:{self.desription}"

class Subscribe(db.Model):
    '''
    class defining how users data who have subscribed will be stored
    '''
    __tablename="subscribes"
    id=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(255), unique=True,index=True)

    def save_subscriber(self):
        '''
        function that saves a subscriber in the db  
        '''
        db.session.add(self)
        db.session.commit()
        

    def __repr__(self)  :
        '''
        function that helps in debugging.
        '''
        return f'Comment {self.body}'        
        
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))        
        
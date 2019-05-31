from sqlalchemy.sql import func
from config import db, bcrypt
import re
from flask import session

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


add_jobs = db.Table('add_job', 
        db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
        db.Column('job_id', db.Integer, db.ForeignKey('jobs.id'), primary_key=True), 
        db. Column('created_at', db.DateTime, server_default=func.now())) 


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    pw_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
    jobs_user_add = db.relationship('Job', secondary=add_jobs)

    #class to validate user registration
    @classmethod
    def register_validation(cls, form):
        errors = []
        if len(form['first_name']) < 1:
            errors.append("Please enter your first name!")
        if len(form['last_name']) < 1:
            errors.append("Please enter your last name!")
        if not EMAIL_REGEX.match(form['email']):
            errors.append("Please enter valid email address!")
        
        #validate if email is already registered
        existing_emails = cls.query.filter_by(email=form['email']).first()
        if existing_emails:
            errors.append("Email is already registered!")
        if form['password'] != form['confirm_password']:
            errors.append("Password must be match!")
        if len(form['password']) < 8:
            errors.append("Password must be at least 8 characters!")
        elif re.search('[0-9]', form['password']) is None:
            errors.append("Password required a number!")
        
        return errors

    @classmethod
    def user_create(cls, form):
        pw_hash = bcrypt.generate_password_hash(form['password'])
        user = cls(
            first_name = form['first_name'],
            last_name = form['last_name'],
            email = form['email'],
            pw_hash = pw_hash,
        )
        db.session.add(user)
        db.session.commit()
        return user.id

#validate logins
    @classmethod
    def login_validation(cls, form):
        user = cls.query.filter_by(email=form['email']).first()
        if user:
            if bcrypt.check_password_hash(user.pw_hash, form['password']):
                return (True, user.id)
        return (False, "Emaill or password is incorrect")
    
#edit users info
    @classmethod
    def user_edit(cls, form):
        edit_user_info = User.query.get(session['user_id'])
        edit_user_info.first_name = form['first_name']
        edit_user_info.last_name = form['last_name']
        edit_user_info.email = form['email']
        edit_user_info.password = form['password']
        db.session.commit()
        return edit_user_info.id
    
#get users by id
    @classmethod
    def get_user(cls, id):
        user = User.query.get(id)
        print(user)
        return user

#jobs that user added
    @classmethod
    def add_job(cls, id):
        current_user = User.query.get(session['user_id'])
        job = Job.query.get(id)
        current_user.jobs_user_add.append(job)
        db.session.commit()
        return current_user

#get jobs that user added
    @classmethod
    def job_list_user_add(cls, id):
        job_list_user_add = User.query.get(id)
        return job_list_user_add.jobs_user_add
    

class Job(db.Model):
    __tablename__ = 'jobs'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())
    updated_at = db.Column(db.DateTime, server_default=func.now(), onupdate=func.now())
#relationship with user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', foreign_keys=[user_id], backref='all_jobs', cascade='all')
    users_who_add_jobs = db.relationship('User', secondary=add_jobs)



#validate creating jobs
    @classmethod
    def jobs_validation(cls, form):
        errors = []
        if len(form['title']) < 1:
            errors.append('Please enter the Job title')
        if len(form['location']) < 1:
            errors.append('Please enter the location')
        if len(form['description']) < 1:
            errors.append('Please enter the description')
        return errors


    @classmethod 
    def job_add(cls,form):
        jobs = Job(
            title = form['title'],
            location = form['location'],
            description = form['description'],
            user_id = session['user_id'],
        )
        db.session.add(jobs)
        db.session.commit()
        return jobs
        
    @classmethod
    def job_edit(cls, form, id):
        job_info_update = Job.query.get(id)
        job_info_update.title = form['title']
        job_info_update.location = form['location']
        job_info_update.description = form['description']
        db.session.commit()
        return job_info_update

    @classmethod
    def jobs_select(cls, form, id):
        jobs = Job.query.get(id)
        return jobs

    @classmethod
    def jobs_list(cls):
        jobs_list = Job.query.all()
        return jobs_list

    @classmethod
    def job_view(cls, id):
        job_view = Job.query.get(id)
        return job_view

    @classmethod
    def job_delete(cls, id):
        job_delete = Job.query.get(id)
        db.session.delete(job_delete)
        db.session.commit()


    
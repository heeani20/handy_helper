from flask import render_template, redirect, request, session, flash, url_for, Response
from models import User, Job, add_jobs

#login page 
def root():
    if 'user_id' not in session:
        return redirect(url_for('users:new_user'))
    return redirect(url_for('dashboard'))

def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('users:new_user'))

    current_user = User.query.get(session['user_id'])
    # job_user = User.job_list_user_add(id)
    list_of_all_jobs = Job.jobs_list()
    user = User.get_user(session['user_id'])
    list_job_user_adds = User.job_list_user_add(user.id)

    return render_template('dashboard.html', 
                            user = current_user, 
                            jobs = list_of_all_jobs, 
                            users_job = list_job_user_adds)


def new_user():
    return render_template('login.html')

#new user
def create_user():
    errors = User.register_validation(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect(url_for('users:new_user'))
    user_id = User.user_create(request.form)
    session['user_id'] = user_id
    return redirect(url_for('dashboard'))

#login
def login():
    valid, response = User.login_validation(request.form)
    if not valid:
        flash(response)
        return redirect(url_for('users:new_user'))
    session['user_id'] = response
    print(response)
    return redirect(url_for('dashboard'))

def logout():
    session.clear()
    return redirect(url_for('users:new_user'))



#dashboard
def jobs():
    current_user = User.query.get(session['user_id'])
    return render_template('create_job.html', user = current_user)

def job_add(id):
    User.add_job(id)
    return redirect(url_for('dashboard'))

def job_new():
    errors = Job.jobs_validation(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect('users:new_job')
    Job.job_add(request.form)
    return redirect(url_for('dashboard'))

def job_view(id):
    job_view = Job.job_view(id)
    current_user = User.query.get(session['user_id'])
    return render_template('job_view.html', user = current_user, job_view = job_view)

def job_edit_page(id):
    current_user = User.query.get(session['user_id'])
    job_view = Job.job_view(id)
    return render_template('job_edit.html', user = current_user, job_view = job_view)

def job_edit(id):
    errors = Job.jobs_validation(request.form)
    if errors:
        for error in errors:
            flash(error)
        return redirect(url_for('users:job_edit_page', id = id))
    Job.job_edit(request.form, id)
    return redirect(url_for('dashboard'))

def job_delete(id):
    Job.job_delete(id)
    return redirect(url_for('dashboard'))

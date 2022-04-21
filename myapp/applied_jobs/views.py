from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import AppliedJob
from myapp.applied_jobs.forms import AppliedJobForm

applied_jobs = Blueprint('applied_jobs', __name__)

@applied_jobs.route('/create', methods=['GET', 'POST'])
@login_required
def create_appliedjob():
    form = AppliedJobForm()
    if form.validate_on_submit():
        applied_job = AppliedJob(title=form.title.data, company=form.company.data, 
        date_applied = form.date_applied.data, accepted= form.accepted.data, in_process=form.in_process.data, rejected=form.rejected.data,
        user_id=current_user.id)
        db.session.add(applied_job)
        db.session.commit()
        flash('Job Post Created')
        print('Job post was created')
        return redirect(url_for('core.index'))
    return render_template('create_appliedjob.html', form=form)

# Make sure the blog_post_id is an integer!

@applied_jobs.route('/<int:applied_job_id>')
def applied_job(applied_job_id):
    applied_job = AppliedJob.query.get_or_404(applied_job_id) 
    return render_template('applied_job.html', title=applied_job.title, date=applied_job.date, job=applied_job_id)

@applied_jobs.route('/<int:applied_job_id>/update',methods=['GET','POST'])
@login_required
def update(applied_job_id):
    applied_job = AppliedJob.query.get_or_404(applied_job_id)

    if applied_job.author != current_user:
        abort(403)

    form = AppliedJobForm()

    if form.validate_on_submit():
        applied_job.title = form.title.data
        applied_job.company = form.company.data
        applied_job.accepted = form.accepted.data
        applied_job.in_process = form.in_process.data
        applied_job.rejected = form.rejected.data
        db.session.commit()
        flash('Applied job post Updated')
        return redirect(url_for('blog_posts.blog_post',blog_post_id=applied_job.id))

    elif request.method == 'GET':
        form.title.data = applied_job.title
        form.company.data = applied_job.company 
        form.accepted.data = applied_job.accepted 
        form.in_process.data = applied_job.in_process
        form.rejected.data = applied_job.rejected

    return render_template('create_appliedjob.html',title='Updating',form=form)

@applied_jobs.route('/<int:applied_job_id>/delete',methods=['GET','POST'])
@login_required
def delete_post(applied_job_id):

    applied_job = AppliedJob.query.get_or_404(applied_job_id)
    if applied_job.author != current_user:
        abort(403)

    db.session.delete(applied_job)
    db.session.commit()
    flash('Applied job post Deleted')
    return redirect(url_for('core.index'))
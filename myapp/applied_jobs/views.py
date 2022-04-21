from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import AppliedJob, BlogPost
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
    return render_template('create_post.html', form=form)

# Make sure the blog_post_id is an integer!

@applied_jobs.route('/<int:applied_job_id>')
def applied_job(applied_job_id):
    applied_job = AppliedJob.query.get_or_404(applied_job_id) 
    return render_template('applied_job.html', title=applied_job.title, date=applied_job.date, job=applied_job_id)
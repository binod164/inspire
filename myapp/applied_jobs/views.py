from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import AppliedJob, BlogPost
from myapp.applied_jobs.forms import AppliedJobForm

applied_jobs = Blueprint('applied_jobs', __name__)

@applied_jobs.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
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
# core/views.py 

from flask import render_template, request, Blueprint
from myapp import applied_jobs
from myapp.applied_jobs.views import applied_job
from myapp.models import AppliedJob

core = Blueprint('core', __name__)

@core.route('/profile')
def index():
    page = request.args.get('page', 1, type=int)
    applied_jobs = AppliedJob.query.order_by(AppliedJob.date.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', applied_jobs=applied_jobs)

@core.route('/info')
def info():
    return render_template('info.html')
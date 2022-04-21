from flask import render_template, url_for, flash, request, redirect, Blueprint, abort
from flask_login import current_user, login_required
from myapp import db 
from myapp.models import BlogPost
from myapp.applied_jobs.forms import AppliedJobForm

applied_jobs = Blueprint('applied_jobs', __name__)
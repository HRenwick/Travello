from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from . import db
from .models import Destination, Comment, User
from .forms import DestinationForm, CommentForm, RegisterForm, LoginForm
from flask_login import login_required, current_user

# Create Blueprint
destbp = Blueprint('destination', __name__, url_prefix='/destinations')

# Register Route: View Destination
@destbp.route('/<id>')
def show(id):
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    form = CommentForm()
    return render_template('destinations/show.html', destination=destination, form=form)

# Register Route: Create Destination
@destbp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    # Check User is Admin
    if current_user.user_type != 'admin':
          flash('This action requires administrator privileges.')
          return redirect(url_for('auth.login'))
    # Proceed as Normal
    form = DestinationForm()
    if form.validate_on_submit():
        db_file_path = check_file(form)
        destination = Destination(city_name=form.city_name.data, country_name=form.country_name.data, 
                                  description=form.description.data, image=db_file_path, 
                                  exchange_rate=form.exchange_rate.data, currency_code=form.currency_code.data)
        db.session.add(destination)
        db.session.commit()
        flash('Your destination was successfully created.')
        print(f"New destination created: '{form.city_name.data}, {form.country_name.data}'")
        return redirect(url_for('destination.show', id=destination.id))
    return render_template('destinations/create.html', form=form)
    
def check_file(form):
    img_file = form.image.data
    if img_file:
        filename = secure_filename(img_file.filename)
        base_path = os.path.dirname(__file__)
        upload_path = os.path.join(base_path, 'static/img', filename)
        db_upload_path = '/static/img/' + filename
        img_file.save(upload_path)
        return db_upload_path
    return None

# Register Route: Post Comment
@destbp.route('/<id>/comment', methods=['GET', 'POST'])
@login_required
def comment(id):
    form = CommentForm()
    destination = db.session.scalar(db.select(Destination).where(Destination.id==id))
    if form.validate_on_submit():
        comment = Comment(text=form.text.data, destination=destination, posted_by=current_user)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment was successfully posted.')
        print(f"New comment posted: '{form.text.data}'")
    return redirect(url_for('destination.show', id=id))
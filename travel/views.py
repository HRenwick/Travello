from flask import Blueprint, render_template, request, redirect, url_for, flash
from .models import Destination
from . import db

# Create Blueprint
mainbp = Blueprint('main', __name__)

# Register Route: Landing Page
@mainbp.route('/')
def index():
    destinations = db.session.scalars(db.select(Destination)).all()
    return render_template('index.html', destinations=destinations)

# Register Route: Search Bar
@mainbp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        query = "%" + request.args['search'] + "%"
        destination = db.session.scalars(db.select(Destination).where(Destination.description.ilike(query))).first()
        if destination:
            return redirect(url_for('destination.show', id=destination.id))
        else:
            flash('Sorry, no matching destination was found.')
            return redirect(url_for('main.index'))
    return redirect(url_for('main.index'))
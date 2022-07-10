from flask import Blueprint, render_template, request, redirect, url_for
from .models import Schemes, Areas, Steps, Methods, Paints
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        new_scheme = Schemes(scheme_name=request.form['name'], scheme_image=request.form['image'])
        db.session.add(new_scheme)
        db.session.commit()
        return redirect(url_for('views.home'))
    
    schemes = Schemes.query.all()

    return render_template("home.html", 
    schemes=schemes)

@views.route('/delete/<scheme_id>', methods=['POST'])
def delete_scheme(scheme_id):
    scheme = Schemes.query.filter_by(id=scheme_id).first()
    db.session.delete(scheme)
    db.session.commit()

    return redirect(url_for('views.home'))

@views.route('/scheme/<scheme_id>', methods=['GET'])
def get_scheme(scheme_id):
    scheme_id=scheme_id
    scheme_areas = Areas.query.filter_by(scheme_id=scheme_id).all()
    scheme = Schemes.query.get(scheme_id)
    steps = Steps.query.all()
    
    return render_template("scheme.html", 
    scheme_id=scheme_id, 
    scheme_areas=scheme_areas, 
    scheme=scheme, 
    steps=steps)

@views.route('/scheme/<scheme_id>/area/<area_id>', methods=['GET','POST'])
def set_area(scheme_id, area_id):

    paints = Paints.query.all()
    methods = Methods.query.all()
    area = Areas.query.filter_by(id=area_id).first()
    if request.method == 'POST':
        new_step = Steps(paint_id=request.form['paint'], method_id=request.form['method'], area_id=area_id)
        db.add(new_step)
        db.commit()
        return redirect(url_for('set_area', scheme_id=scheme_id, area_id=area_id))


    return render_template("edit_area.html", 
    area=area,
    paints=paints,
    methods=methods)

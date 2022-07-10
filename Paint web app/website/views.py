from flask import Blueprint, render_template, request, redirect, url_for
from .models import Schemes, Areas, Steps, Methods, Paints
from . import db

views = Blueprint('views', __name__)

#Bas-sida, visar alla schemes och tar emot post-request för att lägga till nya schemes
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

#Visar delar av ett visst scheme. Hanterar post-request för att lägga till nya delar.
@views.route('/scheme/<scheme_id>', methods=['GET', 'POST'])
def get_scheme(scheme_id):
    scheme_id=scheme_id
    scheme_areas = Areas.query.filter_by(scheme_id=scheme_id).all()
    scheme = Schemes.query.get(scheme_id)
    steps = Steps.query.all()

    if request.method == 'POST':
        new_area = Areas(area=request.form['name'], scheme_id=scheme_id)
        db.session.add(new_area)
        db.session.commit()
        return redirect(url_for('views.get_scheme', scheme_id=scheme_id))
    
    return render_template("scheme.html", 
    scheme_id=scheme_id, 
    scheme_areas=scheme_areas, 
    scheme=scheme, 
    steps=steps)

#Route för att hantera delete av schemes.
@views.route('/delete/<scheme_id>', methods=['POST'])
def delete_scheme(scheme_id):
    scheme = Schemes.query.filter_by(id=scheme_id).first()
    db.session.delete(scheme)
    db.session.commit()

    return redirect(url_for('views.home'))

#Visar alla steg i en del till ett scheme. Hanterar post-request för att lägga till nya steg.
@views.route('/scheme/<scheme_id>/area/<area_id>', methods=['GET','POST'])
def set_area(scheme_id, area_id):

    scheme=Schemes.query.filter_by(id=scheme_id).first()
    paints = Paints.query.all()
    methods = Methods.query.all()
    area = Areas.query.filter_by(id=area_id).first()
    steps = Steps.query.filter_by(area_id=area_id).all()
    if request.method == 'POST':
        new_step = Steps(paint_id=request.form['paint'], method_id=request.form['method'], area_id=area.id)
        db.session.add(new_step)
        db.session.commit()
        return redirect(url_for('views.set_area', scheme_id=scheme.id, area_id=area.id))

    return render_template("edit_area.html",
    scheme=scheme, 
    area=area,
    paints=paints,
    methods=methods,
    steps=steps)

#Hanterar delete av del till ett scheme. 
@views.route('/delete/<scheme_id>/area/<area_id>', methods=['POST'])
def delete_area(scheme_id, area_id):
    scheme_id=scheme_id
    area = Areas.query.filter_by(id=area_id).first()
    db.session.delete(area)
    db.session.commit()

    return redirect(url_for('views.get_scheme',scheme_id=scheme_id))

#Hanterar delete av ett steg till en del. 
@views.route('/delete/<scheme_id>/area/<area_id>/step/<step_id>', methods=['POST'])
def delete_step(scheme_id, area_id, step_id):
    scheme_id=scheme_id
    area_id=area_id
    step = Steps.query.filter_by(id=step_id).first()
    db.session.delete(step)
    db.session.commit()

    return redirect(url_for('views.set_area',scheme_id=scheme_id, area_id=area_id))

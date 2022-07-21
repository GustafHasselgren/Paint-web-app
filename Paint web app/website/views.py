from sre_constants import SUCCESS
from flask import Blueprint, render_template, request, redirect, url_for, flash
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
        flash('Scheme successfully added.')
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
        flash('Area successfully added.')
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
    flash('Scheme successfully deleted.')

    return redirect(url_for('views.home'))

#Visar alla steg i en del till ett scheme. Hanterar post-request för att lägga till nya steg.
@views.route('/scheme/<scheme_id>/area/<area_id>/color/<filter_color>', methods=['GET','POST'])
def set_area(scheme_id, area_id, filter_color):

    scheme=Schemes.query.filter_by(id=scheme_id).first()
    colors = Paints.query.with_entities(Paints.color).distinct()
    if filter_color == "No":
        paints = Paints.query.all()
    else:
        paints = Paints.query.filter_by(color=filter_color).all()
    
    types = Paints.query.with_entities(Paints.type).distinct()    
    methods = Methods.query.all()
    area = Areas.query.filter_by(id=area_id).first()
    steps = Steps.query.filter_by(area_id=area_id).all()
    if request.method == 'POST':
        
        if 'paint' in request.form and 'method' in request.form:
            new_step = Steps(paint_id=request.form['paint'], method_id=request.form['method'], area_id=area.id)
            db.session.add(new_step)
            db.session.commit()
            flash('Step successfully added.')
        else:
            filter_color = request.form['filter_color']

        return redirect(url_for('views.set_area', scheme_id=scheme.id, area_id=area.id, filter_color=filter_color))

    return render_template("edit_area.html",
    scheme=scheme, 
    area=area,
    paints=paints,
    methods=methods,
    steps=steps,
    colors = colors,
    types=types,
    filter_color=filter_color)

#Hanterar delete av del till ett scheme. 
@views.route('/delete/<scheme_id>/area/<area_id>', methods=['POST'])
def delete_area(scheme_id, area_id):
    scheme_id=scheme_id
    area = Areas.query.filter_by(id=area_id).first()
    db.session.delete(area)
    db.session.commit()
    flash('Area successfully deleted.')

    return redirect(url_for('views.get_scheme',scheme_id=scheme_id))

#Hanterar delete av ett steg till en del. 
@views.route('/delete/<scheme_id>/area/<area_id>/step/<step_id>/color/<filter_color>', methods=['POST'])
def delete_step(scheme_id, area_id, step_id, filter_color):
    scheme_id=scheme_id
    area_id=area_id
    filter_color=filter_color
    step = Steps.query.filter_by(id=step_id).first()
    db.session.delete(step)
    db.session.commit()
    flash('Step successfully deleted.')

    return redirect(url_for('views.set_area',scheme_id=scheme_id, area_id=area_id, filter_color=filter_color))

#Visar kompletta databasen över färger och metoder, och att lägga till till dessa.
@views.route('/manage', methods=['GET', 'POST'])
def manage():
    
    paints = Paints.query.all()
    methods = Methods.query.all()

    if request.method == 'POST':
        if request.form['paint']:
            new_paint = Paints(paint_name=request.form['paint'])
            db.session.add(new_paint)
            db.session.commit()
            flash('Paint successfully added.')
        if request.form['method']:
            new_method = Methods(method_name=request.form['method'])
            db.session.add(new_method)
            db.session.commit()
            flash('Method successfully added.')

        return redirect(url_for('views.manage'))
      

    return render_template('manage.html', paints=paints, methods=methods)

#Hanterar delete av färger.
@views.route('/delete/paint/<paint_id>/', methods=['POST'])
def delete_paint(paint_id):
    
    paint = Paints.query.filter_by(id=paint_id).first()
    db.session.delete(paint)
    db.session.commit()
    flash('Paint successfully deleted.')

    return redirect(url_for('views.manage'))

#Hanterar delete av metoder.
@views.route('/delete/method/<method_id>/', methods=['POST'])
def delete_method(method_id):
    
    method = Methods.query.filter_by(id=method_id).first()
    db.session.delete(method)
    db.session.commit()
    flash('Method successfully deleted.')

    return redirect(url_for('views.manage'))



    





from . import db


class Paints(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paint_name = db.Column(db.String(50), nullable=False)

class Areas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    area = db.Column(db.String(50), nullable=False)
    scheme_id = db.Column(db.Integer, db.ForeignKey('schemes.id'))

class Schemes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scheme_name = db.Column(db.String(50), nullable=False)
    scheme_image = db.Column(db.String(100))

    areas = db.relationship('Areas')
     
class Methods(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    method_name = db.Column(db.String(50), nullable=False)

class Steps(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    paint_id = db.Column(db.Integer, db.ForeignKey('paints.id'))
    area_id = db.Column(db.Integer, db.ForeignKey('areas.id'))
    method_id = db.Column(db.Integer, db.ForeignKey('methods.id'))

    paints = db.relationship('Paints')
    areas = db.relationship('Areas')
    methods = db.relationship('Methods')
    
   
    

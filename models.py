from app import db, ma, app
from marshmallow import fields

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(100), unique=True,)
    last_updated = db.Column(db.Date, nullable=False)

class Perscriber(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), unique=True,)
    position = db.Column(db.String(255), nullable=False)
    last_updated = db.Column(db.Date, nullable=False)
    
class Perscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    patient = db.relationship('Patient', backref='perscription')
    date = db.Column(db.Date, nullable=False)
    perscriber_id = db.Column(db.Integer, db.ForeignKey('perscriber.id'))
    perscriber = db.relationship('Perscriber', backref="perscription")
    medications = db.relationship("Medication", backref="perscription")

class Medication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_ndc = db.Column(db.String(50), nullable=False)
    dose = db.Column(db.Integer)
    frequency = db.Column(db.Integer)
    route = db.Column(db.String(100))
    duration = db.Column(db.Integer)
    repeat = db.Column(db.Boolean, default=False, nullable=False)
    repeat_review_date = db.Column(db.Date, nullable=True)
    perscription_id = db.Column(db.Integer, db.ForeignKey('perscription.id'))

class PatientSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Patient

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    last_updated = ma.auto_field()

class PerscriberSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Perscriber

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    position = ma.auto_field()
    last_updated = ma.auto_field()

class MedicationSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Medication
        include_relationships = True
        include_fk = True
    
    id = ma.auto_field()
    product_ndc = ma.auto_field()
    dose = ma.auto_field()
    frequency = ma.auto_field()
    route = ma.auto_field()
    duration = ma.auto_field()
    perscription_id = ma.auto_field()
    repeat = ma.auto_field()
    repeat_review_date = ma.auto_field()

class PerscriptionSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Perscription
        include_relationships = True
        include_fk = True

    id = ma.auto_field()
    patient_id = ma.auto_field()
    patient = fields.Nested(PatientSchema)
    date= ma.auto_field()
    perscriber_id = ma.auto_field()
    perscriber = fields.Nested(PerscriberSchema)
    medications = fields.List(fields.Nested(MedicationSchema))

with app.app_context():
    db.create_all()


from app import app, db
from flask import jsonify, request
from models import Patient, PatientSchema, Perscriber, PerscriberSchema, Perscription, PerscriptionSchema, Medication, MedicationSchema
from datetime import datetime, date

import ssl
ssl._create_default_https_context = ssl._create_unverified_context
from fdaapi import getMedicationData

@app.route('/', methods=['GET'])
def route():
    return 'working'

@app.route('/addPatient', methods=['POST'])
def addPatient():
    data = request.get_json()
    patient = Patient(name=data['name'], email=data['email'], last_updated=datetime.utcnow())
    db.session.add(patient)
    db.session.commit()
    return jsonify("User added")

@app.route('/addPerscriber', methods=['POST'])
def addPerscriber():
    data = request.get_json()
    print(data)
    perscriber = Perscriber(name=data['name'], email=data['email'], position=data['position'], last_updated=datetime.utcnow())
    db.session.add(perscriber)
    db.session.commit()
    return jsonify("Perscriber added")

@app.route('/addPerscription', methods=['POST'])
def addPersrciption():
    id = request.headers.get('id')
    data = request.get_json()
    medications = data['medication']
    listMeds = []
    script = Perscription(patient_id=data['patient_id'], perscriber_id=data['perscriber_id'], date=datetime.utcnow())
    listMeds.append(script)
    for medication in medications:
        if medication['repeat_review_date'] is not None:
            [year, month, day] = medication['repeat_review_date'].split("-")
            listMeds.append(Medication(product_ndc=medication['product_ndc'], dose=medication['dose'], frequency=medication['frequency'], route=medication['route'], duration=medication['duration'], repeat=medication['repeat'], repeat_review_date=date(int(year), int(month), int(day)), perscription=script))
        else:
            listMeds.append(Medication(product_ndc=medication['product_ndc'], dose=medication['dose'], frequency=medication['frequency'], route=medication['route'], duration=medication['duration'], repeat=medication['repeat'], perscription=script))
    db.session.add_all(listMeds)
    db.session.commit()
    return "Perscription Added"

@app.route('/list', methods=['GET'])
def list():
    patients = Patient.query.all()
    perscriber = Perscriber.query.all()
    patient_schema = PatientSchema(many=True)
    perscriber_schema = PerscriberSchema(many=True)
    perscriptions = Perscription.query.all()
    perscription_schema = PerscriptionSchema(many=True)
    
    return jsonify({"patients": patient_schema.dump(patients), "perscribers": perscriber_schema.dump(perscriber), "perscriptions": perscription_schema.dump(perscriptions)})

@app.route('/listPerscriptions', methods=['GET'])
def listPerscriptions():
    perscriptions = Perscription.query.all()
    perscription_schema = PerscriptionSchema(many=True)

    ser_perscriptions = perscription_schema.dump(perscriptions)

    for perscription in ser_perscriptions:
        medications = perscription['medications']
        for medication in medications:
            med_data = getMedicationData(medication['product_ndc'])
            
            if isinstance(med_data, dict):
                medication['medication_data'] = med_data
            else:
                return med_data
            
    return ser_perscriptions


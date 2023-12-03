from flask import Flask, render_template, request, redirect, url_for, abort, jsonify, make_response
from sqlalchemy import distinct
from datetime import datetime
from config import db
from models.criminal import Criminal
from models.alias import Alias
from models.address import Address
from models.criminal_phone import CriminalPhone
from models.officer_phone import OfficerPhone
from models.crime import Crime
from models.sentences import Sentence
from models.charge import Charge
from models.appeal import Appeal
from models.officer import Officer
from models.crime_officer import CrimeOfficer

app = Flask(__name__)
DB_GUEST_URI = 'mysql+pymysql://guestuser:@localhost:3306/project'
DB_MAIN_URI = 'mysql+pymysql://root:@localhost:3306/project'

app.config['SQLALCHEMY_DATABASE_URI'] = DB_MAIN_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
db.init_app(app)

def set_guest():
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_GUEST_URI

def set_admin():
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_MAIN_URI

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/criminals')
def list_of_criminals():
    criminals = Criminal.query.all()
    return render_template('criminals.html', criminals=criminals)

@app.route('/officers/')
def list_of_officers():
    officers = Officer.query.all()
    return render_template('officers.html', officers=officers)

@app.route('/charges/')
def list_of_charges():
    charges = Charge.query.all()
    return render_template('charges.html', charges=charges)

@app.route('/appeals', methods=['POST'])
def add_appeal():
    data = request.get_json()

    # make sure crime exists
    crime_id = data['crime_id']
    crime = Crime.query.get(crime_id)
    if crime is None:
        return make_response(jsonify({'message': 'No crime found with this ID'}), 404)

    new_appeal = Appeal( 
        crime_id=crime_id, 
        filing_date=data['filing_date'], 
        hearing_date=data['hearing_date'], 
        appeal_status=data['appeal_status']
    )

    db.session.add(new_appeal)
    db.session.commit()

    return make_response(jsonify({'message': 'Appeal has been created'}), 200)
    
@app.route('/sentences', methods=['POST'])
def add_sentence():
    data = request.get_json()

    # make sure criminal exists
    criminal_id = data['criminal_id']
    criminal = Criminal.query.get(criminal_id)
    if criminal is None:
        return make_response(jsonify({'message': 'No criminal found with this ID'}), 404)

    new_sentence = Sentence( 
        criminal_id=criminal_id, 
        start_date=data['start_date'], 
        end_date=data['end_date'], 
        num_violations=data['num_violations'],
        type=data['type']
    )

    db.session.add(new_sentence)
    db.session.commit()

    return make_response(jsonify({'message': 'Sentence has been created'}), 200)
    
@app.route('/crimes', methods=['POST'])
def create_crime():
    data = request.get_json()
    
    new_crime = Crime(
        criminal_id=data['criminal_id'],
        fine=data['fine'],
        amount_paid=data['amount_paid'],
        payment_due_date=data['payment_due_date'],
        court_fee=data['court_fee']
    )
    
    try:
        db.session.add(new_crime)
        db.session.commit()

        # add charges associated with the crime
        charges = Charge.query.all()

        # dictionary where each charge_code maps to its classification
        charge_classifications = {charge.charge_code: charge.classification for charge in charges}

        for charge_code in data['charge_codes']:
            new_charge = Charge(charge_code=charge_code, crime_id=new_crime.crime_id, classification=charge_classifications[int(charge_code)])
            db.session.add(new_charge)

        db.session.commit()
        return jsonify(message='New crime and associated charges created'), 201

    except Exception as e:
        # rollback the transaction
        db.session.rollback()
        return jsonify(message=str(e)), 400


@app.route('/criminal/<int:id>', methods=['GET', 'POST', 'DELETE'])
def get_criminal(id):
    criminal = Criminal.query.get(id)
    if not criminal:
        abort(404, description="No criminal found with the provided ID.")    
    if request.method == 'POST':
        # add user authentication before proceeding

        # updating name
        if 'name' in request.form:
            criminal.name = request.form['name']
        
        # updating an alias
        if request.form['alias_select'] and ('delete_alias' in request.form or request.form['alias']):
            alias = Alias.query.get((request.form['alias_select'], id))
            if alias:
                if 'delete_alias' in request.form:
                    db.session.delete(alias)
                else:
                    new_alias = request.form['alias']
                    # make sure user provided an alias and its unique
                    if new_alias and Alias.query.filter_by(alias_name=new_alias, criminal_id=id).first() is None:
                        alias.alias_name = new_alias
                    else:
                        print('alias not unique or its empty')
            else:
                print('alias not found')
        
        # adding a new alias
        if request.form['add_alias']:
            alias_name = request.form.get('add_alias')
            # make sure its unique
            if Alias.query.filter_by(alias_name=alias_name, criminal_id=id).first() is None:
                new_alias = Alias(alias_name=alias_name, criminal_id=id)
                db.session.add(new_alias)
            else:
                print('alias is not unique')


        # updating an address
        if request.form['address_select'] and ('delete_address' in request.form or request.form['street_address']):
            selected_address = request.form['address_select'].split(', ')
            street_address, city, state, zip_code = selected_address[0], selected_address[1], selected_address[2], int(selected_address[3])
            address = Address.query.get((id, street_address, zip_code))
    
            if address:
                if 'delete_address' in request.form:
                    db.session.delete(address)
                else:
                    new_street_address = request.form['street_address']
                    new_city = request.form['city']
                    new_state = request.form['state']
                    new_zip_code = request.form['zip_code']
                    # PKs are provided and are unique
                    if new_street_address and new_city and new_state and new_zip_code and Address.query.filter_by(criminal_id=id, street_address=new_street_address, zip_code=new_zip_code).first() is None:
                        address.street_address = new_street_address
                        address.city = new_city
                        address.state = new_state
                        address.zip_code = new_zip_code
                    else:
                        print("Address not unique or empty")
            else:
                print("Address not found in the database")

        # adding a new address
        if request.form['add_address']:
            new_address = request.form['add_address'].split(', ')
            street_address, city, state, zip_code = new_address[0], new_address[1], new_address[2], int(new_address[3])
            if Address.query.filter_by(street_address=street_address, criminal_id=id, zip_code=zip_code).first() is None:
                address = Address(criminal_id=id, street_address=street_address, city=city, state=state, zip_code=zip_code)
                db.session.add(address)
            else:
                print("Address not unique")

        # updating phone
        if request.form['phone_select'] and ('delete_phone' in request.form or request.form['phone']):
            phone = CriminalPhone.query.get((id, request.form['phone_select']))
            if phone:
                if 'delete_phone' in request.form:
                    db.session.delete(phone)
                else:
                    new_phone = request.form['phone']
                    # phone number is given and unique
                    if new_phone and CriminalPhone.query.filter_by(c_phone_number=new_phone, criminal_id=id).first() is None:
                        phone.c_phone_number = new_phone
                    else:
                        print('phone not unique or empty')
            else:
                print('phone not found')

        # adding a new phone
        if request.form['add_phone']:
            new_phone = request.form['add_phone']
            if CriminalPhone.query.filter_by(c_phone_number=new_phone, criminal_id=id).first() is None:
                phone = CriminalPhone(c_phone_number=new_phone, criminal_id=id)
                db.session.add(phone)
            else:
                print("Phone not unique")

        db.session.commit()
        return redirect(url_for('get_criminal', id=id))
    elif request.method == 'DELETE':
        db.session.delete(criminal)
        db.session.commit()
        return make_response(jsonify({'message': 'Criminal has been deleted'}), 200)
    else: # GET request
        # get all unique charge codes
        charges = Charge.query.with_entities(Charge.charge_code, Charge.classification).distinct().all()        
        crimes = Crime.query.filter_by(criminal_id=id).all()
        sentences = Sentence.query.filter_by(criminal_id=id).all()
        now = datetime.now().strftime('%Y-%m-%d')
        return render_template('criminal.html', criminal=criminal, crimes=crimes, sentences=sentences, now=now, charges=charges)
    
@app.route('/crime/<int:id>', methods=['GET', 'POST', 'DELETE'])
def get_crime(id):
    crime = Crime.query.get(id)
    if crime is None:
        abort(404, description="No crime found with the provided ID.")
    if request.method == 'POST':
        # add user authentication before proceeding

        # update the fine
        if 'fine' in request.form and request.form['fine']:
            crime.fine = request.form['fine']
        
        # update the amount paid
        if 'amount_paid' in request.form and request.form['amount_paid']:
            crime.amount_paid = request.form['amount_paid']

        # update the payment due date
        if 'payment_due_date' in request.form and request.form['payment_due_date']:
            crime.payment_due_date = request.form['payment_due_date']

        # update the court fee
        if 'court_fee' in request.form and request.form['court_fee']:
            crime.court_fee = request.form['court_fee']

        db.session.commit()
        return redirect(url_for('get_crime', id=id))
    
    elif request.method == 'DELETE':
        db.session.delete(crime)
        db.session.commit()
        return make_response(jsonify({'message': 'Crime has been deleted'}), 200)
    
    else:
        charges = Charge.query.filter_by(crime_id=id).all()
        charge_codes = [str(charge.charge_code) for charge in charges]
        appeals = Appeal.query.filter_by(crime_id=id).all()
        crime_officers = CrimeOfficer.query.filter_by(crime_id=id).all()  # query for officers associated with the crime
        officers = [crime_officer.officer for crime_officer in crime_officers]  # get the Officer objects
        criminal = crime.criminal
        now = datetime.now().strftime('%Y-%m-%d')
        return render_template('crime.html', crime=crime, charge_codes=charge_codes, appeals=appeals, officers=officers, criminal=criminal, now=now)

@app.route('/appeal/<int:id>', methods=['GET', 'POST'])
def get_appeal(id):
    appeals = Appeal.query.get(id)
    if appeals is None:
        abort(404, description="No appeal found with the provided ID.")
    if request.method == 'POST':
        # add user authentication before proceeding

        # update the appeal status
        if 'appeal_status' in request.form and request.form['appeal_status']:
            appeals.appeal_status = request.form['appeal_status']

        # update the hearing date
        if 'hearing_date' in request.form and request.form['hearing_date']:
            appeals.hearing_date = request.form['hearing_date']

        # update the filing date
        if 'filing_date' in request.form and request.form['filing_date']:
            appeals.filing_date = request.form['filing_date']

        db.session.commit()
        return redirect(url_for('get_appeal', id=id))
    else:
        criminal = appeals.crime.criminal
        return render_template('appeal.html', appeal=appeals, criminal=criminal)

@app.route('/sentence/<int:id>', methods=['GET', 'POST', 'DELETE'])
def get_sentence(id):
    sentence = Sentence.query.get(id)
    if not sentence:
        abort(404, description="No sentence found with the provided ID.")
    if request.method == 'POST':
        # add user authentication before proceeding

        # update the start date
        if 'start_date' in request.form and request.form['start_date']:
            sentence.start_date = request.form['start_date']

        # update the end date
        if 'end_date' in request.form and request.form['end_date']:
            sentence.end_date = request.form['end_date']

        # update the type
        if 'type' in request.form and request.form['type']:
            sentence.type = request.form['type']

        # update the num violations
        if 'num_violations' in request.form and request.form['num_violations']:
            sentence.num_violations = request.form['num_violations']

        db.session.commit()
        return redirect(url_for('get_sentence', id=id))
    elif request.method == 'DELETE':
        db.session.delete(sentence)
        db.session.commit()
        return make_response(jsonify({'message': 'Sentence has been deleted'}), 200)
    else:
        criminal = sentence.criminal
        return render_template('sentence.html', sentence=sentence, criminal=criminal)

@app.route('/charge/<int:id>', methods=['GET'])
def get_charges(id):
    charge = Charge.query.filter_by(charge_code=id).first()
    charges = Charge.query.filter_by(charge_code=id).all()
    crimes = [crime.crime for crime in charges]
    if not charges:
        abort(404, description="No charge found with the provided ID.")
    return render_template('charge.html', charge=charge, crimes=crimes)
    
@app.route('/officer/<int:id>', methods=['GET', 'POST', 'DELETE'])
def get_officer(id):
    officer = Officer.query.get(id)
    if not officer:
        abort(404, description="No officer found with the provided ID.")
    if request.method == 'POST':
        print(request.form)
        # updating name
        if 'name' in request.form:
            officer.name = request.form['name']
        # updating precinct
        if 'precinct' in request.form:
            officer.precinct = request.form['precinct']
        # updating status
        if 'status' in request.form:
            officer.status = True
        else:
            officer.status = False
        # updating phone
        if 'phone_select' in request.form:
            phone = OfficerPhone.query.get((id, request.form['phone_select']))
            if phone:
                if 'delete_phone' in request.form:
                    db.session.delete(phone)
                else:
                    new_phone = request.form['phone']
                    # phone number is given and unique
                    if new_phone and OfficerPhone.query.filter_by(o_phone_number=new_phone, badge_no=id).first() is None:
                        phone.o_phone_number = new_phone
                    else:
                        print('phone not unique or empty')
        
        # adding a new phone
        if request.form['add_phone']:
            new_phone = request.form['add_phone']
            if OfficerPhone.query.filter_by(o_phone_number=new_phone, badge_no=id).first() is None:
                phone = OfficerPhone(o_phone_number=new_phone, badge_no=id)
                db.session.add(phone)
            else:
                print("Phone not unique")
        db.session.commit()
        return redirect(url_for('get_officer', id=id))
    
    elif request.method == 'DELETE':
        db.session.delete(officer)
        db.session.commit()
        return make_response(jsonify({'message': 'Officer has been deleted'}), 200)
    else:
        return render_template('officer.html', officer=officer)


if __name__ == '__main__':
    app.run(debug=True, port='3000')
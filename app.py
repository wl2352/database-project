from flask import Flask, render_template, request, redirect, url_for, abort
from config import db
from models.criminal import Criminal
from models.alias import Alias
from models.address import Address
from models.criminal_phone import CriminalPhone
from models.crime import Crime
from models.sentences import Sentence


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/project'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # silence the deprecation warning
db.init_app(app)


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

@app.route('/criminal/<int:id>', methods=['GET', 'POST'])
def get_criminal(id):
    if request.method == 'POST':
        # add user authentication before proceeding
        criminal = Criminal.query.get(id)
        if not criminal:
            return 'Criminal not found', 404

        # updating name
        if 'name' in request.form:
            criminal.name = request.form['name']
        
        # updating an alias
        if 'alias_select' in request.form:
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
                        print('alias not unique or empty')
            else:
                print('alias not found')

        # updating an address
        if 'address_select' in request.form:
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

        # updating phone
        if 'phone_select' in request.form:
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

        db.session.commit()
        return redirect(url_for('get_criminal', id=id))

    else: # GET request
        criminal = Criminal.query.get(id)
        if criminal is None:
            abort(404, description="No criminal found with the provided ID.")
        crimes = Crime.query.filter_by(criminal_id=id).all()
        sentences = Sentence.query.filter_by(criminal_id=id).all()
        return render_template('criminal.html', criminal=criminal, crimes=crimes, sentences=sentences)
    
@app.route('/crime/<int:id>', methods=['GET', 'POST'])
def get_crime(id):
    if request.method == 'POST':
        # add user authentication before proceeding
        crime = Crime.query.get(id)
        if not crime:
            return 'Crime not found', 404

        # update the fine
        if 'fine' in request.form:
            crime.fine = request.form['fine']
        
        # update the amount paid
        if 'amount_paid' in request.form:
            crime.amount_paid = request.form['amount_paid']

        # update the payment due date
        if 'payment_due_date' in request.form:
            crime.payment_due_date = request.form['payment_due_date']

        # update the court fee
        if 'court_fee' in request.form:
            crime.court_fee = request.form['court_fee']

        db.session.commit()
        return redirect(url_for('get_crime', id=id))
    else:
        crime = Crime.query.get(id)
        if crime is None:
            abort(404, description="No crime found with the provided ID.")
        return render_template('crime.html', crime=crime)

if __name__ == '__main__':
    app.run(debug=True, port='3000')
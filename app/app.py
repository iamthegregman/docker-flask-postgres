import time
import sys
import os
import traceback
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy import text
from datetime import datetime

# Import configuration
from config import config

# Determine which config to use based on environment
config_name = os.getenv('FLASK_ENV', 'development')
app_config = config.get(config_name, config['default'])

app = Flask(__name__)
app.config.from_object(app_config)

db = SQLAlchemy(app)


class Acceptance(db.Model):
    __tablename__ = 'rdb_v3_tbl_acceptance_testing'
    
    accept_code = db.Column(db.Integer, primary_key=True)
    acceptance_criteria = db.Column(db.String(250))
    
    def __repr__(self):
        return f'<Acceptance {self.acceptance_criteria}>'

class Locations(db.Model):
    __tablename__ = 'rdb_v3_tbl_locations'
    
    location_id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(250))
    
    def __repr__(self):
        return f'<Location {self.location}>'

# Reagent Type Model
class ReagentType(db.Model):
    __tablename__ = 'rdb_v3_tbl_reagent_types'
    
    reagent_type_id = db.Column(db.Integer, primary_key=True)
    reagent_type = db.Column(db.String(255))
    
    def __repr__(self):
        return f'<ReagentType {self.reagent_type}>'

# Reagent Model
class Reagent(db.Model):
    __tablename__ = 'rdb_v3_tbl_reagents'
    
    reagent_id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(255))
    reagent_name = db.Column(db.String(255))
    stability = db.Column(db.Integer)
    disc = db.Column(db.Boolean)
    entered_by = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_users.user_id'))
    min_stock = db.Column(db.Integer)
    current_stock = db.Column(db.Integer)
    cs_deplete = db.Column(db.Boolean)
    mandatory = db.Column(db.Boolean)
    reagent_type = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_reagent_types.reagent_type_id'))
    
    # Relationships
    lots = db.relationship('ReagentLot', backref='reagent', lazy=True)
    reagent_type_info = db.relationship('ReagentType', foreign_keys=[reagent_type])

    def __repr__(self):
        return f'<Reagent {self.reagent_name}>'

# Reagent Lot Model
class ReagentLot(db.Model):
    __tablename__ = 'rdb_v3_tbl_reagent_lots'
    
    reagent_lot_id = db.Column(db.Integer, primary_key=True)
    reagent_id = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_reagents.reagent_id'))
    prep_rec_date = db.Column(db.Date)
    prep_user = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_users.user_id'))
    lot_no = db.Column(db.String(50))
    barcode_r = db.Column(db.String(255))
    exp_date = db.Column(db.Date)
    in_use_from_date = db.Column(db.Date)
    in_use_to_date = db.Column(db.Date)
    disc_date = db.Column(db.Date)
    comment = db.Column(db.String(255))
    tested_date = db.Column(db.Date)
    acceptance = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_acceptance_testing.accept_code'))
    accept_user = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_users.user_id'))
    remedial = db.Column(db.String(255))
    location = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_locations.location_id'))
    
    # Relationships
    acceptance_info = db.relationship('Acceptance', backref='reagent_lots', lazy=True)
    prep_user_info = db.relationship('Users', foreign_keys=[prep_user], backref='prepared_reagent_lots', lazy=True)
    accept_user_info = db.relationship('Users', foreign_keys=[accept_user], backref='accepted_reagent_lots', lazy=True)
    location_info = db.relationship('Locations', backref='reagent_lots', lazy=True)

    def __repr__(self):
        return f'<ReagentLot {self.lot_no}>'

# Define models for SQL here (probably want to move this into a separate file at some point)
class Supplies(db.Model):
    __tablename__ = 'rdb_v3_tbl_supplies'
    
    supply_id = db.Column(db.Integer, primary_key=True)
    supply_name = db.Column(db.String(250))
    manufacturer = db.Column(db.String(50))
    product = db.Column(db.String(50))
    cas = db.Column(db.String(255))
    type = db.Column(db.String(50))
    grade = db.Column(db.String(50))
    purity_quant = db.Column(db.String(50))
    storage_temp = db.Column(db.String(50))
    stability = db.Column(db.String(50))
    comment = db.Column(db.String(250))
    min_stock = db.Column(db.Integer)
    supply_current_stock = db.Column(db.Integer)
    one_shot = db.Column(db.Boolean)
    
    # Relationship with lots
    lots = db.relationship('SuppliesLots', backref='supply', lazy=True)
    
    def __repr__(self):
        return f'<Supply {self.supply_name}>'

class SuppliesLots(db.Model):
    __tablename__ = 'rdb_v3_tbl_supplies_lots'
    
    supply_lot_id = db.Column(db.Integer, primary_key=True)
    supply_id = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_supplies.supply_id'))
    lot_no = db.Column(db.String(50))
    barcode_s = db.Column(db.String(255))
    quant = db.Column(db.String(50))
    condition = db.Column(db.Boolean)
    use_by_date = db.Column(db.Date)
    rec_date = db.Column(db.Date)
    open_date = db.Column(db.Date)
    disc_date = db.Column(db.Date)
    comment = db.Column(db.String(250))
    accept = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_acceptance_testing.accept_code'))
    entered_by = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_users.user_id'))
    location = db.Column(db.Integer, db.ForeignKey('rdb_v3_tbl_locations.location_id'))

    # Relationships
    acceptance_info = db.relationship('Acceptance', backref='supplies_lots', lazy=True)
    location_info = db.relationship('Locations', backref='supplies_lots', lazy=True) 
    entered_by_user = db.relationship('Users', backref='entered_supplies_lots', lazy=True)
    
    def __repr__(self):
        return f'<SupplyLot {self.lot_no}>'

# Users Model (placeholder - adjust based on your actual users table structure)
class Users(db.Model):
    __tablename__ = 'rdb_v3_tbl_users'
    
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    # Add other fields as needed
    
    def __repr__(self):
        return f'<User {self.username}>'

def database_initialization_sequence():
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully")
                
    except Exception as e:
        print("ERROR in database_initialization_sequence: {}".format(e))
        print(traceback.format_exc())
        with app.app_context():
            db.session.rollback()

@app.route('/')
def index():
    return redirect(url_for('supplies'))

@app.route('/reagents')
def reagents():
    try:
        # Get sort parameters from query string (similar to supplies)
        sort_by = request.args.get('sort_by', 'reagent_name')
        sort_dir = request.args.get('sort_dir', 'asc')
        
        if sort_dir == 'desc':
            order = db.desc(getattr(Reagent, sort_by))
        else:
            order = db.asc(getattr(Reagent, sort_by))
        
        reagents_list = Reagent.query.order_by(order).all()
        return render_template('reagents.html', 
                              reagents=reagents_list,
                              sort_by=sort_by,
                              sort_dir=sort_dir)
    except Exception as e:
        error_msg = "ERROR retrieving reagents: {}".format(e)
        print(error_msg)
        print(traceback.format_exc())
        flash(error_msg, 'error')
        return render_template('reagents.html', reagents=[], error=error_msg)

@app.route('/reagent/<int:reagent_id>')
def reagent_detail(reagent_id):
    try:
        reagent = Reagent.query.get_or_404(reagent_id)
        lots = ReagentLot.query.filter_by(reagent_id=reagent_id).order_by(ReagentLot.reagent_lot_id.desc()).all()
        locations = Locations.query.order_by(Locations.location).all()
        reagent_types = ReagentType.query.order_by(ReagentType.reagent_type).all()
        acceptance_codes = Acceptance.query.all()

        now = datetime.now().date()
        
        return render_template('reagent_detail.html', 
                              reagent=reagent, 
                              lots=lots,
                              locations=locations,
                              reagent_types=reagent_types,
                              acceptance_codes=acceptance_codes,
                              now=now)
    except Exception as e:
        error_msg = "ERROR retrieving reagent details: {}".format(e)
        print(error_msg)
        print(traceback.format_exc())
        flash(error_msg, 'error')
        return redirect(url_for('reagents'))

@app.route('/reagent_types')
def reagent_types():
    try:
        types_list = ReagentType.query.order_by(ReagentType.reagent_type).all()
        return render_template('reagent_types.html', types=types_list)
    except Exception as e:
        error_msg = "ERROR retrieving reagent types: {}".format(e)
        print(error_msg)
        print(traceback.format_exc())
        flash(error_msg, 'error')
        return render_template('reagent_types.html', types=[], error=error_msg)

@app.route('/supplies')
def supplies():
    try:
        # Get sort parameters from query string
        sort_by = request.args.get('sort_by', 'supply_name')  # Default sort by name
        sort_dir = request.args.get('sort_dir', 'asc')  # Default ascending
        # Construct sort query based on parameters
        if sort_dir == 'desc':
            order = db.desc(getattr(Supplies, sort_by))
        else:
            order = db.asc(getattr(Supplies, sort_by))
        
        supplies_list = Supplies.query.order_by(order).all()
        return render_template('supplies.html', 
                              supplies=supplies_list,
                              sort_by=sort_by,
                              sort_dir=sort_dir)
    except Exception as e:
        error_msg = "ERROR retrieving supplies: {}".format(e)
        print(error_msg)
        print(traceback.format_exc())
        flash(error_msg, 'error')
        return render_template('supplies.html', supplies=[], error=error_msg)

@app.route('/supply/<int:supply_id>')
def supply_detail(supply_id):
    try:
        supply = Supplies.query.get_or_404(supply_id)
        lots = SuppliesLots.query.filter_by(supply_id=supply_id).order_by(SuppliesLots.supply_lot_id.desc()).all()
        locations = Locations.query.order_by(Locations.location).all()
        acceptance_codes = Acceptance.query.all()
        return render_template('supply_detail.html', 
                              supply=supply, 
                              lots=lots,
                              locations=locations,
                              acceptance_codes=acceptance_codes)
    except Exception as e:
        error_msg = "ERROR retrieving supply details: {}".format(e)
        print(error_msg)
        print(traceback.format_exc())
        flash(error_msg, 'error')
        return redirect(url_for('supplies'))

@app.route('/locations')
def locations():
    try:
        locations_list = Locations.query.order_by(Locations.location).all()
        return render_template('locations.html', locations=locations_list)
    except Exception as e:
        error_msg = "ERROR retrieving locations: {}".format(e)
        print(error_msg)
        print(traceback.format_exc())
        flash(error_msg, 'error')
        return render_template('locations.html', locations=[], error=error_msg)

@app.route('/location/add', methods=['GET', 'POST'])
def add_location():
    # For now, just redirect to locations page
    # You can implement the full functionality later
    flash('Location add feature coming soon!', 'info')
    return redirect(url_for('locations'))

#bootstrap elements for looking some of the elements that can be used
@app.route('/bootstrap_elements')
def bootstrap_elements():
    return render_template('bootstrap_elements.html')

def test_db_connection():
    """Test database connection and print diagnostic information"""
    print("\n=== DATABASE CONNECTION TEST ===")
    print(f"Attempting to connect to: {app_config.DBHOST}:{app_config.DBPORT}")
    print(f"Database: {app_config.DBNAME}")
    print(f"Username: {app_config.DBUSER}")
    
    try:
        # Test raw connection
        from sqlalchemy import create_engine, text
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        connection = engine.connect()
        connection.close()
        print("✅ Basic connection successful!")
        
        # Get PostgreSQL version (with application context)
        with app.app_context():
            result = db.session.execute(text("SELECT version();")).fetchone()
            print(f"PostgreSQL Version: {result[0]}")
            
            # Test table creation
            db.create_all()
            print("✅ Table creation successful!")
        
        return True
    except exc.OperationalError as e:
        print("❌ OPERATIONAL ERROR: {}".format(e))
        print("This typically indicates connection problems (wrong host, port, credentials, etc.)")
        return False
    except exc.ProgrammingError as e:
        print("❌ PROGRAMMING ERROR: {}".format(e))
        print("This typically indicates SQL syntax errors or permission issues")
        return False
    except Exception as e:
        print("❌ UNEXPECTED ERROR: {}".format(e))
        print(traceback.format_exc())
        return False
    finally:
        print("=== END DATABASE CONNECTION TEST ===\n")
        
if __name__ == '__main__':
    print("\n=== STARTING APPLICATION ===")
    print(f"Environment: {config_name}")
    print(f"Debug mode: {app.config['DEBUG']}")
    
    # Multiple connection attempts with detailed error reporting
    dbstatus = False
    retries = 0
    max_retries = 5
    
    while dbstatus == False and retries < max_retries:
        print(f"\nAttempt {retries+1}/{max_retries} to connect to database...")
        try:
            dbstatus = test_db_connection()
            if not dbstatus:
                raise Exception("Connection test failed")
                
        except Exception as e:
            retries += 1
            print(f"ERROR connecting to database: {e}")
            if retries < max_retries:
                wait_time = 5
                print(f"Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
            else:
                print("Maximum retries reached. Giving up.")
    
    if dbstatus:
        print("\n✅ Successfully connected to database")
        print("Initializing database...")
        database_initialization_sequence()
        print("\n=== STARTING FLASK SERVER ===")
        app.run(debug=app.config['DEBUG'], host='0.0.0.0')
    else:
        print("\n❌ FATAL: Could not establish database connection after multiple attempts")
        print("Application will not start")
        sys.exit(1)
import time
import sys
import traceback
from flask import Flask, render_template, flash, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from sqlalchemy import text
from datetime import datetime

DBUSER = 'marco'
DBPASS = 'foobarbaz'
DBHOST = 'db'
DBPORT = '5432'
DBNAME = 'testdb'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=DBUSER,
        passwd=DBPASS,
        host=DBHOST,
        port=DBPORT,
        db=DBNAME)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'foobarbaz'

db = SQLAlchemy(app)

# Define models directly in app.py since you're importing them here
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
    accept = db.Column(db.Integer)
    entered_by = db.Column(db.Integer)
    location = db.Column(db.Integer)
    
    def __repr__(self):
        return f'<SupplyLot {self.lot_no}>'

# Keep the students model for backward compatibility
class students(db.Model):
    id = db.Column('student_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    city = db.Column(db.String(50))
    addr = db.Column(db.String(200))

    def __init__(self, name, city, addr):
        self.name = name
        self.city = city
        self.addr = addr

def database_initialization_sequence():
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully")
            
            # Original student initialization kept for compatibility
            existing = students.query.filter_by(name='John Doe').first()
            if not existing:
                test_rec = students(
                        'John Doe',
                        'Los Angeles',
                        '123 Foobar Ave')
                db.session.add(test_rec)
                db.session.commit()
                print("Test record added successfully")
            else:
                print("Test record already exists, skipping")
                
    except Exception as e:
        print("ERROR in database_initialization_sequence: {}".format(e))
        print(traceback.format_exc())
        with app.app_context():
            db.session.rollback()

@app.route('/')
def index():
    return redirect(url_for('supplies'))

@app.route('/supplies')
def supplies():
    try:
        supplies_list = Supplies.query.order_by(Supplies.supply_name).all()
        return render_template('supplies.html', supplies=supplies_list)
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
        lots = SuppliesLots.query.filter_by(supply_id=supply_id).all()
        return render_template('supply_detail.html', supply=supply, lots=lots)
    except Exception as e:
        error_msg = "ERROR retrieving supply details: {}".format(e)
        print(error_msg)
        print(traceback.format_exc())
        flash(error_msg, 'error')
        return redirect(url_for('supplies'))

# Legacy route preserved for compatibility
@app.route('/students', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        if not request.form['name'] or not request.form['city'] or not request.form['addr']:
            flash('Please enter all the fields', 'error')
        else:
            student = students(
                    request.form['name'],
                    request.form['city'],
                    request.form['addr'])

            db.session.add(student)
            db.session.commit()
            flash('Record was succesfully added')
            return redirect(url_for('home'))
    
    try:
        all_students = students.query.all()
        return render_template('show_all.html', students=all_students)
    except Exception as e:
        error_msg = "ERROR retrieving students: {}".format(e)
        print(error_msg)
        flash(error_msg, 'error')
        return render_template('show_all.html', students=[], error=error_msg)

def test_db_connection():
    """Test database connection and print diagnostic information"""
    print("\n=== DATABASE CONNECTION TEST ===")
    print("Attempting to connect to: {}:{}".format(DBHOST, DBPORT))
    print("Database: {}".format(DBNAME))
    print("Username: {}".format(DBUSER))
    
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
            print("PostgreSQL Version: {}".format(result[0]))
            
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
    
    # Multiple connection attempts with detailed error reporting
    dbstatus = False
    retries = 0
    max_retries = 5
    
    while dbstatus == False and retries < max_retries:
        print("\nAttempt {}/{} to connect to database...".format(retries+1, max_retries))
        try:
            # Test connection more thoroughly
            dbstatus = test_db_connection()
            if not dbstatus:
                raise Exception("Connection test failed")
                
        except Exception as e:
            retries += 1
            print("ERROR connecting to database: {}".format(e))
            if retries < max_retries:
                wait_time = 5
                print("Waiting {} seconds before retrying...".format(wait_time))
                time.sleep(wait_time)
            else:
                print("Maximum retries reached. Giving up.")
    
    if dbstatus:
        print("\n✅ Successfully connected to database")
        print("Initializing database...")
        database_initialization_sequence()
        print("\n=== STARTING FLASK SERVER ===")
        app.run(debug=True, host='0.0.0.0')
    else:
        print("\n❌ FATAL: Could not establish database connection after multiple attempts")
        print("Application will not start")
        sys.exit(1)
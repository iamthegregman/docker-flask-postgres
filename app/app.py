import time
import sys
import os
import traceback
from flask import Flask, jsonify, render_template, flash, redirect, request, url_for
from sqlalchemy import exc
from sqlalchemy import text
from datetime import datetime

# Import configuration
from config import config

# Import models and database
from models import db, Acceptance, Locations, ReagentType, Reagent, ReagentLot, Supplies, SuppliesLots, Users, QCData, ScannerTest


# Determine which config to use based on environment
config_name = os.getenv('FLASK_ENV', 'development')
app_config = config.get(config_name, config['default'])

app = Flask(__name__)
app.config.from_object(app_config)

# Initialize the imported db with your app
db.init_app(app)

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

@app.route('/qc-dashboard')
def qc_dashboard():
    return render_template('qc_dashboard.html')

# moved out of main
from qc_plots import qc_bp
app.register_blueprint(qc_bp)

# Scanner application test
@app.route('/scanner_test')
def scanner_test():
    """Display the barcode scanner test page"""
    return render_template('scanner_test.html')

@app.route('/save_scan', methods=['POST'])
def save_scan():
    """Save scanned barcode to test table"""
    try:
        data = request.get_json()
        
        # Create new scan record
        new_scan = ScannerTest(
            scanned_code=data.get('scanned_code'),
            scan_type=data.get('scan_type', 'camera'),
            notes=data.get('notes', '')
        )
        
        db.session.add(new_scan)
        db.session.commit()
        
        return jsonify({
            'success': True, 
            'message': 'Barcode saved successfully',
            'scan_id': new_scan.scan_id
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False, 
            'message': f'Error saving scan: {str(e)}'
        }), 500

@app.route('/scan_history')
def scan_history():
    """View all scanned barcodes"""
    scans = ScannerTest.query.order_by(ScannerTest.scan_timestamp.desc()).all()
    return render_template('scan_history.html', scans=scans)

@app.route('/test-static')
def test_static():
    """Test that static files are being served correctly"""
    return '''
    <html>
        <head>
            <title>Static Files Test</title>
            <link href="/static/css/bootstrap.min.css" rel="stylesheet">
        </head>
        <body>
            <div class="container mt-5">
                <div class="alert alert-success">
                    <h4>✅ Static Files Test</h4>
                    <p>If this page is styled with Bootstrap, your static files are working!</p>
                    <button class="btn btn-primary">Test Button</button>
                    <a href="/" class="btn btn-secondary">Back to Main App</a>
                </div>
            </div>
            <script src="/static/js/lib/bootstrap.bundle.min.js"></script>
            <script src="/static/js/lib/html5-qrcode.min.js"></script>
            <script>
                console.log('Html5Qrcode available:', typeof Html5Qrcode !== 'undefined');
                console.log('Html5QrcodeScanner available:', typeof Html5QrcodeScanner !== 'undefined');
                if (typeof Html5Qrcode !== 'undefined') {
                    document.querySelector('.alert').innerHTML += '<p><strong>🎉 QR Scanner library loaded successfully!</strong></p>';
                } else {
                    document.querySelector('.alert').className = 'alert alert-danger';
                    document.querySelector('.alert').innerHTML += '<p><strong>❌ QR Scanner library failed to load</strong></p>';
                }
            </script>
        </body>
    </html>
    '''



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
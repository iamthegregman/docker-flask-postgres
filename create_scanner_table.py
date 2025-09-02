import os
import sys
from flask import Flask
from config import config
from models import db, ScannerTest

# Set up Flask app with same config as your main app
config_name = os.getenv('FLASK_ENV', 'development')
app_config = config.get(config_name, config['default'])

app = Flask(__name__)
app.config.from_object(app_config)
db.init_app(app)

def create_scanner_table():
    """Create the scanner test table"""
    with app.app_context():
        try:
            # Create the table
            db.create_all()
            print("✅ Scanner test table created successfully!")
            
            # Verify the table was created
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            
            if 'rdb_v3_tbl_scanner_test' in tables:
                print("✅ Table 'rdb_v3_tbl_scanner_test' confirmed in database")
                
                # Show table structure
                columns = inspector.get_columns('rdb_v3_tbl_scanner_test')
                print("\nTable structure:")
                for column in columns:
                    print(f"  - {column['name']}: {column['type']}")
            else:
                print("❌ Table was not created properly")
                
        except Exception as e:
            print(f"❌ Error creating table: {e}")
            print("\nFull error:")
            import traceback
            traceback.print_exc()

if __name__ == '__main__':
    create_scanner_table()
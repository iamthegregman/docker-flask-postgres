================================================================================
PROJECT STRUCTURE ANALYSIS
Root Directory: C:\Users\Gregt\Coding projects\flask_postgres_git
================================================================================

📁 DIRECTORY STRUCTURE:
----------------------------------------
📂 docker-flask-postgres/
  📂 .git/
    📂 hooks/
    📂 info/
    📂 logs/
      📂 refs/
        📂 heads/
        📂 remotes/
          📂 origin/
    📂 objects/
    📂 refs/
      📂 heads/
      📂 remotes/
        📂 origin/
      📂 tags/
  📂 app/
    📂 __pycache__/
    📂 templates/
  📂 base-image/
  📂 k8s/

📊 FILE SUMMARY (Total: 266 files):
----------------------------------------
Other: 233 files
  • deploy-flask-dbpw.bat
  • deploy-flask.bat
  • deploy-postgres.bat
  • docker-flask-postgres\.git\.COMMIT_EDITMSG.swo
  • docker-flask-postgres\.git\.COMMIT_EDITMSG.swp
  ... and 228 more

Python: 10 files
  • docker-flask-postgres\app\__pycache__\app.cpython-39.pyc
  • docker-flask-postgres\app\__pycache__\config.cpython-39.pyc
  • docker-flask-postgres\app\__pycache__\models.cpython-39.pyc
  • docker-flask-postgres\app\__pycache__\qc_plots.cpython-39.pyc
  • docker-flask-postgres\app\app.py
  ... and 5 more

Static JS: 1 files
  • project_structure.json

Database: 2 files
  • docker-flask-postgres\data_export_filtered.sql
  • qc_data.sql

Config: 5 files
  • docker-flask-postgres\.env
  • docker-flask-postgres\.env.prod
  • docker-flask-postgres\docker-compose.yml
  • docker-flask-postgres\k8s\flask-deployment.yaml
  • docker-flask-postgres\k8s\postgres-deployment.yaml

Docker: 4 files
  • docker-flask-postgres\Dockerfile
  • docker-flask-postgres\Dockerfile.postgres
  • docker-flask-postgres\Dockerfile.prod
  • docker-flask-postgres\base-image\Dockerfile

Documentation: 2 files
  • docker-flask-postgres\README.md
  • docker-flask-postgres\base-image\README.md

Requirements: 2 files
  • docker-flask-postgres\app\requirements.txt
  • docker-flask-postgres\base-image\requirements.txt

Templates: 7 files
  • docker-flask-postgres\app\templates\bootstrap_elements.html
  • docker-flask-postgres\app\templates\locations.html
  • docker-flask-postgres\app\templates\qc_dashboard.html
  • docker-flask-postgres\app\templates\reagent_detail.html
  • docker-flask-postgres\app\templates\reagents.html
  • docker-flask-postgres\app\templates\supplies.html
  • docker-flask-postgres\app\templates\supply_details.html

🌶️ FLASK APPLICATION ANALYSIS:
----------------------------------------
Main Application Files:
  • docker-flask-postgres\app\app.py

Model Files:
  • docker-flask-postgres\app\models.py
  • docker-flask-postgres\app\__pycache__\models.cpython-39.pyc

HTML Templates (7 files):
  • docker-flask-postgres\app\templates\bootstrap_elements.html
  • docker-flask-postgres\app\templates\locations.html
  • docker-flask-postgres\app\templates\qc_dashboard.html
  • docker-flask-postgres\app\templates\reagent_detail.html
  • docker-flask-postgres\app\templates\reagents.html
  • docker-flask-postgres\app\templates\supplies.html
  • docker-flask-postgres\app\templates\supply_detail.html

Static Files (1 files):
  • project_structure.json

Configuration Files:
  • docker-flask-postgres\.env
  • docker-flask-postgres\.env.prod
  • docker-flask-postgres\docker-compose.yml
  • docker-flask-postgres\k8s\flask-deployment.yaml
  • docker-flask-postgres\k8s\postgres-deployment.yaml

Docker Files:
  • docker-flask-postgres\Dockerfile
  • docker-flask-postgres\Dockerfile.postgres
  • docker-flask-postgres\Dockerfile.prod
  • docker-flask-postgres\base-image\Dockerfile

🔍 DETAILED FILE ANALYSIS:
----------------------------------------

Flask Routes Analysis:
  Could not analyze docker-flask-postgres\app\app.py: 'charmap' codec can't decode byte 0x9d in position 7679: character maps to <undefined>

Database Models Analysis:

  From docker-flask-postgres\app\models.py:
    • Acceptance
    • Locations
    • ReagentType
    • Reagent
    • ReagentLot
    • Supplies
    • SuppliesLots
    • Users
    • QCData
  Could not analyze docker-flask-postgres\app\__pycache__\models.cpython-39.pyc: 'charmap' codec can't decode byte 0x8d in position 422: character maps to <undefined>

Dependency Files:
  • docker-flask-postgres\app\requirements.txt
    Contains 7 dependencies
    - flask
    - requests
    - flask-sqlalchemy
    - psycopg2-binary>=2.9.3
    - python-dotenv
    - gunicorn
    - plotly
  • docker-flask-postgres\base-image\requirements.txt
    Contains 7 dependencies
    - flask
    - requests
    - flask-sqlalchemy
    - psycopg2-binary>=2.9.3
    - python-dotenv
    - gunicorn
    - plotly

================================================================================
ANALYSIS COMPLETE
================================================================================

You can copy this output into your context window to help with project planning.
Consider creating these documentation files based on the analysis:
  • FILE_STRUCTURE.md - Document the directory organization
  • DATABASE_SCHEMA.md - Detail your SQLAlchemy models
  • DEPLOYMENT_CONFIG.md - Document Docker/Kubernetes setup
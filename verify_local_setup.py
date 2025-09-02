# verify_local_setup.py
# Run this to verify your local static files are set up correctly

import os
from pathlib import Path

def verify_static_files():
    """Verify that all required static files are present"""
    
    print("🔍 Verifying Static Files Setup\n")
    
    # Define required files
    required_files = {
        'app/static/js/lib/html5-qrcode.min.js': 'HTML5 QR Code Scanner Library',
        'app/static/js/lib/bootstrap.bundle.min.js': 'Bootstrap JavaScript Bundle',
        'app/static/css/bootstrap.min.css': 'Bootstrap CSS'
    }
    
    all_present = True
    
    for file_path, description in required_files.items():
        path = Path(file_path)
        if path.exists():
            file_size = path.stat().st_size
            print(f"✅ {description}")
            print(f"   Location: {file_path}")
            print(f"   Size: {file_size:,} bytes\n")
        else:
            print(f"❌ {description}")
            print(f"   Missing: {file_path}\n")
            all_present = False
    
    # Check directory structure
    print("📁 Directory Structure:")
    static_dir = Path('app/static')
    if static_dir.exists():
        for root, dirs, files in os.walk(static_dir):
            level = root.replace(str(static_dir), '').count(os.sep)
            indent = '  ' * level
            print(f"{indent}{os.path.basename(root)}/")
            subindent = '  ' * (level + 1)
            for file in files:
                print(f"{subindent}{file}")
    else:
        print("❌ app/static directory does not exist!")
        all_present = False
    
    print("\n" + "="*50)
    
    if all_present:
        print("✅ ALL FILES PRESENT - Your setup is ready!")
        print("\nNext steps:")
        print("1. Make sure your Flask app is configured for static files")
        print("2. Test by visiting: http://your-app/test-static")
        print("3. Try the scanner at: http://your-app/scanner_test")
    else:
        print("❌ SETUP INCOMPLETE")
        print("\nTo fix:")
        print("1. Run: python download_scanner_library.py")
        print("2. Or use the npm approach and copy files manually")
        print("3. Ensure your directory structure matches the requirements")
    
    return all_present

def create_static_dirs():
    """Create the static directory structure"""
    dirs_to_create = [
        'app/static/js/lib',
        'app/static/css',
        'app/static/images'
    ]
    
    for dir_path in dirs_to_create:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print(f"📁 Created directory: {dir_path}")

if __name__ == '__main__':
    print("Creating static directories...")
    create_static_dirs()
    print()
    verify_static_files()
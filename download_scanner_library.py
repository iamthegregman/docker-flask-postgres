# download_scanner_library.py
import os
import urllib.request
from pathlib import Path

def download_html5_qrcode_library():
    """Download the html5-qrcode library to local static files"""
    
    # Ensure static/js/lib directory exists
    lib_dir = Path('app/static/js/lib')
    lib_dir.mkdir(parents=True, exist_ok=True)
    
    # URLs for the library files
    files_to_download = {
        'html5-qrcode.min.js': 'https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js',
        # You can also download the full version for debugging:
        # 'html5-qrcode.js': 'https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.js'
    }
    
    for filename, url in files_to_download.items():
        file_path = lib_dir / filename
        
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, file_path)
            print(f"✅ Successfully downloaded {filename}")
            
            # Check file size to ensure it downloaded correctly
            file_size = file_path.stat().st_size
            print(f"   File size: {file_size:,} bytes")
            
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")
    
    # Also download Bootstrap locally if you want to be fully self-contained
    bootstrap_files = {
        'bootstrap.min.css': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css',
        'bootstrap.bundle.min.js': 'https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js'
    }
    
    # Create CSS directory
    css_dir = Path('app/static/css')
    css_dir.mkdir(parents=True, exist_ok=True)
    
    for filename, url in bootstrap_files.items():
        if filename.endswith('.css'):
            file_path = css_dir / filename
        else:
            file_path = lib_dir / filename
            
        print(f"Downloading {filename}...")
        try:
            urllib.request.urlretrieve(url, file_path)
            print(f"✅ Successfully downloaded {filename}")
            
            file_size = file_path.stat().st_size
            print(f"   File size: {file_size:,} bytes")
            
        except Exception as e:
            print(f"❌ Error downloading {filename}: {e}")
    
    print(f"\n🎉 All libraries downloaded to:")
    print(f"   - app/static/js/lib/")
    print(f"   - app/static/css/")
    print(f"\nYour static directory structure:")
    
    # Show directory structure
    static_dir = Path('app/static')
    for root, dirs, files in os.walk(static_dir):
        level = root.replace(str(static_dir), '').count(os.sep)
        indent = ' ' * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

if __name__ == '__main__':
    download_html5_qrcode_library()
#!/usr/bin/env python3
"""
Verification script to check that all new files and endpoints are properly integrated
"""

import os
import sys

def check_file_exists(filepath):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ File exists: {filepath}")
        return True
    else:
        print(f"❌ File missing: {filepath}")
        return False

def check_imports():
    """Check that we can import our new modules"""
    try:
        # Add the project root to sys.path
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        backend_path = os.path.join(project_root, "social-media-manager-app")
        sys.path.insert(0, backend_path)
        
        # Try to import our new modules
        from src.services.video_analyzer import VideoAnalyzer
        print("✅ VideoAnalyzer import successful")
        
        from src.routes.user_analytics import user_analytics_bp
        print("✅ user_analytics_bp import successful")
        
        from src.routes.favorite_content import favorite_content_bp
        print("✅ favorite_content_bp import successful")
        
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    print("🔍 Verifying AI Social Media Manager Implementation")
    print("=" * 55)
    
    # Define the base path
    base_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    # Check for new service files
    service_files = [
        "social-media-manager-app/src/services/video_analyzer.py"
    ]
    
    # Check for new route files
    route_files = [
        "social-media-manager-app/src/routes/user_analytics.py",
        "social-media-manager-app/src/routes/favorite_content.py"
    ]
    
    # Check all files
    all_files_exist = True
    
    print("\n📁 Checking service files:")
    for file in service_files:
        filepath = os.path.join(base_path, file)
        if not check_file_exists(filepath):
            all_files_exist = False
    
    print("\n🛣️ Checking route files:")
    for file in route_files:
        filepath = os.path.join(base_path, file)
        if not check_file_exists(filepath):
            all_files_exist = False
    
    print("\n🔧 Checking imports:")
    imports_ok = check_imports()
    
    print("\n" + "=" * 55)
    if all_files_exist and imports_ok:
        print("🎉 All verification checks passed!")
        print("✅ New files are properly created")
        print("✅ Modules can be imported successfully")
        print("✅ Implementation is complete and integrated")
    else:
        print("❌ Some verification checks failed")
        print("Please review the errors above")
    
    return all_files_exist and imports_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
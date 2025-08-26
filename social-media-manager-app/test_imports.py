import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.main import create_app
    print("✓ main.py imports successfully")
except Exception as e:
    print(f"✗ Error importing main.py: {e}")

try:
    from src.ai_providers import ai_manager, AIProvider
    print("✓ ai_providers imports successfully")
    # Test that the required methods exist
    if hasattr(ai_manager, 'get_provider_status'):
        print("✓ ai_manager.get_provider_status method exists")
    else:
        print("✗ ai_manager.get_provider_status method missing")
        
    if hasattr(ai_manager, 'transcribe_audio'):
        print("✓ ai_manager.transcribe_audio method exists")
    else:
        print("✗ ai_manager.transcribe_audio method missing")
        
    if hasattr(ai_manager, 'analyze_image'):
        print("✓ ai_manager.analyze_image method exists")
    else:
        print("✗ ai_manager.analyze_image method missing")
except Exception as e:
    print(f"✗ Error importing ai_providers: {e}")

try:
    from src.database import db_manager, Platform, ContentType
    print("✓ database imports successfully")
except Exception as e:
    print(f"✗ Error importing database: {e}")

try:
    from src.ml_services import ml_services
    print("✓ ml_services imports successfully")
except Exception as e:
    print(f"✗ Error importing ml_services: {e}")

try:
    import app
    print("✓ app.py imports successfully")
except Exception as e:
    print(f"✗ Error importing app.py: {e}")
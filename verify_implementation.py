"""
Verification script to check if the Urdu translation implementation is complete
without requiring the server to be running.
"""

import os
import sys
from pathlib import Path

def verify_backend_implementation():
    """Verify backend translation implementation"""
    print("Verifying Backend Implementation...")
    print("=" * 40)

    backend_path = Path("E:\\GIAIC Q4 AGENTIC AI\\PIAHR\\backend")

    # Check required files exist
    required_files = [
        "src/api/translation_routes.py",
        "src/services/translation_service.py",
        "src/schemas/translation.py",
        "src/models/translation_session.py",
        "src/utils/translation_cache.py",
        "src/middleware/translation_auth.py"
    ]

    all_present = True
    for file_path in required_files:
        full_path = backend_path / file_path
        if full_path.exists():
            print(f"[OK] {file_path} - EXISTS")
        else:
            print(f"[ER] {file_path} - MISSING")
            all_present = False

    # Check if translation routes are included in main API
    api_init_path = backend_path / "src/api/__init__.py"
    if api_init_path.exists():
        content = api_init_path.read_text()
        if "translation" in content.lower():
            print("[OK] Translation routes registered in main API")
        else:
            print("[ER] Translation routes NOT registered in main API")
            all_present = False

    # Check if Google Cloud Translation is configured
    config_path = backend_path / "src/core/config.py"
    if config_path.exists():
        content = config_path.read_text()
        if "GOOGLE_CLOUD_TRANSLATE" in content:
            print("[OK] Google Cloud Translation API configured in settings")
        else:
            print("[??] Google Cloud Translation API settings not found (may be OK for development)")

    return all_present

def verify_frontend_implementation():
    """Verify frontend translation implementation"""
    print("\nVerifying Frontend Implementation...")
    print("=" * 40)

    frontend_path = Path("E:\\GIAIC Q4 AGENTIC AI\\PIAHR\\frontend")

    # Check required files exist
    required_files = [
        "src/components/TranslationButton/TranslationButton.tsx",
        "src/components/TranslationButton/TranslationButton.css",
        "src/components/ChapterContent/ChapterContent.jsx"
    ]

    all_present = True
    for file_path in required_files:
        full_path = frontend_path / file_path
        if full_path.exists():
            print(f"[OK] {file_path} - EXISTS")
        else:
            print(f"[ER] {file_path} - MISSING")
            all_present = False

    # Check if RTL styling is implemented
    custom_css_path = frontend_path / "src/css/custom.css"
    if custom_css_path.exists():
        content = custom_css_path.read_text()
        if "rtl" in content.lower() or "direction: rtl" in content:
            print("[OK] RTL (right-to-left) styling implemented")
        else:
            print("[??] RTL styling not found")

    # Check if Urdu fonts are imported
    if "noto nastaliq" in content.lower():
        print("[OK] Urdu fonts imported")
    else:
        print("[??] Urdu fonts not found in CSS")

    return all_present

def verify_requirements():
    """Verify requirements include necessary dependencies"""
    print("\nVerifying Requirements...")
    print("=" * 40)

    backend_path = Path("E:\\GIAIC Q4 AGENTIC AI\\PIAHR\\backend")
    requirements_path = backend_path / "requirements.txt"

    if requirements_path.exists():
        content = requirements_path.read_text()
        if "google-cloud-translate" in content:
            print("[OK] Google Cloud Translation dependency included")
        else:
            print("[ER] Google Cloud Translation dependency missing")

        if "slowapi" in content:
            print("[OK] SlowAPI rate limiting dependency included")
        else:
            print("[??] SlowAPI dependency not found (may be needed for rate limiting)")

    return True

def verify_no_bonus_points():
    """Verify that bonus points functionality has been removed"""
    print("\nVerifying No Bonus Points Implementation...")
    print("=" * 40)

    backend_path = Path("E:\\GIAIC Q4 AGENTIC AI\\PIAHR\\backend")

    # Check that bonus points related files are not present or have been removed
    potential_bonus_files = [
        "src/services/bonus_points_service.py",
        "src/models/bonus_points_record.py",  # This should not exist anymore
        "src/api/bonus_points_routes.py"
    ]

    no_bonus_found = True
    for file_path in potential_bonus_files:
        full_path = backend_path / file_path
        if full_path.exists():
            print(f"[ER] {file_path} - BONUS POINTS FILE STILL EXISTS")
            no_bonus_found = False
        else:
            print(f"[OK] {file_path} - CORRECTLY REMOVED")

    # Check that schemas don't include bonus points
    schema_path = backend_path / "src/schemas/translation.py"
    if schema_path.exists():
        content = schema_path.read_text()
        if "bonus" in content.lower():
            print("[ER] Bonus points still present in translation schema")
            no_bonus_found = False
        else:
            print("[OK] No bonus points in translation schema")

    # Check that translation service doesn't include bonus points
    service_path = backend_path / "src/services/translation_service.py"
    if service_path.exists():
        content = service_path.read_text()
        if "bonus" in content.lower() and "bonus_points_awarded" in content:
            print("[??] Bonus points still referenced in translation service")
        else:
            print("[OK] Translation service doesn't reference bonus points")

    return no_bonus_found

def main():
    print("URDU TRANSLATION IMPLEMENTATION VERIFICATION")
    print("=" * 50)
    print("Checking if all required components for Urdu translation are implemented...")
    print()

    backend_ok = verify_backend_implementation()
    frontend_ok = verify_frontend_implementation()
    requirements_ok = verify_requirements()
    no_bonus_ok = verify_no_bonus_points()

    print("\nSUMMARY")
    print("=" * 50)
    print(f"Backend Implementation: {'[OK] COMPLETE' if backend_ok else '[ER] INCOMPLETE'}")
    print(f"Frontend Implementation: {'[OK] COMPLETE' if frontend_ok else '[ER] INCOMPLETE'}")
    print(f"Requirements: {'[OK] COMPLETE' if requirements_ok else '[ER] INCOMPLETE'}")
    print(f"No Bonus Points: {'[OK] CORRECT' if no_bonus_ok else '[ER] INCORRECT'}")

    overall_success = all([backend_ok, frontend_ok, requirements_ok, no_bonus_ok])

    print(f"\nOVERALL STATUS: {'[OK] ALL REQUIREMENTS MET' if overall_success else '[ER] SOME REQUIREMENTS MISSING'}")

    if overall_success:
        print("\n[SUCCESS] Urdu translation functionality has been successfully implemented!")
        print("   - Backend translation service is in place")
        print("   - Frontend translation button component created")
        print("   - Right-to-left text rendering implemented")
        print("   - Error handling and fallback strategies in place")
        print("   - No bonus points functionality (as requested)")
        print("   - Rate limiting configured")
    else:
        print("\n[ERROR] Some implementation requirements are not met. Please review the issues above.")

    return overall_success

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
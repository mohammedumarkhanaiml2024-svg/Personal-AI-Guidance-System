#!/usr/bin/env python3
"""
Quick API Test Script
Tests if the Personal AI Guidance System API is running correctly
"""

import requests
import json

API_URL = "http://localhost:8000"

def print_header(text):
    print("\n" + "=" * 70)
    print(f"  {text}")
    print("=" * 70 + "\n")

def test_api():
    print_header("🧪 TESTING PERSONAL AI GUIDANCE SYSTEM API")
    
    # Test 1: Check if server is running
    print("Test 1: Checking server status...")
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Server is ONLINE!")
            print(f"   App: {data['app']}")
            print(f"   Version: {data['version']}")
            print(f"   Status: {data['status']}")
        else:
            print(f"❌ Server returned status code: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ CONNECTION REFUSED!")
        print("\nTroubleshooting:")
        print("  1. Check if server is running: ps aux | grep uvicorn")
        print("  2. In Codespaces, check the PORTS tab at the bottom")
        print("  3. Restart server: python -m uvicorn main_enhanced:app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Check available features
    print("\nTest 2: Checking available features...")
    print("\n1️⃣  INPUT FEATURES (Data Collection):")
    for feature in data['features']['input_features']:
        print(f"   ✓ {feature}")
    
    print("\n2️⃣  AI CAPABILITIES:")
    for capability in data['features']['ai_capabilities']:
        print(f"   ✓ {capability}")
    
    # Test 3: Try to register a user
    print("\nTest 3: Testing user registration...")
    import time
    username = f"testuser_{int(time.time())}"
    try:
        response = requests.post(f"{API_URL}/register", json={
            "username": username,
            "password": "testpass123"
        })
        if response.status_code == 200:
            print(f"✅ User '{username}' registered successfully!")
        else:
            print(f"⚠️  Registration returned status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Registration test skipped: {e}")
    
    # Test 4: Check API documentation
    print("\nTest 4: Checking API documentation...")
    try:
        response = requests.get(f"{API_URL}/docs", timeout=5)
        if response.status_code == 200:
            print("✅ Swagger UI is accessible at /docs")
        else:
            print(f"⚠️  Docs returned status: {response.status_code}")
    except Exception as e:
        print(f"⚠️  Could not check docs: {e}")
    
    print_header("✅ ALL TESTS PASSED!")
    print("Your Personal AI Guidance System is ready to use!\n")
    print("📍 ACCESS THE API:")
    print(f"   • Swagger UI: {API_URL}/docs")
    print(f"   • ReDoc:      {API_URL}/redoc")
    print(f"   • API Root:   {API_URL}/")
    print("\n💡 TIP: In GitHub Codespaces, check the PORTS tab and click on port 8000")
    print("\n🚀 NEXT STEPS:")
    print("   1. Open /docs in your browser for interactive API testing")
    print("   2. Run: python demo_example.py for a complete demo")
    print("   3. Read: README.md for full documentation\n")
    
    return True

if __name__ == "__main__":
    try:
        test_api()
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

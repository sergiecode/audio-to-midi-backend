"""
Simple API Test - No Dependencies
Created by Sergie Code

Tests basic API connectivity without external libraries.
"""

import urllib.request
import urllib.parse
import json

def test_health():
    """Test health endpoint using urllib."""
    print("🏥 Testing health endpoint...")
    try:
        with urllib.request.urlopen('http://localhost:5000/health') as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print(f"✅ Health check passed: {data['status']}")
                return True
            else:
                print(f"❌ Health check failed: {response.status}")
                return False
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
        return False

def test_formats():
    """Test supported formats endpoint."""
    print("📝 Testing supported formats...")
    try:
        with urllib.request.urlopen('http://localhost:5000/supported_formats') as response:
            if response.status == 200:
                data = json.loads(response.read().decode())
                print(f"✅ Supported formats: {', '.join(data['supported_formats'])}")
                return True
            else:
                print(f"❌ Formats check failed: {response.status}")
                return False
    except Exception as e:
        print(f"❌ Formats test error: {str(e)}")
        return False

def main():
    """Run basic connectivity tests."""
    print("🎵 Audio to MIDI Backend - Basic API Test")
    print("Created by Sergie Code\n")
    
    tests_passed = 0
    total_tests = 2
    
    if test_health():
        tests_passed += 1
    
    print()
    
    if test_formats():
        tests_passed += 1
    
    print(f"\n{'='*50}")
    print(f"Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 Basic API tests passed!")
        print("\n📋 To test full functionality:")
        print("   1. Open browser: http://localhost:5000/health")
        print("   2. Use Postman to test file upload to /transcribe")
        print("   3. Or run: python quick_test.py (if requests library available)")
    else:
        print("❌ Some tests failed.")
        print("   Make sure the server is running: python app.py")
    
    print("\n✨ Testing complete!")

if __name__ == "__main__":
    main()

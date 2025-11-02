#!/usr/bin/env python3
"""
Test script for Enhanced Fake Job Postings Detection App
Tests both text analysis and OCR functionality
"""

import requests
import json
import base64
from PIL import Image, ImageDraw, ImageFont
import io
import os

API_BASE_URL = 'http://localhost:5000'

def test_backend_health():
    """Test if backend is running."""
    try:
        response = requests.get(f'{API_BASE_URL}/health')
        if response.status_code == 200:
            print("✅ Backend is running!")
            return True
        else:
            print("❌ Backend health check failed")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to backend. Make sure Flask app is running on port 5000")
        return False

def test_text_analysis():
    """Test text-based job posting analysis."""
    print("\n🔍 Testing Text Analysis...")
    
    # Test with a suspicious job posting
    fake_job_text = """
    URGENT! Make $5000/week working from home!
    
    No experience needed! Just pay $99 registration fee to get started.
    Contact us at: jobscam@gmail.com
    
    This is a limited time offer - ACT NOW!
    Send money via Western Union to secure your position.
    """
    
    try:
        response = requests.post(f'{API_BASE_URL}/api/analyze', 
                               json={'text': fake_job_text})
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Analysis completed!")
            print(f"   Score: {result['score']}/100")
            print(f"   Status: {'FAKE' if result['is_fake'] else 'LEGITIMATE'}")
            print(f"   Method: {result['method']}")
            print(f"   Flags found: {len(result['flags'])}")
            return True
        else:
            print(f"❌ Analysis failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error during text analysis: {e}")
        return False

def create_test_image():
    """Create a test job posting image."""
    # Create a simple job posting image
    img = Image.new('RGB', (600, 400), color='white')
    draw = ImageDraw.Draw(img)
    
    # Try to use a default font, fallback to basic if not available
    try:
        font = ImageFont.truetype("arial.ttf", 16)
        title_font = ImageFont.truetype("arial.ttf", 20)
    except:
        font = ImageFont.load_default()
        title_font = ImageFont.load_default()
    
    # Add job posting text
    job_text = [
        "SOFTWARE DEVELOPER POSITION",
        "",
        "Company: TechCorp Solutions",
        "Location: Remote",
        "",
        "Requirements:",
        "- 2+ years Python experience",
        "- Knowledge of Flask/Django",
        "- Bachelor's degree preferred",
        "",
        "Salary: $60,000 - $80,000",
        "",
        "Contact: hr@techcorp.com",
        "Apply at: www.techcorp.com/careers"
    ]
    
    y_position = 20
    for line in job_text:
        if line == job_text[0]:  # Title
            draw.text((20, y_position), line, fill='black', font=title_font)
        else:
            draw.text((20, y_position), line, fill='black', font=font)
        y_position += 25
    
    # Convert to base64
    buffer = io.BytesIO()
    img.save(buffer, format='PNG')
    img_data = base64.b64encode(buffer.getvalue()).decode()
    
    return f"data:image/png;base64,{img_data}"

def test_image_analysis():
    """Test image-based job posting analysis."""
    print("\n📷 Testing Image Analysis (OCR)...")
    
    try:
        # Create test image
        test_image_data = create_test_image()
        
        response = requests.post(f'{API_BASE_URL}/api/analyze', 
                               json={'image': test_image_data})
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ OCR Analysis completed!")
            print(f"   Score: {result['score']}/100")
            print(f"   Status: {'FAKE' if result['is_fake'] else 'LEGITIMATE'}")
            print(f"   Source: {result['source']}")
            if 'extracted_text' in result:
                print(f"   Extracted text length: {len(result['extracted_text'])} characters")
                print(f"   Sample text: {result['extracted_text'][:100]}...")
            return True
        else:
            error_data = response.json() if response.headers.get('content-type') == 'application/json' else response.text
            print(f"❌ OCR Analysis failed: {error_data}")
            return False
            
    except Exception as e:
        print(f"❌ Error during image analysis: {e}")
        return False

def test_chatbot():
    """Test chatbot functionality."""
    print("\n🤖 Testing Chatbot...")
    
    # Mock analysis result for context
    mock_context = {
        'score': 30,
        'is_fake': True,
        'recommendations': {
            'courses': [
                {'title': 'Python Programming', 'provider': 'Coursera', 'free': True, 'url': 'https://example.com'}
            ],
            'jobs': [
                {'title': 'Software Jobs', 'company': 'LinkedIn', 'url': 'https://linkedin.com/jobs'}
            ]
        }
    }
    
    test_messages = [
        "Show me courses",
        "Find me job opportunities", 
        "Give me safety tips",
        "Help me"
    ]
    
    success_count = 0
    for message in test_messages:
        try:
            response = requests.post(f'{API_BASE_URL}/api/chat', 
                                   json={'message': message, 'context': mock_context})
            
            if response.status_code == 200:
                result = response.json()
                print(f"✅ Chatbot response for '{message}': {len(result['response'])} chars")
                success_count += 1
            else:
                print(f"❌ Chatbot failed for '{message}': {response.text}")
                
        except Exception as e:
            print(f"❌ Error testing chatbot with '{message}': {e}")
    
    return success_count == len(test_messages)

def main():
    """Run all tests."""
    print("🧪 Enhanced Fake Job Postings Detection - Test Suite")
    print("=" * 60)
    
    tests_passed = 0
    total_tests = 4
    
    # Test 1: Backend Health
    if test_backend_health():
        tests_passed += 1
    
    # Test 2: Text Analysis
    if test_text_analysis():
        tests_passed += 1
    
    # Test 3: Image Analysis (OCR)
    if test_image_analysis():
        tests_passed += 1
    
    # Test 4: Chatbot
    if test_chatbot():
        tests_passed += 1
    
    # Results
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("🎉 All tests passed! Your enhanced app is working correctly.")
    else:
        print("⚠️ Some tests failed. Check the error messages above.")
        
        if tests_passed == 0:
            print("\n💡 Quick fixes:")
            print("1. Make sure Flask backend is running: python backend/app.py")
            print("2. Install dependencies: pip install -r requirements.txt")
            print("3. Setup OCR: python install_ocr.py")

if __name__ == "__main__":
    main()
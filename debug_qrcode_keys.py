import requests
import json

API_URL = "https://chatbot-production-e324.up.railway.app"

def debug_qrcode():
    print(f"🔍 Debugging QR Code endpoint: {API_URL}/management/qrcode")
    
    try:
        response = requests.get(f"{API_URL}/management/qrcode", timeout=30)
        
        print(f"Status Code: {response.status_code}")
        try:
            data = response.json()
            print("Keys returned:", data.keys())
            if 'base64' in data:
                print(f"base64 starts with: {data['base64'][:50]}...")
            if 'code' in data:
                print(f"code starts with: {data['code'][:50]}...")
        except:
            print("Response Text:")
            print(response.text)
            
    except Exception as e:
        print(f"❌ Request failed: {e}")

if __name__ == "__main__":
    debug_qrcode()

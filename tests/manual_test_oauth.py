import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.infrastructure.auth import LinkedInAuthenticator

def run_test():
    print("Testing LinkedIn Authenticator with Client Credentials Flow...")
    auth = LinkedInAuthenticator()
    
    token = auth.get_client_credentials_token()
    
    if token:
        print(f"\nSuccess! Retrieved token: {token[:15]}... (truncated for security)")
    else:
        print("\nFailed to retrieve token. Please ensure your LINKEDIN_CLIENT_ID and LINKEDIN_CLIENT_SECRET in the .env file are valid.")

if __name__ == '__main__':
    run_test()

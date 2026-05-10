import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.infrastructure.auth import LinkedInAuthenticator

def run_test():
    print("Testing LinkedIn Authenticator with 3-Legged Authorization Code Flow...")
    auth = LinkedInAuthenticator()
    
    # You MUST configure this exact redirect URI in your LinkedIn Developer App portal
    # under the "Auth" tab -> "OAuth 2.0 settings" -> "Authorized redirect URLs for your app"
    redirect_uri = "http://localhost:8000/callback"
    
    token = auth.get_authorization_code_token(redirect_uri=redirect_uri)
    
    if token:
        print(f"\nSuccess! Retrieved Token: {token}")
        print("\nIMPORTANT: Copy the token above and paste it as your LINKEDIN_ACCESS_TOKEN in your .env file!")
    else:
        print("\nFailed to retrieve token. Make sure your client credentials are correct and you pasted the correct code.")

if __name__ == '__main__':
    run_test()

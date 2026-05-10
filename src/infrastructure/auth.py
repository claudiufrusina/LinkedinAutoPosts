import requests
from src.config import LINKEDIN_CLIENT_ID, LINKEDIN_CLIENT_SECRET

class LinkedInAuthenticator:
    def __init__(self, client_id: str = None, client_secret: str = None):
        self.client_id = client_id or LINKEDIN_CLIENT_ID
        self.client_secret = client_secret or LINKEDIN_CLIENT_SECRET
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"

    def get_client_credentials_token(self) -> str:
        """
        Retrieves a 2-legged OAuth token using Client Credentials Flow.
        Note: This token is typically used for managing Organization pages,
        not for posting on personal member profiles.
        """
        if not self.client_id or not self.client_secret:
            print("Client ID or Secret is missing.")
            return None

        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            response = requests.post(self.token_url, data=payload, headers=headers)
            
            if response.status_code == 200:
                token_data = response.json()
                print("Successfully generated access token.")
                return token_data.get("access_token")
            else:
                print(f"Failed to get access token: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error during token generation: {e}")
            return None

    def get_authorization_code_token(self, redirect_uri: str = "http://localhost:8000/callback") -> str:
        """
        Retrieves a 3-legged OAuth token using the Authorization Code Flow.
        This is typically required for posting on behalf of a personal LinkedIn member.
        """
        import urllib.parse

        if not self.client_id or not self.client_secret:
            print("Client ID or Secret is missing.")
            return None

        # Step 1: Generate Authorization URL
        auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        # The 'w_member_social' scope is required to create posts. 
        # 'openid', 'profile', 'email' are common standard scopes if you need to read user info.
        scope = "w_member_social openid profile email" 
        
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": redirect_uri,
            "state": "random_string_123",
            "scope": scope
        }
        
        url_params = urllib.parse.urlencode(params)
        full_auth_url = f"{auth_url}?{url_params}"
        
        print("\n--- 3-Legged OAuth Authorization ---")
        print("1. Please open the following URL in your web browser:")
        print(f"\n{full_auth_url}\n")
        print("2. Log into LinkedIn and authorize the application.")
        print(f"3. You will be redirected to a page starting with '{redirect_uri}'.")
        print("   (It's okay if your browser says 'Site can't be reached')")
        print("4. Look at the URL in your browser's address bar. It will look something like this:")
        print(f"   {redirect_uri}?code=AQW...&state=random_string_123")
        
        # Step 2: Get code from user
        auth_code = input("\n5. Paste the 'code' parameter value here (just the code string): ").strip()
        
        if not auth_code:
            print("No code provided. Aborting.")
            return None
            
        # Step 3: Exchange code for access token
        payload = {
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        try:
            print("\nExchanging code for access token...")
            response = requests.post(self.token_url, data=payload, headers=headers)
            
            if response.status_code == 200:
                token_data = response.json()
                print("Successfully generated 3-legged access token!")
                
                # Note: This token is valid for a certain duration (e.g., 60 days)
                expires_in = token_data.get("expires_in", 0)
                print(f"Token expires in {expires_in} seconds ({expires_in/86400:.1f} days).")
                
                return token_data.get("access_token")
            else:
                print(f"Failed to get access token: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Error during token exchange: {e}")
            return None

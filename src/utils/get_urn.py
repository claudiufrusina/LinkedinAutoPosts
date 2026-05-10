import os
import requests
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("LINKEDIN_ACCESS_TOKEN")

if not token or token == "your_access_token":
    print("Please set your LINKEDIN_ACCESS_TOKEN in .env first.")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

print("Attempting to fetch your Person URN...")

# Try the userinfo endpoint (requires openid scope)
resp1 = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
if resp1.status_code == 200:
    data = resp1.json()
    urn = f"urn:li:person:{data.get('sub')}"
    print(f"\nSUCCESS! Your URN is: {urn}")
    print("\nCopy and paste this into your .env file as LINKEDIN_PERSON_URN")
    exit(0)

# Try the me endpoint (requires r_liteprofile or profile scope)
resp2 = requests.get("https://api.linkedin.com/v2/me", headers=headers)
if resp2.status_code == 200:
    data = resp2.json()
    urn = f"urn:li:person:{data.get('id')}"
    print(f"\nSUCCESS! Your URN is: {urn}")
    print("\nCopy and paste this into your .env file as LINKEDIN_PERSON_URN")
    exit(0)

print("\nFailed to get URN.")
print("The token in your .env file only has permission to post (w_member_social), but not to read your profile ID.")
print("\nTo fix this:")
print("1. Go back to the LinkedIn Token Generator.")
print("2. When selecting scopes, check BOTH 'w_member_social' AND 'profile' (or 'openid').")
print("3. Generate a new token, put it in .env, and run this script again.")

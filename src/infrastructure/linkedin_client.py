import requests
from typing import Optional
from src.interfaces.social_client import ISocialClient
from src.config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN

class LinkedInClient(ISocialClient):
    def __init__(self, access_token: str = None, person_urn: str = None):
        self.access_token = access_token or LINKEDIN_ACCESS_TOKEN
        self.person_urn = person_urn or LINKEDIN_PERSON_URN
        self.headers = {
            'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        if self.access_token:
            self.headers['Authorization'] = f'Bearer {self.access_token}'

    def _register_upload(self) -> dict:
        if not self.access_token or not self.person_urn:
            print("Missing LinkedIn credentials.")
            return {}

        url = "https://api.linkedin.com/v2/assets?action=registerUpload"
        payload = {
            "registerUploadRequest": {
                "recipes": ["urn:li:digitalmediaRecipe:feedshare-image"],
                "owner": self.person_urn,
                "serviceRelationships": [
                    {
                        "relationshipType": "OWNER",
                        "identifier": "urn:li:userGeneratedContent"
                    }
                ]
            }
        }
        response = requests.post(url, headers=self.headers, json=payload)
        
        if response.status_code == 200:
            return response.json()
        print(f"Error registering upload: {response.status_code} - {response.text}")
        return {}

    def _upload_image(self, image_path: str, upload_url: str) -> bool:
        with open(image_path, 'rb') as f:
            image_data = f.read()
            
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/octet-stream'
        }
        response = requests.put(upload_url, headers=headers, data=image_data)
        
        if response.status_code == 201:
            return True
        print(f"Error uploading image: {response.status_code} - {response.text}")
        return False

    def _create_post(self, text: str, asset_urn: str = None) -> bool:
        if not self.access_token or not self.person_urn:
            print("Missing LinkedIn credentials.")
            return False

        url = "https://api.linkedin.com/v2/ugcPosts"
        
        media_content = []
        if asset_urn:
            media_content = [{
                "status": "READY",
                "media": asset_urn
            }]

        payload = {
            "author": self.person_urn,
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {
                        "text": text
                    },
                    "shareMediaCategory": "IMAGE" if asset_urn else "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        
        if media_content:
            payload["specificContent"]["com.linkedin.ugc.ShareContent"]["media"] = media_content
        
        response = requests.post(url, headers=self.headers, json=payload)
        if response.status_code == 201:
            print("Post created successfully!")
            return True
        print(f"Error creating post: {response.status_code} - {response.text}")
        return False

    def publish_post(self, text: str, image_path: Optional[str] = None) -> bool:
        asset_urn = None
        
        if image_path:
            upload_data = self._register_upload()
            if upload_data and 'value' in upload_data:
                upload_mechanism = upload_data['value']['uploadMechanism']['com.linkedin.digitalmedia.uploading.MediaUploadHttpRequest']
                upload_url = upload_mechanism['uploadUrl']
                asset_urn = upload_data['value']['asset']
                
                print(f"Uploading image to {upload_url[:50]}...")
                upload_success = self._upload_image(image_path, upload_url)
                if not upload_success:
                    print("Failed to upload image. Posting without image.")
                    asset_urn = None
        
        return self._create_post(text, asset_urn)

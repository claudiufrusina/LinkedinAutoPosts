import os
import json
from datetime import datetime
from typing import Tuple, Optional
from src.interfaces.content_provider import IContentProvider

class FileContentProvider(IContentProvider):
    def __init__(self):
        # Account for being in src/infrastructure now (2 levels deep to root)
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        self.texts_file = os.path.join(self.data_dir, 'texts.json')
        self.links_file = os.path.join(self.data_dir, 'links.json')
        self.images_dir = os.path.join(self.data_dir, 'images')
        self.template_file = os.path.join(self.data_dir, 'Template.txt')

    def get_post_content(self) -> Tuple[str, Optional[str]]:
        # 1. Pop from links.json
        if not os.path.exists(self.links_file):
            return "No content available", None
            
        with open(self.links_file, 'r', encoding='utf-8') as f:
            try:
                links_data = json.load(f)
            except json.JSONDecodeError:
                links_data = []
                
        if not links_data:
            return "No content available", None
            
        link_obj = None
        now = datetime.now()
        
        # Loop until we find a valid link or run out
        while links_data:
            candidate = links_data.pop(0)
            exp_str = candidate.get("expiration_date")
            
            if exp_str:
                try:
                    exp_date = datetime.fromisoformat(exp_str)
                    if exp_date < now:
                        print(f"Post {candidate.get('id')} has expired (expired on {exp_date}). Skipping.")
                        continue
                except ValueError:
                    print(f"Invalid expiration_date format for {candidate.get('id')}. Proceeding anyway.")
            
            # Found a valid one!
            link_obj = candidate
            break
        
        # Save the file without the extracted (or expired) links
        with open(self.links_file, 'w', encoding='utf-8') as f:
            json.dump(links_data, f, indent=2)
            
        if not link_obj:
            return "No valid content available", None
            
        post_id = link_obj.get("id")
        url = link_obj.get("url", "")
        image_name = link_obj.get("image")
        
        # 2. Match by ID in texts.json
        body_text = "Check out our latest update!"
        if os.path.exists(self.texts_file):
            with open(self.texts_file, 'r', encoding='utf-8') as f:
                try:
                    texts_data = json.load(f)
                    # Find the text object with matching id
                    for text_obj in texts_data:
                        if text_obj.get("id") == post_id:
                            body_text = text_obj.get("body", body_text)
                            break
                except json.JSONDecodeError:
                    pass
                    
        # 3. Format Template
        post_template = "{body}\n\n{link}"  # Default fallback
        if os.path.exists(self.template_file):
            with open(self.template_file, 'r', encoding='utf-8') as f:
                post_template = f.read()

        # Safely handle the formatting so if {link} or {body} is missing it still works
        try:
            final_text = post_template.format(body=body_text, link=url)
        except KeyError:
            # Fallback if template is malformed (e.g., contains unescaped curly braces)
            final_text = f"{body_text}\n\n{url}"
            
        # 4. Resolve Image
        image_path = None
        if image_name:
            full_image_path = os.path.join(self.images_dir, image_name)
            if os.path.exists(full_image_path):
                image_path = full_image_path
                
        return final_text, image_path

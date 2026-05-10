import os
import json
import random
from typing import Tuple, Optional
from src.interfaces.content_provider import IContentProvider

class FileContentProvider(IContentProvider):
    def __init__(self):
        # Account for being in src/infrastructure now (2 levels deep to root)
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
        self.texts_file = os.path.join(self.data_dir, 'texts.json')
        self.links_file = os.path.join(self.data_dir, 'links.txt')
        self.images_dir = os.path.join(self.data_dir, 'images')

    def _load_random_text(self) -> str:
        if not os.path.exists(self.texts_file):
            return "Check out our latest update!"
        with open(self.texts_file, 'r', encoding='utf-8') as f:
            try:
                texts = json.load(f)
                if texts:
                    return random.choice(texts)
            except json.JSONDecodeError:
                pass
        return "Check out our latest update!"

    def _pop_link(self) -> str:
        if not os.path.exists(self.links_file):
            return ""
        with open(self.links_file, 'r', encoding='utf-8') as f:
            links = [line.strip() for line in f if line.strip()]
        if not links:
            return ""
        selected_link = links.pop(0)
        with open(self.links_file, 'w', encoding='utf-8') as f:
            for link in links:
                f.write(f"{link}\n")
        return selected_link

    def _get_random_image(self) -> Optional[str]:
        if not os.path.exists(self.images_dir):
            return None
        images = [f for f in os.listdir(self.images_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if not images:
            return None
        image_name = random.choice(images)
        return os.path.join(self.images_dir, image_name)

    def get_post_content(self) -> Tuple[str, Optional[str]]:
        text = self._load_random_text()
        link = self._pop_link()
        image_path = self._get_random_image()
        
        final_text = text
        if link:
            final_text += f"\n\nFind out more here: {link}"
            
        return final_text, image_path

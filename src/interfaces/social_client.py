from typing import Protocol, Optional

class ISocialClient(Protocol):
    def publish_post(self, text: str, image_path: Optional[str] = None) -> bool:
        """
        Publishes a post to the social media platform.
        
        Args:
            text (str): The text content of the post.
            image_path (Optional[str]): Path to the image file to attach, if any.
            
        Returns:
            bool: True if the post was successfully published, False otherwise.
        """
        ...

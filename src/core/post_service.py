from src.interfaces.content_provider import IContentProvider
from src.interfaces.social_client import ISocialClient

class PostService:
    def __init__(self, content_provider: IContentProvider, social_client: ISocialClient, dry_run: bool = False):
        self.content_provider = content_provider
        self.social_client = social_client
        self.dry_run = dry_run

    def create_and_publish_post(self) -> bool:
        """Assembles the post text, link, and image using the provider, then publishes it."""
        print("Starting post creation process...")
        
        # 1. Load contents via provider
        text, image_path, metadata = self.content_provider.get_post_content()
        
        if text == "No valid content available" or text == "No content available":
            print(text)
            return False

        print(f"Prepared Text:\n{text}")
        print(f"Selected Image: {image_path}")
        if metadata:
            print(f"Metadata: {metadata}")

        # 2. Dry-run mode: show the post but do NOT publish
        if self.dry_run:
            print("\n" + "=" * 50)
            print("🔶 DRY RUN MODE — Post was NOT published.")
            print("=" * 50)
            print("The post above is exactly what would be sent to LinkedIn.")
            print("Set DRY_RUN=false in .env or remove --dry-run to publish for real.")
            return True

        # 3. Publish via social client
        success = self.social_client.publish_post(text, image_path, metadata)
        
        if success:
            self.content_provider.mark_as_published()
            print("Content marked as successfully published.")
        else:
            print("Post failed. Content was not deleted from the queue.")
            
        return success

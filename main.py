import time
import schedule
from src.config import POSTING_TIMES, MAX_POSTS_PER_DAY
from src.infrastructure.file_content_provider import FileContentProvider
from src.infrastructure.linkedin_client import LinkedInClient
from src.core.post_service import PostService

def job():
    print("Running scheduled post creation...")
    
    # Dependency Injection
    content_provider = FileContentProvider()
    social_client = LinkedInClient()
    post_service = PostService(content_provider, social_client)
    
    success = post_service.create_and_publish_post()
    
    if success:
        print("Post published successfully via schedule.")
    else:
        print("Failed to publish post via schedule.")

def main():
    print("Starting LinkedIn Auto Poster Scheduler...")
    print(f"Configured posting times: {POSTING_TIMES}")
    print(f"Max posts per day: {MAX_POSTS_PER_DAY} (Note: currently scheduling by specific times)")
    
    for posting_time in POSTING_TIMES:
        time_str = posting_time.strip()
        if time_str:
            print(f"Scheduling job for {time_str}")
            schedule.every().day.at(time_str).do(job)
            
    if not schedule.jobs:
        print("No valid posting times configured. Exiting.")
        return

    print("Scheduler is now running. Waiting for the next scheduled time...")
    
    # Run the job once immediately upon startup
    print("Executing initial run on startup...")
    job()
    
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()

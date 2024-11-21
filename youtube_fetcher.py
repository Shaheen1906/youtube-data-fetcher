
import json
import pandas as pd
from googleapiclient.discovery import build
from urllib.parse import urlparse
import logging
import isodate

# Initialize logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

with open('config.json') as config_file:
  config = json.load(config_file)

API_KEY = config['API_KEY']
YOUTUBE_API_SERVICE_NAME = config['YOUTUBE_API_SERVICE_NAME']
YOUTUBE_API_VERSION = config['YOUTUBE_API_VERSION']


# Utility functions
def extract_channel_id(youtube, channel_url):
    """Extract channel ID from the handle-based URL."""
    try:
        # Extract handle from the URL
        parsed_url = urlparse(channel_url)
        handle = parsed_url.path.strip("/")
        
        if not handle.startswith("@"):
            raise ValueError("The provided URL does not contain a valid YouTube handle.")
        
        # Use the search endpoint to find the channel
        response = youtube.search().list(
            part="snippet",
            q=handle,
            maxResults=1,
            type="channel"
        ).execute()
        
        if not response.get("items"):
            raise ValueError("Channel not found for the given handle.")
        
        return response["items"][0]["snippet"]["channelId"]
    except Exception as e:
        logging.error(f"Error extracting channel ID: {e}")
        raise

def fetch_video_data(youtube, channel_id):
    """Fetch basic video data for a channel."""
    videos = []
    try:
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=50,  # Fetch 50 videos at a time
            type="video"
        )
        while request:
            response = request.execute()
            for item in response["items"]:
                video_id = item["id"]["videoId"]
                video_snippet = item["snippet"]
                videos.append({
                    "video_id": video_id,
                    "title": video_snippet["title"],
                    "description": video_snippet.get("description", ""),
                    "published_date": video_snippet["publishedAt"],
                    "thumbnail_url": video_snippet["thumbnails"]["default"]["url"]
                })
            request = youtube.search().list_next(request, response)
    except Exception as e:
        logging.error(f"Error fetching video data: {e}")
        raise
    return videos


def parse_duration(duration):
    """Convert ISO 8601 duration (PT2M2S) to HH:MM:SS format."""
    try:
        parsed_duration = isodate.parse_duration(duration)
        total_seconds = int(parsed_duration.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"  # Returns HH:MM:SS format
    except Exception as e:
        logging.error(f"Error parsing duration: {e}")
        return "00:00:00"  # Default value if parsing fails

def fetch_video_statistics(youtube, video_ids):
    """Fetch video statistics (views, likes, etc.)."""
    stats = []
    try:
        for i in range(0, len(video_ids), 50):  # YouTube API allows max 50 IDs per request
            response = youtube.videos().list(
                part="statistics,contentDetails",
                id=",".join(video_ids[i:i+50])
            ).execute()
            for item in response["items"]:
                stats.append({
                    "video_id": item["id"],
                    "view_count": item["statistics"].get("viewCount", 0),
                    "like_count": item["statistics"].get("likeCount", 0),
                    "comment_count": item["statistics"].get("commentCount", 0),
                    # "duration": item["contentDetails"]["duration"],
                     "duration": parse_duration(item["contentDetails"]["duration"]), 
                })
    except Exception as e:
        logging.error(f"Error fetching video statistics: {e}")
        raise
    return stats

def fetch_comments(youtube, video_id, max_comments=100):
    """Fetch comments and replies for a video."""
    comments = []
    try:
        request = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=100
        )
        while request and len(comments) < max_comments:
            response = request.execute()
            for item in response["items"]:
                # Top-level comment data
                top_comment = item["snippet"]["topLevelComment"]["snippet"]
                top_comment_text = top_comment["textDisplay"]
                top_comment_id = item["id"]
                
                # Append top-level comment
                comments.append({
                    "video_id": video_id,
                    "comment_id": top_comment_id,
                    "text": top_comment_text,
                    "author": top_comment["authorDisplayName"],
                    "published_date": top_comment["publishedAt"],
                    "like_count": top_comment["likeCount"],
                    "reply_to": None  # Top-level comments have no parent
                })
                
                # Append replies, if any
                if "replies" in item:
                    for reply in item["replies"]["comments"]:
                        reply_snippet = reply["snippet"]
                        comments.append({
                            "video_id": video_id,
                            "comment_id": reply["id"],
                            "text": reply_snippet["textDisplay"],
                            "author": reply_snippet["authorDisplayName"],
                            "published_date": reply_snippet["publishedAt"],
                            "like_count": reply_snippet["likeCount"],
                            # "reply_to": {
                            #     "id": top_comment_id,
                            #     "text": top_comment_text
                            # }
                            "reply_to":top_comment_text
                        })
            request = youtube.commentThreads().list_next(request, response)
    except Exception as e:
        logging.error(f"Error fetching comments: {e}")
        raise
    return comments


def save_to_excel(video_data, comment_data, filename="youtube_data.xlsx"):
    """Save fetched data to an Excel file."""
    try:
        with pd.ExcelWriter(filename, engine="openpyxl") as writer:
            pd.DataFrame(video_data).to_excel(writer, sheet_name="Video Data", index=False)
            pd.DataFrame(comment_data).to_excel(writer, sheet_name="Comments Data", index=False)
        logging.info(f"Data successfully saved to {filename}")
    except Exception as e:
        logging.error(f"Error saving data to Excel: {e}")
        raise

# Main script
def main(channel_url):
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)
        channel_id = extract_channel_id(youtube, channel_url)
        videos = fetch_video_data(youtube, channel_id)
        video_ids = [video["video_id"] for video in videos]
        stats = fetch_video_statistics(youtube, video_ids)
        
        # Merge video data with statistics
        for video in videos:
            video.update(next((stat for stat in stats if stat["video_id"] == video["video_id"]), {}))
        
        # Fetch comments for all videos
        all_comments = []
        for video_id in video_ids:
            all_comments.extend(fetch_comments(youtube, video_id))
        
        # Save data to Excel
        save_to_excel(videos, all_comments)
    except Exception as e:
        logging.error(f"An error occurred: {e}")

if __name__ == "__main__":
    channel_url = input("Enter the YouTube channel URL: ")
    main(channel_url)

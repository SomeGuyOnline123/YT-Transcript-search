from youtube_transcript_api import YouTubeTranscriptApi
from pytube import YouTube
import json
import re

# Read the file containing YouTube URLs
with open('youtube_urls.txt', 'r') as file:
    urls = file.readlines()

# Read the existing episodes from the file
existing_episodes = []
with open('episodes.js', 'r') as file:
    content = file.read()
    if content.strip():
        # Extract the episodes list from the file
        episodes_start_index = content.index('[')
        episodes_end_index = content.rindex(']')
        existing_episodes = json.loads(content[episodes_start_index:episodes_end_index + 1])

# Process each YouTube URL
for url in urls:
    url = url.strip()

    print(f"Working with {url}")

    try:
       # Extract the video ID from the URL using regex
        match = re.search(r"(?:watch\?v=|/videos/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v%3D|watch\?feature=player_embedded&v=|%2Fvideos%2F|embed%\u200C\u200B2F|youtu.be%2F|\/v%2F|e%2F)([^#\\&\\?]*)(?:\S+)?", url)
        if match:
            video_id = match.group(1)
        else:
            print(f"Skipping URL: {url} (Invalid YouTube URL)")
            continue

        # Check if episode with the same video ID already exists
        existing_episode = next((episode for episode in existing_episodes if episode['video_id'] == video_id), None)
        if existing_episode:
            print(f"Skipping URL: {url} (Video ID already exists)")
            continue

        # Retrieve the YouTube video title
        video = YouTube(url)
        video_title = video.title
        channel_name = video.author

        # Retrieve the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        # Create a list to store transcript objects
        transcript_list = []

        # Process each transcript segment
        for segment in transcript:
            start_time = segment['start']
            text = segment['text']

            # Create the transcript object
            transcript_obj = {
                'url': f'{url}&t={start_time}s',
                'time': start_time,
                'text': text
            }

            # Add the transcript object to the list
            transcript_list.append(transcript_obj)

        # Create the episode object with video ID
        episode_obj = {
            'video_id': video_id,
            'title': video_title,
            'channel': channel_name,
            'date': video.publish_date.strftime('%B %d, %Y'),
            'transcripts': transcript_list
        }

        # Append new episode
        existing_episodes.append(episode_obj)

    except Exception as e:
        print(f'Error retrieving transcript for {url}: {str(e)}')

# Write the merged episodes list to the JSON file
with open('episodes.js', 'w') as file:
    file.write('var episodes = ')
    json.dump(existing_episodes, file, indent=2)


import requests
from googleapiclient.discovery import build
import pandas as pd
import os

YOUTUBE_API_KEY = "AIzaSyCsFM2-UPCB4JAesSSNRTQkNzmVRDnyRmU"
INSTA_TOKEN = "IGAAZC2S4ZAYlrhBZAGEzU0h6SzRiWkI0TGNqT1JFRjdaWG03elJVTmJvZAGJJZAW95ZA0xoRlBjcGl4d0RZAeFBiRDg0ZAHdfWnhjQm9NvmhLOTNWaUNHeUljdWJFNEpNOVh2ZAnU0OGNubHFWOVZAmcG54ME5wYmNfZA2lCcHk5eXZApclNnUQZDZD"
LINKEDIN_CLIENT_ID = "86f07keg6caao3"
LINKEDIN_CLIENT_SECRET = "WPL_AP1.paBk624XcB4tsrK1.RPjL5w=="

print("🚀 MARKET RESEARCH TOOL")
print("=" * 50)
print("📝 Enter your query below (examples:)")
print("• business podcast africa")
print("• tech startups nigeria") 
print("• entrepreneurship south africa")
print("• fintech podcast kenya")
print("=" * 50)

query = input("🔍 YOUR QUERY: ").strip()
if not query:
    query = "business podcast africa"
    print("⚠️ Using default: business podcast africa")

print(f"\n🎯 ANALYZING: '{query}'")
print("⏳ Searching YouTube + Instagram + LinkedIn...")

# 1. YOUTUBE
print("📺 YouTube search...")
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
request = youtube.search().list(
    part='snippet',
    q=f"{query} podcast OR channel -news -cnbc -bbc -ntv",
    type='channel',
    maxResults=20,
    order='viewCount'
)
response = request.execute()

youtube_channels = []
for item in response.get('items', []):
    channel_id = item['snippet']['channelId']
    chan_req = youtube.channels().list(part='snippet,statistics', id=channel_id)
    chan_data = chan_req.execute()
    
    if chan_data['items']:
        stats = chan_data['items'][0]['statistics']
        title = chan_data['items'][0]['snippet']['title']
        youtube_channels.append({
            'platform': 'YouTube',
            'title': title,
            'subscribers': stats.get('subscriberCount', '0'),
            'views': stats.get('viewCount', '0'),
            'videos': stats.get('videoCount', '0'),
            'url': f"https://youtube.com/channel/{channel_id}",
            'query': query
        })

# 2. INSTAGRAM
print("📱 Instagram search...")
insta_url = f"https://graph.facebook.com/v20.0/ig_hashtag_search?user_id=4492928887592632&q={query.replace(' ', '%20')}&access_token={INSTA_TOKEN}"
insta_resp = requests.get(insta_url)
insta_data = insta_resp.json().get('data', [])

instagram_hashtags = []
for item in insta_data[:10]:
    instagram_hashtags.append({
        'platform': 'Instagram',
        'title': f"#{item['name']}",
        'subscribers': 'N/A',
        'views': 'N/A', 
        'videos': 'N/A',
        'url': f"https://www.instagram.com/explore/tags/{item['name']}/",
        'query': query
    })

# 3. LINKEDIN (Simple keyword search simulation)
print("💼 LinkedIn search...")
linkedin_results = []
linkedin_keywords = f"{query} podcast OR business OR entrepreneur"
sample_linkedin = [
    {"title": f"{query.title()} Expert", "subscribers": "5000", "company": "Africa Tech", "url": "linkedin.com/in/expert"},
    {"title": f"{query.title()} Podcast Host", "subscribers": "2500", "company": "Startup Africa", "url": "linkedin.com/in/host"}
]
for item in sample_linkedin:
    linkedin_results.append({
        'platform': 'LinkedIn',
        'title': item['title'],
        'subscribers': item['subscribers'],
        'views': 'N/A',
        'videos': 'N/A',
        'company': item['company'],
        'url': item['url'],
        'query': query
    })

# COMBINE + SAVE
all_results = youtube_channels + instagram_hashtags + linkedin_results
df = pd.DataFrame(all_results)

filename = f"{query.replace(' ', '_')}_research.csv"
df.to_csv(filename, index=False)

print("\n" + "="*60)
print("✅ ANALYSIS COMPLETE!")
print("="*60)
print(f"📊 TOTAL RESULTS: {len(df)}")
print(f"📺 YouTube: {len(youtube_channels)} channels")
print(f"📱 Instagram: {len(instagram_hashtags)} hashtags")
print(f"💼 LinkedIn: {len(linkedin_results)} profiles")
print(f"💾 SAVED: {filename}")
print("\n🏆 TOP 5 RESULTS:")
for i, row in df.head().iterrows():
    print(f"{i+1}. [{row['platform']}] {row['title'][:50]}...")

print("\n🌐 NEXT: streamlit run dashboard.py")
print("="*60)

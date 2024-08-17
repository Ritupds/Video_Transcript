import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a video summarizer. You will be taking the transcript text from multiple videos and summarizing the entire content,
providing the important topics of the week in two or three lines. Give important notes too, if required. Please provide the summary: """


def extract_transcripts(youtube_urls):
    all_transcripts = []
    for url in youtube_urls:
        try:
            # Extract video ID from the URL
            if "youtu.be" in url:
                video_id = url.split("/")[-1].split("?")[0]
            elif "youtube.com" in url:
                video_id = url.split("v=")[1].split("&")[0]
            else:
                raise ValueError("Invalid YouTube URL")
            
            # Fetch transcript for the video ID
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcript_text = " ".join([i['text'] for i in transcript])
            all_transcripts.append(transcript_text)
        except Exception as e:
            st.error(f"Error fetching transcript for URL {url}: {str(e)}")
    
    # Concatenate all transcripts into one string
    combined_transcript = " ".join(all_transcripts)
    return combined_transcript

def generate_summary(transcript_text, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt + transcript_text)
    return response.text

st.title("YouTube Transcript Summarizer")
youtube_urls = st.text_area("Enter YouTube video URLs (one per line):").splitlines()

if st.button("Summarize"):
    if youtube_urls:
        combined_transcript = extract_transcripts(youtube_urls)
        if combined_transcript:
            summary = generate_summary(combined_transcript, prompt)
            st.write(summary)


# week 1 python prog links for testing
"""https://youtu.be/8ndsDXohLMQ?si=_XMkEBg-ycBvQUfW
https://youtu.be/NgZZ0HIUqbs?si=cnHY_SGz_2W-trGc
https://youtu.be/As7_aq6XGfI?si=qscajhevDZ_2T3Zg
https://youtu.be/Yg6xzi2ie5s?si=r_plPcbtCE3QIqJr
https://youtu.be/ruQb8jzkGyQ?si=tBxrBkFYBeJt8OgX
https://youtu.be/tDaXdoKfX0k?si=D-B4yM4_QPYrnq_g
https://youtu.be/8n4MBjuDBu4?si=1y51PqR9h2cO9wHL
https://youtu.be/xQXxufhEJHw?si=xO-abweGW5apgQdc
https://youtu.be/8pu73HKzNOE?si=VcVZmPoHg7AAa5an
https://youtu.be/Y53K9FFu97Q?si=mrZlH-J47GFRuvhH
https://youtu.be/sS89tiDuqoM?si=MYK7k1ORwXhWZ7Qe
https://youtu.be/e45MVXwya7A?si=xG0PrfUA3bTfEwtN
https://youtu.be/_Ccezy5hlc8?si=5xO7hyXv-ODct_Ps"""
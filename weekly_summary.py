import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are a video summarizer. You will be taking the transcript text from multiple videos and summarizing the entire content,
providing the detailed summary in points within 300 words. Please provide the summary: """


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

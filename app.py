import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
import google.generativeai as genai

from youtube_transcript_api import YouTubeTranscriptApi
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

prompt = """You are video summarizer. You will be taking the transcript text and summarizing the entire video and 
providing the important summary in points within 300 words. Please provide the summary : """


def extract_transcript(youtube_video_url):
    try:
        if "youtu.be" in youtube_video_url:
            video_id = youtube_video_url.split("/")[-1].split("?")[0]
        elif "youtube.com" in youtube_video_url:
            video_id = youtube_video_url.split("v=")[1].split("&")[0]
        else:
            raise ValueError("Invalid YouTube URL")
        
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([i['text'] for i in transcript_text])
        return transcript_text
    except Exception as e:
        raise e



def generate_gemini_content(transcript_text,prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript_text)
    return response.text

st.title("Youtube Transcript Summarizer")
youtube_url = st.text_input("Enter the youtube video url:") 

if st.button("Summarize"):
    transcript_text = extract_transcript(youtube_url)

    if transcript_text:
        summary = generate_gemini_content(transcript_text,prompt)
        st.write(summary)

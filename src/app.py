try:
    import os
    import time
    import json
    from PIL import Image # type: ignore
    import io
    from pytube import YouTube # type: ignore
    from dotenv import load_dotenv # type: ignore 
    import google.generativeai as genai # type: ignore 
    import streamlit as st # type: ignore
    from youtube_transcript_api import YouTubeTranscriptApi # type: ignore
    from langchain_core.messages import AIMessage, HumanMessage # type: ignore
except Exception as e:
    print(f"An error occurred: {e}")
MEDIA_FOLDER = 'medias'
SUMMARY_PROMPT = """
You are a YouTube video summarizer. You will take the transcript text and summarize the entire video, providing the important points within 250 words. Please provide the summary of the text given here:
"""
IMAGE_PROMPT = """
You are an AI image analyzer. Analyze the given image and provide a description and insights about it within 150 words.
"""
VIDEO_PROMPT = """
You are a video analyzer. Analyze the given video and provide a description and insights about it within 250 words.
"""
load_dotenv()

# Initialize default model and parameters
DEFAULT_MODEL = "gemini-1.5-flash"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_OUTPUT_TOKENS = 5000

def save_uploaded_file(uploaded_file):
    file_path = os.path.join(MEDIA_FOLDER, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.read())
    return file_path

def process_video(video_path):
    st.write(f"Processing video: {video_path}")
    video_file = genai.upload_file(path=video_path)
    while video_file.state.name == "PROCESSING":
        with st.spinner("Waiting for video to be processed..."):
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

    if video_file.state.name == "FAILED":
        raise ValueError("Video processing failed")

    prompt = VIDEO_PROMPT
    response = genai.GenerativeModel(model_name=DEFAULT_MODEL).generate_content([prompt, video_file], request_options={"timeout": 600})

    st.success('Video processing complete')
    st.subheader("Video Insights")
    st.info(response.text)
    genai.delete_file(video_file.name)

def process_image(image_path):
    st.write(f"Processing image: {image_path}")
    image_file = genai.upload_file(path=image_path)
    while image_file.state.name == "PROCESSING":
        with st.spinner("Waiting for image to be processed..."):
            time.sleep(10)
            image_file = genai.get_file(image_file.name)

    if image_file.state.name == "FAILED":
        raise ValueError("Image processing failed")

    prompt = IMAGE_PROMPT
    response = genai.GenerativeModel(model_name=DEFAULT_MODEL).generate_content([prompt, image_file], request_options={"timeout": 600})

    st.success('Image processing complete')
    st.subheader("Image Insights")
    st.info(response.text)
    genai.delete_file(image_file.name)

def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, languages=['en', 'hi'])
        transcript = " ".join([item["text"] for item in transcript_list])
        return transcript, video_id
    except Exception as e:
        print(f"An error occurred: {e}")

def generate_gemini_content(transcript_text, prompt, max_output_tokens, temperature=DEFAULT_TEMPERATURE):
    response = genai.GenerativeModel(model_name=DEFAULT_MODEL).generate_content(
        prompt + transcript_text,
        generation_config={
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
        }
    )
    return response.text

def get_response(user_query, chat_history="", max_output_tokens=DEFAULT_MAX_OUTPUT_TOKENS, temperature=DEFAULT_TEMPERATURE):
    try:
        prompt = f"You are a helpful assistant. Answer the following question considering the history of the conversation:\n {chat_history}\n User question: {user_query}"
        response = genai.GenerativeModel(model_name=DEFAULT_MODEL).generate_content(
            prompt, 
            generation_config={
                "max_output_tokens": max_output_tokens,
                "temperature": temperature
            }
        )
        return response.text
    except Exception as e:
        return f"An error occurred: {e}"

# Streamlit app setup
def app():
    if not os.path.exists(MEDIA_FOLDER):
        os.makedirs(MEDIA_FOLDER)
    
    st.set_page_config(page_title="AI Chatbot and Media Insights", page_icon="🤖",
                        menu_items={"About": "This is a Streamlit app that uses GenAI models for chatbot and media insights."})
    st.header('InsightBot Media 🤖', divider='rainbow')

    # Initialize chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Sidebar for API key configuration and settings
    st.sidebar.title("API Key and Settings")

    # API Key Configuration
    st.sidebar.info("To use the app, enter your GenAI API key in the text input field below.")
    st.sidebar.info("You can generate a new API key from your GenAI account.")
    api_key = st.sidebar.text_input("🔐 Enter your GenAI API key:", type="password")
    if api_key:
        try:
            genai.configure(api_key=api_key)
            st.sidebar.success("API key configured successfully!")
        except Exception as e:
            st.sidebar.error(f"Error configuring API key: {e}")
            return  # Stop execution if API key configuration fails
    else:
        st.error("Please enter your API key to use the app.")
        return  # Stop execution if no API key is provided

    # Model selection
    model_option = st.sidebar.selectbox("Select Model", ["gemini-1.5-flash", "gemini-pro", "gemini-1.5-pro"])
    global model
    model = genai.GenerativeModel(model_name=model_option)
    
    # Temperature adjustment
    temperature = st.sidebar.slider("Set Temperature", min_value=0.0, max_value=1.0, value=DEFAULT_TEMPERATURE, step=0.1)
    
    # Max output tokens
    max_output_tokens = st.sidebar.slider("Set Max Output Tokens", min_value=50, max_value=DEFAULT_MAX_OUTPUT_TOKENS, value=100)

    # Reset button
    def reset_conversation():
        if 'chat_history' in st.session_state and len(st.session_state.chat_history) > 0:
            st.session_state.pop('chat_history', None)
        # Delete all uploaded files
        for file in os.listdir(MEDIA_FOLDER):
            file_path = os.path.join(MEDIA_FOLDER, file)
            if os.path.isfile(file_path):
                os.remove(file_path)
                st.sidebar.info("All uploaded files removed from temporary location.")

    # Reset button
    st.sidebar.button(
        "🗑️ Reset Conversation", 
        on_click=reset_conversation,
    )

    # Sidebar for media options
    st.sidebar.title("📁 Media Options")
    option = st.sidebar.selectbox("Choose an option", ("Upload a video", "Provide a YouTube URL", "Upload an image"))

    if option in ["Upload a video", "Provide a YouTube URL", "Upload an image"]:
        # Clear chat history when a media option is selected
        st.session_state.chat_history = []

    if option == "Upload a video":
        uploaded_file = st.sidebar.file_uploader("Choose a video file", type=["mp4", "avi", "mov"])
        if uploaded_file is not None:
            file_path = save_uploaded_file(uploaded_file)
            st.video(file_path)  # Display the video on the main screen
            try:
                process_video(file_path)
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    st.sidebar.info("Video file removed from temporary location.")

    elif option == "Provide a YouTube URL":
        youtube_link = st.sidebar.text_input("Enter the YouTube video URL")
        if youtube_link:
            transcript_text, video_id = extract_transcript_details(youtube_link)
            st.video(f"https://www.youtube.com/watch?v={video_id}")

            if st.sidebar.button("Get Detailed Notes"):
                if transcript_text:
                    summary = generate_gemini_content(transcript_text, SUMMARY_PROMPT, max_output_tokens, temperature)
                    st.markdown("## Detailed Notes:")
                    st.write(summary)
                else:
                    st.sidebar.error("Transcript extraction failed")

    elif option == "Upload an image":
        uploaded_image = st.sidebar.file_uploader("Choose an image file", type=["jpg", "jpeg", "png"])
        if uploaded_image is not None:
            image_path = save_uploaded_file(uploaded_image)
            st.image(image_path, use_column_width=True)
            try:
                process_image(image_path)
            finally:
                if os.path.exists(image_path):
                    os.remove(image_path)
                    st.sidebar.info("Image file removed from temporary location.")

    # User input
    user_query = st.chat_input("Type your message here...")
    if user_query is not None and user_query != "":
        response = get_response(user_query, chat_history="\n".join([msg.content for msg in st.session_state.chat_history]), max_output_tokens=max_output_tokens, temperature=temperature)
        st.session_state.chat_history.append(HumanMessage(content=user_query))
        st.session_state.chat_history.append(AIMessage(content=response))

    # Display conversation
    for message in st.session_state.chat_history:
        if isinstance(message, AIMessage):
            with st.chat_message("AI"):
                st.write(message.content)
        elif isinstance(message, HumanMessage):
            with st.chat_message("Human"):
                st.write(message.content)
if __name__ == "__main__":
    app()

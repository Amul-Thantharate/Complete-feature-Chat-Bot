# AI Chatbot and Media Insights

## Overview

AI Chatbot and Media Insights is a versatile Streamlit application designed to provide insights from various types of media. It supports processing and analyzing YouTube videos, images, and user input through a chatbot interface. The application uses advanced Generative AI models to generate summaries, analyze images, and provide responses to user queries.

## Features

- **Video Processing**: Upload and analyze video files. Get insights and summaries of the video content.
- **YouTube Integration**: Provide a YouTube URL to extract transcripts, summarize the video, and watch the video directly in the app.
- **Image Analysis**: Upload images to receive descriptions and insights based on image content.
- **Chat Interface**: Interact with the AI chatbot to get responses based on the history of the conversation.
- **Text-to-Speech**: Read out the insights and chatbot responses using text-to-speech functionality.

## Installation

To run this application locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/Amul-Thantharate/ai-chatbot-media-insights.git
    cd ai-chatbot-media-insights
    ```

2. **Set Up a Virtual Environment** (optional but recommended):
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Create a `.env` File**:
    - Copy the example `.env` file:
        ```bash
        cp .env.example .env
        ```
    - Add your GenAI API key to the `.env` file:
        ```
        GENAI_API_KEY=your_genai_api_key_here
        ```

5. **Run the Application**:
    ```bash
    streamlit run app.py
    ```

## Usage

- **Upload a Video**: Use the sidebar to upload a video file and get insights about the video content.
- **Provide a YouTube URL**: Enter a YouTube URL to get a transcript, view the video, and obtain detailed notes.
- **Upload an Image**: Upload an image to get a description and insights.
- **Chat with the AI**: Interact with the AI chatbot by typing your message in the chat input box.

## Configuration

- **API Key**: Enter your GenAI API key in the sidebar to configure the application.
- **Model Selection**: Choose the desired model from the sidebar for text generation tasks.
- **Temperature**: Adjust the temperature parameter for text generation to control creativity.
- **Max Output Tokens**: Set the maximum number of tokens for generated responses.

## Example

1. **Upload Video**:
    - Choose a video file from your computer.
    - View the video on the main screen and get insights after processing.

2. **Provide YouTube URL**:
    - Enter a YouTube URL.
    - View the video and get detailed notes based on the transcript.

3. **Upload Image**:
    - Choose an image file.
    - View the image and receive an analysis of its content.

## Contributing

Contributions to the project are welcome! To contribute:

1. **Fork the Repository**.
2. **Create a New Branch**:
    ```bash
    git checkout -b feature/your-feature
    ```
3. **Make Your Changes**.
4. **Commit Your Changes**:
    ```bash
    git add .
    git commit -m "Add your message here"
    ```
5. **Push to Your Fork**:
    ```bash
    git push origin feature/your-feature
    ```
6. **Submit a Pull Request**.

Please ensure that your code adheres to the project's coding standards and includes tests for any new features.

## Contact

For any questions or feedback, please reach out to:

- **Email**: amulthantharate@gmail.com
- **GitHub Issues**: [Issues](https://github.com/Amul-Thantharate/)
- **LinkedIn**: [Amul Thantharate](https://www.linkedin.com/in/amul-thantharate/)


# Audio Transcription & Conversation App

A Streamlit application that transcribes audio files and enables conversational interaction with the content using AssemblyAI's API.

![App Demo](https://i.imgur.com/tbWmAja.gif)

## Features

- **Audio Transcription**: Transcribe audio from multiple sources (sample audio, URLs, or uploaded files)
- **AI-Powered Conversation**: Ask questions about the transcribed content and receive intelligent responses
- **Multiple Source Options**: Flexibility to work with various audio inputs
- **Full Transcript Access**: View the complete transcript for reference

## Requirements

- Python 3.7+
- Streamlit 1.24.0+
- AssemblyAI API key ([Get one here](https://support.assemblyai.com/articles/7562135267-how-to-get-your-api-key))

## Installation

1. Clone this repository:

   ```
   git clone https://github.com/yourusername/audio-transcription-app.git
   cd audio-transcription-app
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the app:
   ```
   streamlit run app.py
   ```

## Usage

1. Enter your AssemblyAI API key when prompted
2. Select an audio source (sample audio, URL, or upload your own file)
3. Click "Transcribe Audio" to process the audio
4. Once transcription is complete, you'll see a summary of the content
5. Ask questions about the transcribed content in the conversation interface
6. View the full transcript using the expander at the bottom

## How It Works

This app uses AssemblyAI's API to:

1. Transcribe the audio file into text
2. Generate an initial summary using Claude through AssemblyAI's Lemur
3. Enable follow-up questions about the content through a conversational interface

## Deployment

This app can be deployed on Streamlit Community Cloud:

1. Push to GitHub
2. Connect your repository on [share.streamlit.io](https://share.streamlit.io)
3. Deploy without any additional configuration

## License

[MIT](LICENSE)

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [AssemblyAI](https://www.assemblyai.com/) for transcription and AI conversation

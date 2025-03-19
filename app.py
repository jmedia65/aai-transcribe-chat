import streamlit as st
import assemblyai as aai

# Set page configuration
st.set_page_config(page_title="Audio Transcription App", layout="wide")

# Hide the menu button and other default elements
hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# API Key handling - in the main area for visibility
api_key_col1, api_key_col2, api_key_col3 = st.columns([1, 3, 1])

with api_key_col2:
    # App title
    st.title("Audio Transcription & Conversation")
    # API key input with password masking
    api_key = st.text_input(
        "Enter your AssemblyAI API Key to start", 
        type="password",
        help="Your API key is required to use the transcription service"
    )

    st.markdown(
        "<div style='padding-bottom:12px;'><a href='https://support.assemblyai.com/articles/7562135267-how-to-get-your-api-key' target='_blank'>Get your API key here</a></div>", 
        unsafe_allow_html=True
    )

# Initialize session state for audio source
if 'audio_source' not in st.session_state:
    st.session_state.audio_source = "Sample Audio"

# Check if API key is provided
if api_key:
    # Set the API key
    aai.settings.api_key = api_key
    
    # Sidebar for configuration
    with st.sidebar:
        st.header("Configuration")
        
        # Reset button at the top of sidebar
        if st.button("Reset App"):
            # Clear session state except for API key
            for key in list(st.session_state.keys()):
                if key != "api_key":  # Keep the API key
                    del st.session_state[key]
            # Immediately set the audio source back to default
            st.session_state.audio_source = "Sample Audio"
            # st.rerun()
            
        audio_source = st.radio(
            "Select audio source:",
            ["Sample Audio", "URL", "Upload File"],
            key="audio_source"
        )
        
        # Initialize audio_file as None to prevent errors
        audio_file = None
        
        if audio_source == "Sample Audio":
            audio_file = "https://storage.googleapis.com/aai-web-samples/architecture-call.mp3"
            st.info("Using sample audio file. Hear it below.")
            st.audio(audio_file)
        elif audio_source == "URL":
            audio_file = st.text_input("Enter audio URL:")
        elif audio_source == "Upload File":
            uploaded_file = st.file_uploader("Choose an audio file", type=["mp3", "wav", "m4a", "ogg"])
            if uploaded_file is not None:
                # Save uploaded file to use with AssemblyAI
                with open("temp_audio.mp3", "wb") as f:
                    f.write(uploaded_file.getbuffer())
                audio_file = "temp_audio.mp3"

    # Main container for transcript and conversation
    if 'transcription_done' not in st.session_state:
        st.session_state.transcription_done = False
        st.session_state.transcript = None
        st.session_state.conversation = []

    # Function to transcribe audio
    def transcribe_audio():
        with st.spinner('Transcribing audio... This may take a minute.'):
            try:
                transcriber = aai.Transcriber()
                transcript = transcriber.transcribe(audio_file)
                
                # Get initial summary
                with st.spinner('Generating summary...'):
                    result = transcript.lemur.task(
                        "I'm sending you a transcript of a video, please summarize it and I'll ask you questions about it.",
                        final_model=aai.LemurModel.claude3_5_sonnet    
                    )
                    
                st.session_state.transcript = transcript
                st.session_state.transcription_done = True
                st.session_state.conversation.append({"role": "assistant", "content": result.response})
                
                return result.response
            except Exception as e:
                st.error(f"Error during transcription: {str(e)}")
                return None

    st.markdown("""<hr style="height:10px;border:none;color:#333;background-color:#333;" /> """, unsafe_allow_html=True) 
    # Button to start transcription
    if not st.session_state.transcription_done:
        # Show the button only if a valid audio source is available
        if audio_file:
            if st.button("Transcribe Audio"):
                summary = transcribe_audio()
        else:
            # Show a message if no valid audio source is selected
            if audio_source == "URL":
                st.warning("Please enter a valid URL to transcribe")
            elif audio_source == "Upload File":
                st.warning("Please upload an audio file to transcribe")

    # Display the conversation and handle questions
    if st.session_state.transcription_done:
        # Display the conversation
        st.subheader("Conversation")
        
        for message in st.session_state.conversation:
            if message["role"] == "user":
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 15px;">
                    <div style="background-color: #4B5563; border-radius: 20px; padding: 2px 8px; margin-right: 8px;">👤</div>
                    <div style="background-color: #374151; border-radius: 10px; padding: 10px; max-width: 80%;">
                        <span style="font-weight: bold;">You:</span> {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display: flex; align-items: flex-start; margin-bottom: 15px;">
                    <div style="background-color: #4B5563; border-radius: 20px; padding: 2px 8px; margin-right: 8px;">🤖</div>
                    <div style="background-color: #1E293B; border-radius: 10px; padding: 10px; max-width: 80%;">
                        <span style="font-weight: bold;">Assistant:</span> {message['content']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        # Define a callback function to handle form submission
        def submit_question():
            if st.session_state.user_question:
                question = st.session_state.user_question
                
                # Add user question to conversation
                st.session_state.conversation.append({"role": "user", "content": question})
                
                # Get AI response
                with st.spinner('Generating response...'):
                    try:
                        result = st.session_state.transcript.lemur.task(
                            question, 
                            final_model=aai.LemurModel.claude3_5_sonnet
                        )
                        
                        # Add AI response to conversation
                        st.session_state.conversation.append({"role": "assistant", "content": result.response})
                    except Exception as e:
                        st.error(f"Error generating response: {str(e)}")
                
                # Clear the session state for next run
                st.session_state.user_question = ""
                
                # Rerun to update the conversation
                # st.rerun()
        
        # Get user question with on_change callback
        user_question = st.text_input(
            "Ask a question about the transcript:", 
            key="user_question"
        )
        
        # Button triggers the callback
        if st.button("Send", on_click=submit_question) and not user_question:
            # This handles the case when the button is clicked but the input is already empty
            pass

    # Display the raw transcript if available
    if st.session_state.transcription_done:
        with st.expander("View Raw Transcript"):
            st.markdown(st.session_state.transcript.text)

else:
    # Centered content when no API key is provided
    # Create a 3-column layout to effectively center the content
    left_spacer, center_content, right_spacer = st.columns([1, 3, 1])
    # Display demo message when no API key is entered
    with center_content:
        # Display the welcome info and preview here
        st.info("👆 Enter your AssemblyAI API Key to get started with automatic audio transcription and conversation.")
        
        st.markdown("""
        ### What you can do with this app:
        
        1. **Transcribe audio** from various sources:
           - Sample audio files
           - Audio URLs
           - Your own uploaded audio files
           
        2. **Engage in a conversation** about the transcribed content:
           - Get an automatic summary of the audio
           - Ask questions about the content
           - Receive AI-powered responses based on the audio
        
        3. **View the full transcript** for reference
        
        Enter your API key above to start using these features!
        """)
        
        # Demo preview in a nice container
        st.markdown("""
        <div style="border:2px solid #ddd; border-radius:10px; padding:10px; background-color:#f8f9fa;">
            <p style="text-align:center; font-style:italic; font-weight: bold; color:#555; margin-bottom:8px;">Demo Preview</p>
            <img src="https://i.imgur.com/tbWmAja.gif" width="100%" style="border-radius:5px;">
            <p style="text-align:center; color:#555; margin-top:8px;">Example of the app in action</p>
        </div>
        """, unsafe_allow_html=True)
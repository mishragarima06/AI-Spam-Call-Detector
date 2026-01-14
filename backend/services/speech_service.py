from google.cloud import speech_v1p1beta1 as speech
import io
import os

class SpeechToTextService:
    def __init__(self):
        """Initialize Google Cloud Speech-to-Text client"""
        try:
            self.client = speech.SpeechClient()
            print("✅ Speech-to-Text service initialized")
        except Exception as e:
            print(f"❌ Speech-to-Text initialization failed: {e}")
            raise
    
    def transcribe_audio(self, audio_file):
        """
        Convert audio to text using Google Speech-to-Text API
        
        Args:
            audio_file: Audio file object from request
            
        Returns:
            str: Transcribed text
        """
        try:
            # Read audio content
            content = audio_file.read()
            
            # Configure audio
            audio = speech.RecognitionAudio(content=content)
            
            # Configure recognition
            config = speech.RecognitionConfig(
                encoding=speech.RecognitionConfig.AudioEncoding.WEBM_OPUS,
                sample_rate_hertz=48000,
                language_code="en-IN",  # Primary: Indian English
                alternative_language_codes=["hi-IN", "ta-IN", "te-IN", "bn-IN", "mr-IN"],
                enable_automatic_punctuation=True,
                enable_word_time_offsets=False,
                model="latest_long",  # Best for longer audio
                use_enhanced=True  # Enhanced model for better accuracy
            )
            
            # Perform recognition
            response = self.client.recognize(config=config, audio=audio)
            
            # Extract transcript
            transcript = ""
            for result in response.results:
                transcript += result.alternatives[0].transcript + " "
            
            if not transcript.strip():
                return "No speech detected in audio"
            
            return transcript.strip()
            
        except Exception as e:
            print(f"Transcription error: {e}")
            raise Exception(f"Failed to transcribe audio: {str(e)}")
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Google Cloud
    GOOGLE_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
    GOOGLE_PROJECT_ID = os.getenv('GOOGLE_CLOUD_PROJECT')
    
    # Firebase
    FIREBASE_CREDENTIALS = os.getenv('FIREBASE_CREDENTIALS')
    
    # Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    
    # API
    HOST = os.getenv('API_HOST', '0.0.0.0')
    PORT = int(os.getenv('API_PORT', 5000))
    
    # Model paths
    DEEPFAKE_MODEL_PATH = 'models/deepfake_detector.h5'
    TEMP_UPLOAD_FOLDER = '/tmp/phantomx_uploads'
    
    # Supported languages
    SUPPORTED_LANGUAGES = ['en-IN', 'hi-IN', 'ta-IN', 'te-IN', 'bn-IN', 'mr-IN']
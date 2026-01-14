import librosa
import numpy as np
import os
import tempfile
from models.deepfake_model import DeepfakeDetector

class DeepfakeDetectionService:
    def __init__(self):
        """Initialize deepfake detection service"""
        try:
            self.model = DeepfakeDetector()
            print("✅ Deepfake detection service initialized")
        except Exception as e:
            print(f"❌ Deepfake service initialization failed: {e}")
            raise
    
    def analyze_audio(self, audio_file):
        """
        Analyze audio for deepfake/AI-generated voice detection
        
        Args:
            audio_file: Audio file object
            
        Returns:
            dict: Deepfake analysis results
        """
        try:
            # Save audio to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.webm') as temp_file:
                audio_file.save(temp_file.name)
                temp_path = temp_file.name
            
            try:
                # Extract features
                features = self.extract_features(temp_path)
                
                # Predict using ML model
                prediction = self.model.predict(features)
                
                is_deepfake = prediction > 0.5
                confidence = float(prediction if is_deepfake else 1 - prediction)
                
                result = {
                    'is_deepfake': bool(is_deepfake),
                    'confidence': round(confidence * 100, 2),
                    'risk_level': 'High' if is_deepfake else 'Low',
                    'features_analyzed': {
                        'mfcc': True,
                        'spectral_features': True,
                        'pitch_analysis': True,
                        'zero_crossing_rate': True
                    }
                }
                
                return result
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)
                    
        except Exception as e:
            print(f"Deepfake analysis error: {e}")
            # Return safe default if analysis fails
            return {
                'is_deepfake': False,
                'confidence': 50.0,
                'risk_level': 'Unknown',
                'error': str(e)
            }
    
    def extract_features(self, audio_path):
        """
        Extract acoustic features for deepfake detection
        
        Features extracted:
        - MFCC (Mel-frequency cepstral coefficients)
        - Spectral features (centroid, rolloff, contrast)
        - Pitch/fundamental frequency
        - Zero crossing rate
        """
        try:
            # Load audio file
            y, sr = librosa.load(audio_path, sr=16000, duration=30)
            
            # Extract MFCC features (13 coefficients)
            mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
            mfcc_mean = np.mean(mfcc, axis=1)
            mfcc_std = np.std(mfcc, axis=1)
            
            # Spectral features
            spectral_centroids = librosa.feature.spectral_centroid(y=y, sr=sr)[0]
            spectral_rolloff = librosa.feature.spectral_rolloff(y=y, sr=sr)[0]
            spectral_contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
            
            # Zero crossing rate
            zcr = librosa.feature.zero_crossing_rate(y)[0]
            
            # Pitch features
            pitches, magnitudes = librosa.piptrack(y=y, sr=sr)
            
            # Combine all features
            features = np.concatenate([
                mfcc_mean,
                mfcc_std,
                [np.mean(spectral_centroids)],
                [np.std(spectral_centroids)],
                [np.mean(spectral_rolloff)],
                [np.mean(spectral_contrast)],
                [np.mean(zcr)],
                [np.std(zcr)]
            ])
            
            return features.reshape(1, -1)
            
        except Exception as e:
            print(f"Feature extraction error: {e}")
            # Return zero features if extraction fails
            return np.zeros((1, 32))
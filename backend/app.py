from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import traceback
from config import Config
from services.speech_service import SpeechToTextService
from services.nlp_service import NLPService
from services.deepfake_service import DeepfakeDetectionService
from services.classification_service import CallClassificationService
from services.firebase_service import FirebaseService

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)
CORS(app)

# Ensure upload folder exists
os.makedirs(Config.TEMP_UPLOAD_FOLDER, exist_ok=True)

# Initialize services
try:
    speech_service = SpeechToTextService()
    nlp_service = NLPService()
    deepfake_service = DeepfakeDetectionService()
    classification_service = CallClassificationService()
    firebase_service = FirebaseService()
    print("✅ All services initialized successfully")
except Exception as e:
    print(f"❌ Error initializing services: {e}")
    traceback.print_exc()

@app.route('/', methods=['GET'])
def home():
    """Health check endpoint"""
    return jsonify({
        'status': 'online',
        'service': 'PhantomX API',
        'version': '1.0.0'
    })

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert audio to text using Google Speech-to-Text"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'Empty filename'}), 400
        
        # Transcribe audio
        transcript = speech_service.transcribe_audio(audio_file)
        
        return jsonify({
            'transcript': transcript,
            'status': 'success',
            'language_detected': 'en-IN'
        })
    except Exception as e:
        print(f"Speech-to-text error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect-intent', methods=['POST'])
def detect_intent():
    """Detect call intent using NLP"""
    try:
        data = request.json
        text = data.get('text', '')
        
        if not text:
            return jsonify({'error': 'No text provided'}), 400
        
        # Analyze intent
        intent_result = nlp_service.analyze_intent(text)
        
        return jsonify(intent_result)
    except Exception as e:
        print(f"Intent detection error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/detect-deepfake', methods=['POST'])
def detect_deepfake():
    """Detect if voice is AI-generated (deepfake)"""
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file provided'}), 400
        
        audio_file = request.files['audio']
        
        # Analyze for deepfake
        deepfake_result = deepfake_service.analyze_audio(audio_file)
        
        return jsonify(deepfake_result)
    except Exception as e:
        print(f"Deepfake detection error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/classify-call', methods=['POST'])
def classify_call():
    """Final call classification combining all analyses"""
    try:
        data = request.json
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Classify call
        result = classification_service.classify(
            transcript=data.get('transcript', ''),
            intent=data.get('intent', {}),
            deepfake=data.get('deepfake', {})
        )
        
        # Save to Firebase
        result_id = firebase_service.save_call_analysis(result)
        result['id'] = result_id
        
        return jsonify(result)
    except Exception as e:
        print(f"Classification error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get call analysis history"""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = firebase_service.get_call_history(limit=limit)
        
        return jsonify({
            'history': history,
            'count': len(history)
        })
    except Exception as e:
        print(f"History retrieval error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Submit user feedback for continuous learning"""
    try:
        data = request.json
        result_id = data.get('result_id')
        is_correct = data.get('is_correct')
        
        if result_id is None or is_correct is None:
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Save feedback
        firebase_service.save_feedback(result_id, is_correct)
        
        return jsonify({
            'status': 'success',
            'message': 'Feedback saved successfully'
        })
    except Exception as e:
        print(f"Feedback error: {e}")
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        stats = firebase_service.get_statistics()
        return jsonify(stats)
    except Exception as e:
        print(f"Stats error: {e}")
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    print(f"🚀 Starting PhantomX API on {Config.HOST}:{Config.PORT}")
    app.run(
        debug=Config.DEBUG,
        host=Config.HOST,
        port=Config.PORT
    )
from datetime import datetime
import numpy as np

class CallClassificationService:
    def __init__(self):
        """Initialize classification service"""
        print("✅ Classification service initialized")
    
    def classify(self, transcript, intent, deepfake):
        """
        Final call classification combining all analysis layers
        
        Args:
            transcript (str): Call transcript
            intent (dict): NLP intent analysis
            deepfake (dict): Deepfake detection results
            
        Returns:
            dict: Final classification result
        """
        try:
            # Get intent classification
            call_intent = intent.get('intent', 'unknown')
            intent_confidence = intent.get('confidence', 50)
            keywords = intent.get('keywords', [])
            
            # Get deepfake analysis
            is_deepfake = deepfake.get('is_deepfake', False)
            deepfake_confidence = deepfake.get('confidence', 50)
            
            # Determine final call type
            if call_intent == 'spam' or is_deepfake:
                call_type = 'spam'
                risk_level = 'High Risk'
                recommendation = 'Block and report this call immediately'
                
                if is_deepfake:
                    details = 'AI-generated voice detected. Likely voice cloning scam.'
                else:
                    details = 'Spam keywords and suspicious patterns detected.'
                    
            elif call_intent == 'business':
                call_type = 'business'
                risk_level = 'Safe'
                recommendation = 'Safe to answer - appears to be a legitimate delivery/business call'
                details = 'Delivery or business-related call detected.'
                
            else:
                call_type = 'safe'
                risk_level = 'Low Risk'
                recommendation = 'Proceed with caution'
                details = 'No clear spam indicators detected.'
            
            # Calculate overall confidence
            # Weight: Intent (60%), Deepfake (40%)
            overall_confidence = (intent_confidence * 0.6) + (deepfake_confidence * 0.4)
            
            # Determine specific intent message
            if call_type == 'spam':
                if 'otp' in keywords or 'verify' in keywords:
                    intent_message = 'Financial Fraud Attempt'
                elif 'prize' in keywords or 'lottery' in keywords:
                    intent_message = 'Prize/Lottery Scam'
                else:
                    intent_message = 'Suspicious Call Activity'
            elif call_type == 'business':
                if 'delivery' in keywords or 'order' in keywords:
                    intent_message = 'Delivery Service Call'
                else:
                    intent_message = 'Business Communication'
            else:
                intent_message = 'General Call'
            
            # Build final result
            result = {
                'type': call_type,
                'confidence': round(overall_confidence, 2),
                'risk_level': risk_level,
                'intent': intent_message,
                'recommendation': recommendation,
                'details': details,
                'keywords': keywords[:5],  # Top 5 keywords
                'timestamp': datetime.now().isoformat(),
                'analysis_layers': {
                    'speech_to_text': 'Completed',
                    'intent_detection': 'Completed',
                    'deepfake_analysis': 'Completed',
                    'final_classification': 'Completed'
                },
                'scores': {
                    'intent_confidence': intent_confidence,
                    'deepfake_confidence': deepfake_confidence,
                    'spam_indicators': intent.get('spam_indicators', 0),
                    'business_indicators': intent.get('business_indicators', 0)
                }
            }
            
            return result
            
        except Exception as e:
            print(f"Classification error: {e}")
            return {
                'type': 'unknown',
                'confidence': 0,
                'risk_level': 'Unknown',
                'intent': 'Analysis Failed',
                'recommendation': 'Unable to analyze call',
                'details': f'Error: {str(e)}',
                'keywords': [],
                'timestamp': datetime.now().isoformat()
            }
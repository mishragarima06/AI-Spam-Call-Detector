from google.cloud import language_v1
import re

class NLPService:
    def __init__(self):
        """Initialize Google Cloud Natural Language API client"""
        try:
            self.client = language_v1.LanguageServiceClient()
            print("✅ NLP service initialized")
        except Exception as e:
            print(f"❌ NLP initialization failed: {e}")
            raise
        
        # Spam/Scam indicators
        self.spam_keywords = [
            'otp', 'urgent', 'verify', 'bank account', 'blocked', 'suspend',
            'immediately', 'prize', 'lottery', 'congratulations', 'winner',
            'click here', 'limited time', 'act now', 'card details',
            'password', 'pin', 'cvv', 'update kyc', 'account suspended',
            'fraud', 'security alert', 'unauthorized', 'confirm identity',
            'aadhaar', 'pan card', 'refund', 'cashback', 'offer expires'
        ]
        
        # Delivery/Business call indicators
        self.business_keywords = [
            'delivery', 'order', 'package', 'courier', 'swiggy', 'zomato',
            'address', 'location', 'reaching', 'arriving', 'outside', 'gate',
            'apartment', 'pickup', 'drop', 'food', 'restaurant', 'amazon',
            'flipkart', 'parcel', 'shipment', 'tracking', 'delivered'
        ]
    
    def analyze_intent(self, text):
        """
        Analyze text to detect intent, sentiment, and extract entities
        
        Args:
            text (str): Transcribed call text
            
        Returns:
            dict: Analysis results including intent, keywords, sentiment
        """
        try:
            if not text or len(text.strip()) < 3:
                return {
                    'intent': 'unknown',
                    'keywords': [],
                    'sentiment_score': 0,
                    'confidence': 0
                }
            
            # Create document
            document = language_v1.Document(
                content=text,
                type_=language_v1.Document.Type.PLAIN_TEXT,
                language="en"
            )
            
            # Analyze sentiment
            sentiment_response = self.client.analyze_sentiment(
                request={'document': document}
            )
            sentiment = sentiment_response.document_sentiment
            
            # Analyze entities
            entities_response = self.client.analyze_entities(
                request={'document': document}
            )
            entities = entities_response.entities
            
            # Keyword-based classification
            text_lower = text.lower()
            
            spam_matches = [kw for kw in self.spam_keywords if kw in text_lower]
            business_matches = [kw for kw in self.business_keywords if kw in text_lower]
            
            spam_score = len(spam_matches)
            business_score = len(business_matches)
            
            # Determine intent
            if spam_score > business_score and spam_score > 0:
                intent = 'spam'
                confidence = min(90, 60 + (spam_score * 10))
            elif business_score > spam_score and business_score > 0:
                intent = 'business'
                confidence = min(90, 60 + (business_score * 10))
            else:
                intent = 'safe'
                confidence = 50
            
            # Collect all detected keywords
            detected_keywords = spam_matches + business_matches
            
            return {
                'intent': intent,
                'confidence': confidence,
                'keywords': detected_keywords[:10],  # Top 10 keywords
                'sentiment_score': round(sentiment.score, 3),
                'sentiment_magnitude': round(sentiment.magnitude, 3),
                'spam_indicators': spam_score,
                'business_indicators': business_score,
                'entities': [entity.name for entity in entities[:5]]
            }
            
        except Exception as e:
            print(f"NLP analysis error: {e}")
            return {
                'intent': 'unknown',
                'keywords': [],
                'sentiment_score': 0,
                'confidence': 0,
                'error': str(e)
            }
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

class FirebaseService:
    def __init__(self):
        """Initialize Firebase Admin SDK"""
        try:
            # Initialize Firebase if not already initialized
            if not firebase_admin._apps:
                cred = credentials.Certificate('database/firebase_config.json')
                firebase_admin.initialize_app(cred)
            
            self.db = firestore.client()
            print("✅ Firebase service initialized")
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")
            raise
    
    def save_call_analysis(self, result):
        """
        Save call analysis result to Firestore
        
        Args:
            result (dict): Analysis result
            
        Returns:
            str: Document ID
        """
        try:
            # Add server timestamp
            result['created_at'] = firestore.SERVER_TIMESTAMP
            
            # Save to 'call_analyses' collection
            doc_ref = self.db.collection('call_analyses').add(result)
            
            return doc_ref[1].id
            
        except Exception as e:
            print(f"Error saving to Firebase: {e}")
            return None
    
    def get_call_history(self, limit=50):
        """
        Retrieve call analysis history
        
        Args:
            limit (int): Maximum number of records to retrieve
            
        Returns:
            list: List of call analysis results
        """
        try:
            # Query recent analyses
            docs = self.db.collection('call_analyses')\
                .order_by('created_at', direction=firestore.Query.DESCENDING)\
                .limit(limit)\
                .stream()
            
            history = []
            for doc in docs:
                data = doc.to_dict()
                data['id'] = doc.id
                history.append(data)
            
            return history
            
        except Exception as e:
            print(f"Error retrieving history: {e}")
            return []
    
    def save_feedback(self, result_id, is_correct):
        """
        Save user feedback for model improvement
        
        Args:
            result_id (str): Analysis result ID
            is_correct (bool): Whether the analysis was correct
        """
        try:
            # Update document with feedback
            doc_ref = self.db.collection('call_analyses').document(result_id)
            doc_ref.update({
                'feedback': {
                    'is_correct': is_correct,
                    'submitted_at': firestore.SERVER_TIMESTAMP
                }
            })
            
            # Also save to feedback collection for training
            self.db.collection('feedback').add({
                'result_id': result_id,
                'is_correct': is_correct,
                'timestamp': firestore.SERVER_TIMESTAMP
            })
            
            print(f"✅ Feedback saved for result {result_id}")
            
        except Exception as e:
            print(f"Error saving feedback: {e}")
    
    def get_statistics(self):
        """Get overall statistics"""
        try:
            docs = self.db.collection('call_analyses').stream()
            
            total = 0
            spam_count = 0
            business_count = 0
            safe_count = 0
            
            for doc in docs:
                total += 1
                data = doc.to_dict()
                call_type = data.get('type', '')
                
                if call_type == 'spam':
                    spam_count += 1
                elif call_type == 'business':
                    business_count += 1
                elif call_type == 'safe':
                    safe_count += 1

            return {
                'total': total,
                'spam': spam_count,
                'business': business_count,
                'safe': safe_count
            }

        except Exception as e:
            print(f"Error retrieving statistics: {e}")
            return {
                'total': 0,
                'spam': 0,
                'business': 0,
                'safe': 0
            }
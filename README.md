# PhantomX – AI-Based Call Fraud & Deepfake Detection

# PROBLEM STATEMENT
The rapid growth of AI-based voice cloning and text-to-speech technologies has led to a surge in phone-based
financial frauds and impersonation scams. In India, multiple incidents-including cases from Hyderabad and
Lucknow-along with reports showing that over 80% of individuals have faced losses due to AI voice scams,
highlight the seriousness of this threat. Scammers can convincingly mimic voices of bank officials, family
members, or authorities, making real-time detection extremely difficult due to background noise and call
compression. Most existing solutions focus on video deepfakes or post-call analysis, leaving a critical gap in
real-time voice call security.

To address the rise of AI-based voice scams, we propose a Real-Time Deepfake Voice Call Detection System.

# SOLUTION OVERVIEW
AI Spam Call Detector is a prototype system that analyzes voice calls in real time to detect AI-generated, cloned, or suspicious voices and alerts the user instantly.

The system uses machine learning–based audio analysis, behavioral patterns, and signal-level features to classify calls as genuine or AI-generated.
MULTI LAYER AIDETECTION
LAYER 01- Speech-to-Text Analysis.
LAYER 02- Intent detection using NLP.
LAYER 03- Context And Behavior Analysis.
LAYER 04- User Feedback Learning.


# KEY FEATURES 
  -AI‑based Call Classification
            Automatically classifies calls into Spam, Delivery/Business, or Safe.
  -Context‑Aware Detection
            Understands call purpose using voice content, not just phone number.
  -Delivery Call Identification
            Accurately detects calls from Swiggy, Zomato, courier, etc., and avoids false spam alerts.
  -Speech‑to‑Text Analysis
            Converts call audio into text for intelligent analysis.
  -Keyword & Pattern Detection
            Identifies scam keywords (OTP, urgent, bank block) and delivery keywords (order, location).
  -User Feedback Learning
            Improves accuracy over time based on user feedback.
  -Real‑Time Alert Labeling
            Displays clear labels like Spam, Delivery Call, or Safe Call.

# SYSTEM ARCHIETECTURE
- Audio Input

     Live call audio (simulated)

     Uploaded call recordings (WAV/MP3)

-Preprocessing Layer

     Noise reduction

     Feature extraction (MFCC, pitch, spectral features)

-ML Detection Engine

    Trained model to detect AI-generated voice patterns

    Binary / multi-class classification

-Backend API

    Flask-based REST API

    Handles audio processing & prediction

-Frontend Dashboard

    User-friendly web interface

    Displays call status & confidence score

# TECH STACK 
-Frontend

    HTML / CSS / JavaScript

    (or React – if planned)

-Backend

    Python

    Flask (API framework)

-Machine Learning

     Python

    Librosa (audio feature extraction)

    NumPy / Pandas

    Scikit-learn / Deep Learning model (planned)

-Tools & Platforms

    GitHub (version control)

    VS Code

    Postman (API testing)

# WORKFLOW (PROTOTYPE)
  -User uploads or streams call audio

  -Audio is preprocessed and cleaned

  -Features are extracted from the voice

  -ML model analyzes authenticity

  -System returns:

  -Genuine / AI-generated

  -Confidence score

  -User receives alert if call is suspicious

# HOW TO RUNN THE CODE
  # Clone the repository
git clone https://github.com/your-username/AI-Spam-Call-Detector.git

# Go to project directory
cd AI-Spam-Call-Detector

# Install dependencies
pip install -r requirements.txt

# Run backend
python app.py

# FUTURE SCOPE

Live phone call integration

Mobile app (Android / iOS)

Telecom-level deployment

Multilingual voice detection

Integration with banking & law enforcement systems


# DISCLAIMER 
This project is a prototype built for hackathon purposes to demonstrate feasibility and concept. Real-world deployment would require telecom-level integrations and large-scale datasets.
  

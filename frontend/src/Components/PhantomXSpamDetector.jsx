import React, { useState, useRef, useEffect } from 'react';
import { Phone, Shield, AlertTriangle, CheckCircle, Mic, Upload, X, TrendingUp, MapPin, Globe } from 'lucide-react';

const PhantomXSpamDetector = () => {
  const [activeTab, setActiveTab] = useState('detector');
  const [isRecording, setIsRecording] = useState(false);
  const [audioFile, setAudioFile] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [callHistory, setCallHistory] = useState([]);
  const [feedback, setFeedback] = useState('');
  const [recordingTime, setRecordingTime] = useState(0);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const [audioChunks, setAudioChunks] = useState([]);
  const fileInputRef = useRef(null);
  const timerRef = useRef(null);

  // Simulated analysis function
  const analyzeCall = async (audio) => {
    setAnalyzing(true);
    setResult(null);

    // Simulate API processing time
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Generate random realistic results for demo
    const callTypes = [
      {
        type: 'spam',
        confidence: 92,
        keywords: ['urgent', 'OTP', 'bank account', 'verify immediately'],
        intent: 'Financial Fraud Attempt',
        recommendation: 'Block and report this call',
        riskLevel: 'High Risk',
        details: 'Detected scam keywords and suspicious urgency patterns'
      },
      {
        type: 'business',
        confidence: 88,
        keywords: ['delivery', 'order', 'address', 'location'],
        intent: 'Delivery Call',
        recommendation: 'Safe to answer',
        riskLevel: 'Safe',
        details: 'Legitimate delivery service call detected'
      },
      {
        type: 'safe',
        confidence: 95,
        keywords: ['meeting', 'appointment', 'confirm'],
        intent: 'Business Communication',
        recommendation: 'Safe to answer',
        riskLevel: 'Safe',
        details: 'Normal business communication detected'
      }
    ];

    const randomResult = callTypes[Math.floor(Math.random() * callTypes.length)];
    
    const analysisResult = {
      ...randomResult,
      timestamp: new Date().toLocaleString(),
      audioSource: audio.name || 'Live Recording',
      layers: {
        speechToText: 'Completed',
        intentDetection: 'Completed',
        contextAnalysis: 'Completed',
        behaviorPattern: 'Completed'
      }
    };

    setResult(analysisResult);
    setCallHistory(prev => [analysisResult, ...prev].slice(0, 10));
    setAnalyzing(false);
  };

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      setAudioFile(file);
      analyzeCall(file);
    }
  };

  const handleRecording = () => {
    if (!isRecording) {
      setIsRecording(true);
      setTimeout(() => {
        setIsRecording(false);
        analyzeCall({ name: 'Live Recording' });
      }, 5000);
    }
  };

  const submitFeedback = () => {
    if (feedback.trim()) {
      alert('Thank you for your feedback! This helps improve our AI model.');
      setFeedback('');
    }
  };

  const getRiskColor = (type) => {
    switch(type) {
      case 'spam': return 'bg-red-500';
      case 'business': return 'bg-blue-500';
      case 'safe': return 'bg-green-500';
      default: return 'bg-gray-500';
    }
  };

  const getRiskBorderColor = (type) => {
    switch(type) {
      case 'spam': return 'border-red-500';
      case 'business': return 'border-blue-500';
      case 'safe': return 'border-green-500';
      default: return 'border-gray-500';
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Header */}
      <div className="bg-black/30 backdrop-blur-md border-b border-white/10">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <Shield className="w-8 h-8 text-purple-400" />
              <div>
                <h1 className="text-2xl font-bold">PhantomX</h1>
                <p className="text-xs text-gray-400">AI-Powered Call Protection</p>
              </div>
            </div>
            <div className="flex space-x-2">
              <button
                onClick={() => setActiveTab('detector')}
                className={`px-4 py-2 rounded-lg transition ${
                  activeTab === 'detector'
                    ? 'bg-purple-600 text-white'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                Detector
              </button>
              <button
                onClick={() => setActiveTab('history')}
                className={`px-4 py-2 rounded-lg transition ${
                  activeTab === 'history'
                    ? 'bg-purple-600 text-white'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                History
              </button>
              <button
                onClick={() => setActiveTab('insights')}
                className={`px-4 py-2 rounded-lg transition ${
                  activeTab === 'insights'
                    ? 'bg-purple-600 text-white'
                    : 'bg-white/10 hover:bg-white/20'
                }`}
              >
                Insights
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Detector Tab */}
        {activeTab === 'detector' && (
          <div className="space-y-6">
            {/* Upload Section */}
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <h2 className="text-2xl font-bold mb-6 flex items-center">
                <Phone className="w-6 h-6 mr-2 text-purple-400" />
                Analyze Call Audio
              </h2>
              
              <div className="grid md:grid-cols-2 gap-4 mb-6">
                <button
                  onClick={handleRecording}
                  disabled={isRecording || analyzing}
                  className={`p-8 rounded-xl border-2 border-dashed transition ${
                    isRecording
                      ? 'border-red-500 bg-red-500/20 animate-pulse'
                      : 'border-purple-500 hover:border-purple-400 hover:bg-white/5'
                  } ${analyzing ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  <Mic className={`w-12 h-12 mx-auto mb-3 ${isRecording ? 'text-red-400' : 'text-purple-400'}`} />
                  <p className="font-semibold">
                    {isRecording ? 'Recording...' : 'Record Live Call'}
                  </p>
                  <p className="text-sm text-gray-400 mt-1">
                    Click to start 5-second demo recording
                  </p>
                </button>

                <button
                  onClick={() => fileInputRef.current?.click()}
                  disabled={analyzing}
                  className={`p-8 rounded-xl border-2 border-dashed border-purple-500 hover:border-purple-400 hover:bg-white/5 transition ${
                    analyzing ? 'opacity-50 cursor-not-allowed' : ''
                  }`}
                >
                  <Upload className="w-12 h-12 mx-auto mb-3 text-purple-400" />
                  <p className="font-semibold">Upload Audio File</p>
                  <p className="text-sm text-gray-400 mt-1">
                    MP3, WAV, or other audio formats
                  </p>
                </button>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="audio/*"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </div>

              {audioFile && (
                <div className="bg-black/30 rounded-lg p-4 mb-4">
                  <p className="text-sm text-gray-300">
                    Selected: {audioFile.name}
                  </p>
                </div>
              )}
            </div>

            {/* Analysis Progress */}
            {analyzing && (
              <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
                <h3 className="text-xl font-bold mb-6 text-center">Analyzing Call...</h3>
                <div className="space-y-4">
                  {['Speech-to-Text Conversion', 'Intent Detection (NLP)', 'Context Analysis', 'Behavior Pattern Check'].map((step, idx) => (
                    <div key={idx} className="flex items-center space-x-3">
                      <div className="w-6 h-6 rounded-full bg-purple-600 animate-pulse"></div>
                      <p className="text-gray-300">{step}</p>
                    </div>
                  ))}
                </div>
                <div className="mt-6 h-2 bg-gray-700 rounded-full overflow-hidden">
                  <div className="h-full bg-gradient-to-r from-purple-600 to-pink-600 animate-pulse" style={{ width: '70%' }}></div>
                </div>
              </div>
            )}

            {/* Results */}
            {result && !analyzing && (
              <div className={`bg-white/10 backdrop-blur-md rounded-2xl p-8 border-2 ${getRiskBorderColor(result.type)}`}>
                <div className="flex items-start justify-between mb-6">
                  <div>
                    <h3 className="text-2xl font-bold mb-2">Analysis Complete</h3>
                    <p className="text-gray-400 text-sm">{result.timestamp}</p>
                  </div>
                  <div className={`px-4 py-2 rounded-full ${getRiskColor(result.type)} font-semibold`}>
                    {result.riskLevel}
                  </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6 mb-6">
                  <div className="bg-black/30 rounded-xl p-6">
                    <p className="text-gray-400 text-sm mb-2">Call Type</p>
                    <p className="text-2xl font-bold capitalize">{result.type}</p>
                  </div>
                  <div className="bg-black/30 rounded-xl p-6">
                    <p className="text-gray-400 text-sm mb-2">Confidence Score</p>
                    <p className="text-2xl font-bold">{result.confidence}%</p>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="bg-black/30 rounded-xl p-6">
                    <p className="text-gray-400 text-sm mb-2">Detected Intent</p>
                    <p className="text-lg font-semibold">{result.intent}</p>
                  </div>

                  <div className="bg-black/30 rounded-xl p-6">
                    <p className="text-gray-400 text-sm mb-2">Keywords Detected</p>
                    <div className="flex flex-wrap gap-2 mt-2">
                      {result.keywords.map((keyword, idx) => (
                        <span key={idx} className="px-3 py-1 bg-purple-600/50 rounded-full text-sm">
                          {keyword}
                        </span>
                      ))}
                    </div>
                  </div>

                  <div className="bg-black/30 rounded-xl p-6">
                    <p className="text-gray-400 text-sm mb-2">Recommendation</p>
                    <p className="text-lg">{result.recommendation}</p>
                  </div>

                  <div className="bg-black/30 rounded-xl p-6">
                    <p className="text-gray-400 text-sm mb-2">Analysis Details</p>
                    <p className="text-sm text-gray-300">{result.details}</p>
                  </div>
                </div>

                {/* Feedback Section */}
                <div className="mt-6 pt-6 border-t border-white/10">
                  <p className="text-sm font-semibold mb-3">Was this analysis accurate?</p>
                  <div className="flex space-x-3">
                    <button className="px-6 py-2 bg-green-600 hover:bg-green-700 rounded-lg transition">
                      ✓ Correct
                    </button>
                    <button className="px-6 py-2 bg-red-600 hover:bg-red-700 rounded-lg transition">
                      ✗ Incorrect
                    </button>
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {/* History Tab */}
        {activeTab === 'history' && (
          <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
            <h2 className="text-2xl font-bold mb-6">Call History</h2>
            {callHistory.length === 0 ? (
              <p className="text-gray-400 text-center py-12">No calls analyzed yet</p>
            ) : (
              <div className="space-y-4">
                {callHistory.map((call, idx) => (
                  <div key={idx} className={`bg-black/30 rounded-xl p-6 border-l-4 ${getRiskBorderColor(call.type)}`}>
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <p className="font-semibold capitalize">{call.type} Call</p>
                        <p className="text-sm text-gray-400">{call.timestamp}</p>
                      </div>
                      <span className={`px-3 py-1 rounded-full text-sm ${getRiskColor(call.type)}`}>
                        {call.confidence}%
                      </span>
                    </div>
                    <p className="text-sm text-gray-300">{call.intent}</p>
                    <div className="flex flex-wrap gap-2 mt-3">
                      {call.keywords.slice(0, 3).map((kw, i) => (
                        <span key={i} className="px-2 py-1 bg-white/10 rounded text-xs">
                          {kw}
                        </span>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {/* Insights Tab */}
        {activeTab === 'insights' && (
          <div className="space-y-6">
            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <h2 className="text-2xl font-bold mb-6 flex items-center">
                <TrendingUp className="w-6 h-6 mr-2 text-purple-400" />
                Fraud Activity Insights
              </h2>
              <div className="grid md:grid-cols-3 gap-6">
                <div className="bg-black/30 rounded-xl p-6 text-center">
                  <p className="text-4xl font-bold text-red-400 mb-2">127</p>
                  <p className="text-gray-400">Spam Calls Blocked</p>
                </div>
                <div className="bg-black/30 rounded-xl p-6 text-center">
                  <p className="text-4xl font-bold text-green-400 mb-2">89%</p>
                  <p className="text-gray-400">Detection Accuracy</p>
                </div>
                <div className="bg-black/30 rounded-xl p-6 text-center">
                  <p className="text-4xl font-bold text-blue-400 mb-2">43</p>
                  <p className="text-gray-400">Delivery Calls Identified</p>
                </div>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <h2 className="text-xl font-bold mb-6 flex items-center">
                <MapPin className="w-5 h-5 mr-2 text-purple-400" />
                Regional Scam Trends
              </h2>
              <div className="space-y-4">
                <div className="bg-black/30 rounded-xl p-4 flex items-center justify-between">
                  <div>
                    <p className="font-semibold">Mathura, UP</p>
                    <p className="text-sm text-gray-400">Your location</p>
                  </div>
                  <span className="px-3 py-1 bg-yellow-600 rounded-full text-sm">Medium Risk</span>
                </div>
                <p className="text-sm text-gray-400">
                  ⚠️ 15% increase in financial fraud calls detected in your region this week
                </p>
              </div>
            </div>

            <div className="bg-white/10 backdrop-blur-md rounded-2xl p-8 border border-white/20">
              <h2 className="text-xl font-bold mb-6 flex items-center">
                <Globe className="w-5 h-5 mr-2 text-purple-400" />
                Multi-Language Support
              </h2>
              <p className="text-gray-300 mb-4">
                PhantomX now supports Hindi and regional Indian languages for better accuracy
              </p>
              <div className="flex flex-wrap gap-2">
                {['English', 'Hindi', 'Tamil', 'Telugu', 'Bengali', 'Marathi'].map((lang, idx) => (
                  <span key={idx} className="px-4 py-2 bg-purple-600/50 rounded-lg text-sm">
                    {lang}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-black/30 backdrop-blur-md border-t border-white/10 mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6 text-center text-gray-400 text-sm">
          <p>PhantomX - AI-Based Multi-Layer Call Spam Detection</p>
          <p className="mt-2">Powered by Google Cloud AI Technologies</p>
        </div>
      </div>
    </div>
  );
};

export default PhantomXSpamDetector;
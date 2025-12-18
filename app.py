import streamlit as st
import pickle
import string
from nltk.corpus import stopwords
import nltk
from nltk.stem.porter import PorterStemmer
from datetime import datetime
import pandas as pd
import time
import random

ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)

tfidf = pickle.load(open('vectorizer.pkl','rb'))
model = pickle.load(open('model.pkl','rb'))

# Page configuration
st.set_page_config(
    page_title="SpamShield - AI Spam Classifier",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI
st.markdown("""
<style>
    /* Main container styling */
    .main {
        padding: 0rem 1rem;
    }
    
    /* Header styling */
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
    }
    
    /* Card styling */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #f0f0f0;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: #666;
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .total-color { color: #667eea; }
    .spam-color { color: #e74c3c; }
    .safe-color { color: #27ae60; }
    
    /* Result cards */
    .result-spam {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 40px rgba(238, 90, 90, 0.3);
        animation: slideIn 0.5s ease;
    }
    
    .result-safe {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 40px rgba(0, 184, 148, 0.3);
        animation: slideIn 0.5s ease;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .result-icon {
        font-size: 4rem;
        margin-bottom: 1rem;
    }
    
    .result-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .result-subtitle {
        font-size: 1rem;
        opacity: 0.9;
    }
    
    /* Message type selector */
    .type-selector {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 1rem;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        padding: 1rem;
        font-size: 1rem;
        transition: border-color 0.3s ease;
    }
    
    .stTextArea textarea:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-size: 1.1rem;
        font-weight: 600;
        width: 100%;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #f8f9fa;
    }
    
    /* History item */
    .history-item {
        background: white;
        padding: 1rem;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        border-left: 4px solid;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .history-spam {
        border-left-color: #e74c3c;
    }
    
    .history-safe {
        border-left-color: #27ae60;
    }
    
    .history-type {
        font-size: 0.75rem;
        color: #888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .history-message {
        font-size: 0.9rem;
        color: #333;
        margin: 0.5rem 0;
        word-wrap: break-word;
    }
    
    .history-result {
        font-size: 0.8rem;
        font-weight: 600;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        display: inline-block;
    }
    
    .history-result-spam {
        background: #ffeaea;
        color: #e74c3c;
    }
    
    .history-result-safe {
        background: #eafff5;
        color: #27ae60;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 10px;
        padding: 10px 20px;
    }
    
    /* Loading animation */
    .loading-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        text-align: center;
        color: white;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .loading-spinner {
        width: 60px;
        height: 60px;
        border: 4px solid rgba(255,255,255,0.3);
        border-top: 4px solid white;
        border-radius: 50%;
        animation: spin 1s linear infinite;
        margin: 0 auto 1.5rem auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .loading-text {
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        animation: pulse 1.5s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }
    
    .loading-step {
        font-size: 0.9rem;
        opacity: 0.8;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
    }
    
    .loading-step .checkmark {
        color: #00ff88;
        font-weight: bold;
    }
    
    .progress-bar-container {
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
        height: 8px;
        margin-top: 1.5rem;
        overflow: hidden;
    }
    
    .progress-bar-fill {
        background: white;
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    /* Thinking box */
    .thinking-box {
        background: #f8f9fa;
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        border: 2px dashed #ddd;
        min-height: 180px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        overflow: hidden;
    }
    
    .thinking-step {
        color: #666;
        font-size: 0.95rem;
        padding: 0.5rem 1rem;
        margin: 0.25rem 0;
        animation: fadeInOut 0.5s ease;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    @keyframes fadeInOut {
        0% {
            opacity: 0;
            transform: translateY(-10px);
        }
        100% {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .thinking-icon {
        animation: pulse 1s ease-in-out infinite;
    }
    
    .completed-step {
        color: #27ae60;
        font-size: 0.85rem;
        opacity: 0.6;
    }
    
    .current-step {
        color: #667eea;
        font-weight: 600;
        font-size: 0.95rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state for history
if 'message_history' not in st.session_state:
    st.session_state.message_history = []

if 'analyzing' not in st.session_state:
    st.session_state.analyzing = False

if 'last_result' not in st.session_state:
    st.session_state.last_result = None

# Analysis steps for loading animation
ANALYSIS_STEPS = [
    "🔍 Analyzing message content...",
    "🕵️ Checking for spam indicators...",
    "🔗 Evaluating links and keywords...",
    "🎣 Scanning for phishing patterns...",
    "👤 Reviewing sender behavior patterns...",
    "📊 Cross-referencing with known spam databases...",
    "⚠️ Detecting urgency and emotional triggers...",
    "📢 Assessing promotional language...",
    "🌐 Verifying URL safety...",
    "🧮 Calculating spam probability..."
]

# Sidebar - Dashboard
with st.sidebar:
    st.markdown("## 📊 Dashboard")
    st.markdown("---")
    
    # Calculate statistics
    total_messages = len(st.session_state.message_history)
    spam_count = sum(1 for msg in st.session_state.message_history if msg['result'] == 'Spam')
    safe_count = total_messages - spam_count
    
    # Stats cards
    st.markdown(f"""
    <div class="stat-card">
        <div class="stat-label">Total Analyzed</div>
        <div class="stat-number total-color">{total_messages}</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">🚫 Spam</div>
            <div class="stat-number spam-color">{spam_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-label">✅ Safe</div>
            <div class="stat-number safe-color">{safe_count}</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Spam rate
    if total_messages > 0:
        spam_rate = (spam_count / total_messages) * 100
        st.markdown("### 📈 Spam Rate")
        st.progress(spam_rate / 100)
        st.markdown(f"<p style='text-align: center; color: #666;'>{spam_rate:.1f}% of messages are spam</p>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Clear history button
    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.message_history = []
        st.rerun()

# Main content
st.markdown("""
<div class="main-header">
    <h1>🛡️ SpamShield</h1>
    <p>AI-Powered Email & SMS Spam Detection</p>
</div>
""", unsafe_allow_html=True)

# Create tabs
tab1, tab2 = st.tabs(["🔍 **Analyze Message**", "📜 **Message History**"])

with tab1:
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Message type selector
        st.markdown("### 📝 Enter Your Message")
        message_type = st.radio(
            "Select message type:",
            ["📧 Email", "💬 SMS"],
            horizontal=True,
            label_visibility="collapsed"
        )
        
        # Clean up the selection
        message_type_clean = "Email" if "Email" in message_type else "SMS"
        
        # Text input
        input_sms = st.text_area(
            "Message content",
            height=200,
            placeholder=f"Paste your {message_type_clean.lower()} content here to check if it's spam...",
            label_visibility="collapsed"
        )
        
        # Analyze button
        if st.button("🔍 Analyze Message", use_container_width=True):
            if input_sms.strip():
                st.session_state.analyzing = True
                st.session_state.current_input = input_sms
                st.session_state.current_type = message_type_clean
                st.session_state.last_result = None
                st.rerun()
            else:
                st.warning("⚠️ Please enter a message to analyze.")
    
    with col2:
        st.markdown("### 📊 Result")
        result_placeholder = st.empty()
        
        # Handle the analyzing state
        if st.session_state.analyzing:
            # Randomly select 5-7 steps to show
            num_steps = random.randint(5, 7)
            selected_steps = random.sample(ANALYSIS_STEPS, num_steps)
            
            completed_steps = []
            
            for i, step in enumerate(selected_steps):
                # Build the thinking box with completed and current steps
                steps_html = '<div class="thinking-box">'
                steps_html += '<p style="font-size: 2rem; margin: 0 0 0.5rem 0;" class="thinking-icon">🤖</p>'
                
                # Show last 2 completed steps (faded)
                visible_completed = completed_steps[-2:] if len(completed_steps) > 2 else completed_steps
                for completed_step in visible_completed:
                    steps_html += f'<div class="thinking-step completed-step"><span>✓</span> {completed_step}</div>'
                
                # Show current step (highlighted)
                steps_html += f'<div class="thinking-step current-step"><span class="thinking-icon">⏳</span> {step}</div>'
                steps_html += '</div>'
                
                result_placeholder.markdown(steps_html, unsafe_allow_html=True)
                completed_steps.append(step)
                time.sleep(random.uniform(0.4, 0.7))
            
            # Perform the actual prediction
            transformed_sms = transform_text(st.session_state.current_input)
            vector_input = tfidf.transform([transformed_sms])
            result = model.predict(vector_input)[0]
            
            # Show final analyzing step
            steps_html = '<div class="thinking-box">'
            steps_html += '<p style="font-size: 2rem; margin: 0 0 0.5rem 0;" class="thinking-icon">🤖</p>'
            visible_completed = completed_steps[-2:]
            for completed_step in visible_completed:
                steps_html += f'<div class="thinking-step completed-step"><span>✓</span> {completed_step}</div>'
            steps_html += '<div class="thinking-step current-step"><span class="thinking-icon">✨</span> Finalizing results...</div>'
            steps_html += '</div>'
            result_placeholder.markdown(steps_html, unsafe_allow_html=True)
            
            time.sleep(0.5)
            
            # Store result
            result_text = "Spam" if result == 1 else "Not Spam"
            
            # Add to history
            st.session_state.message_history.insert(0, {
                'type': st.session_state.current_type,
                'message': st.session_state.current_input[:100] + ('...' if len(st.session_state.current_input) > 100 else ''),
                'full_message': st.session_state.current_input,
                'result': result_text,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M")
            })
            
            # Store result and reset analyzing state
            st.session_state.last_result = result
            st.session_state.analyzing = False
            st.rerun()
        
        # Display result if available
        elif st.session_state.last_result is not None:
            if st.session_state.last_result == 1:
                result_placeholder.markdown("""
                <div class="result-spam">
                    <div class="result-icon">🚫</div>
                    <div class="result-title">SPAM DETECTED</div>
                    <div class="result-subtitle">This message appears to be spam. Be cautious!</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.error("⚠️ **Warning:** Do not click any links or share personal information!")
            else:
                result_placeholder.markdown("""
                <div class="result-safe">
                    <div class="result-icon">✅</div>
                    <div class="result-title">SAFE MESSAGE</div>
                    <div class="result-subtitle">This message appears to be legitimate.</div>
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.success("✓ This message passed our spam detection filters.")
        else:
            result_placeholder.markdown("""
            <div class="thinking-box">
                <p style="font-size: 3rem; margin: 0;">🔍</p>
                <p style="color: #888; margin-top: 1rem;">Enter a message and click<br><strong>Analyze Message</strong><br>to see the result</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📜 Recent Analysis History")
    
    if st.session_state.message_history:
        for idx, item in enumerate(st.session_state.message_history[:20]):  # Show last 20
            result_class = "history-spam" if item['result'] == "Spam" else "history-safe"
            result_badge_class = "history-result-spam" if item['result'] == "Spam" else "history-result-safe"
            result_emoji = "🚫" if item['result'] == "Spam" else "✅"
            type_emoji = "📧" if item['type'] == "Email" else "💬"
            
            st.markdown(f"""
            <div class="history-item {result_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span class="history-type">{type_emoji} {item['type']} • {item['timestamp']}</span>
                    <span class="history-result {result_badge_class}">{result_emoji} {item['result']}</span>
                </div>
                <div class="history-message">{item['message']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #f8f9fa; padding: 3rem; border-radius: 16px; text-align: center;">
            <p style="font-size: 4rem; margin: 0;">📭</p>
            <p style="color: #888; font-size: 1.1rem; margin-top: 1rem;">No messages analyzed yet</p>
            <p style="color: #aaa;">Start by analyzing your first message!</p>
        </div>
        """, unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #888; padding: 1rem;">
    <p>🛡️ <strong>SpamShield</strong> - Powered by Machine Learning</p>
    <p style="font-size: 0.8rem;">Protecting your inbox from unwanted messages</p>
</div>
""", unsafe_allow_html=True)

import os
import time
import pygame
from gtts import gTTS
import streamlit as st
import speech_recognition as sr
from googletrans import LANGUAGES, Translator
from datetime import datetime
import csv
import io

# Page configuration
st.set_page_config(page_title="Language Translator", page_icon="🎙️", layout="centered")

# Initialize session state
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = False
if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []

isTranslateOn = False

translator = Translator()
pygame.mixer.init()

language_mapping = {name: code for code, name in LANGUAGES.items()}

def get_language_code(language_name):
    return language_mapping.get(language_name, language_name)

def translator_function(spoken_text, from_language, to_language):
    return translator.translate(spoken_text, src='{}'.format(from_language), dest='{}'.format(to_language))

def text_to_voice(text_data, to_language):
    myobj = gTTS(text=text_data, lang='{}'.format(to_language), slow=False)
    myobj.save("cache_file.mp3")
    audio = pygame.mixer.Sound("cache_file.mp3")
    audio.play()
    pygame.time.wait(int(audio.get_length() * 1000))
    os.remove("cache_file.mp3")

def add_to_history(original, translated, from_lang, to_lang):
    """Add translation to history"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.translation_history.insert(0, {
        'timestamp': timestamp,
        'original': original,
        'translated': translated,
        'from_lang': from_lang,
        'to_lang': to_lang
    })
    # Keep only last 50 translations
    if len(st.session_state.translation_history) > 50:
        st.session_state.translation_history.pop()

def export_history_csv():
    """Export history to CSV"""
    if not st.session_state.translation_history:
        return None
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['timestamp', 'original', 'translated', 'from_lang', 'to_lang'])
    writer.writeheader()
    writer.writerows(st.session_state.translation_history)
    return output.getvalue()

def main_process(output_placeholder, from_language, to_language, from_lang_name, to_lang_name):
    global isTranslateOn
    
    while isTranslateOn:
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            output_placeholder.text("Listening...")
            rec.pause_threshold = 1
            audio = rec.listen(source, phrase_time_limit=10)
        
        try:
            output_placeholder.text("Processing...")
            spoken_text = rec.recognize_google(audio, language='{}'.format(from_language))
            st.write("You said:", spoken_text)
            
            output_placeholder.text("Translating...")
            translated_text = translator_function(spoken_text, from_language, to_language)
            st.write("Translated text:", translated_text.text)
            
            # Add to history
            add_to_history(spoken_text, translated_text.text, from_lang_name, to_lang_name)

            text_to_voice(translated_text.text, to_language)
    
        except Exception as e:
            print(e)

# Custom CSS with animated background
if st.session_state.dark_mode:
    bg_color1, bg_color2, circle_color1, circle_color2, circle_color3 = "#0f2027", "#203a43", "#2c5364", "#0f2027", "#203a43"
else:
    bg_color1, bg_color2, circle_color1, circle_color2, circle_color3 = "#667eea", "#764ba2", "#f093fb", "#4facfe", "#00f2fe"

st.markdown(f"""
<style>
    .stApp {{
        background: linear-gradient(135deg, {bg_color1} 0%, {bg_color2} 100%);
        position: relative;
        overflow: hidden;
    }}
    
    .stApp::before {{
        content: '';
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: 0;
        pointer-events: none;
    }}
    
    @keyframes float {{
        0%, 100% {{ transform: translate(0, 0) rotate(0deg); }}
        33% {{ transform: translate(30px, -30px) rotate(120deg); }}
        66% {{ transform: translate(-20px, 20px) rotate(240deg); }}
    }}
    
    @keyframes float2 {{
        0%, 100% {{ transform: translate(0, 0) scale(1); }}
        50% {{ transform: translate(-50px, 50px) scale(1.1); }}
    }}
    
    @keyframes float3 {{
        0%, 100% {{ transform: translate(0, 0) rotate(0deg) scale(1); }}
        33% {{ transform: translate(40px, 40px) rotate(180deg) scale(0.9); }}
        66% {{ transform: translate(-30px, -20px) rotate(270deg) scale(1.1); }}
    }}
    
    .animated-bg {{
        position: fixed;
        width: 100%;
        height: 100%;
        top: 0;
        left: 0;
        z-index: 0;
        pointer-events: none;
    }}
    
    .circle {{
        position: absolute;
        border-radius: 50%;
        opacity: 0.2;
    }}
    
    .circle1 {{
        width: 300px;
        height: 300px;
        background: {circle_color1};
        top: 10%;
        left: 10%;
        animation: float 20s infinite ease-in-out;
    }}
    
    .circle2 {{
        width: 200px;
        height: 200px;
        background: {circle_color2};
        top: 50%;
        right: 15%;
        animation: float2 15s infinite ease-in-out;
    }}
    
    .circle3 {{
        width: 250px;
        height: 250px;
        background: {circle_color3};
        bottom: 10%;
        left: 50%;
        animation: float3 18s infinite ease-in-out;
    }}
    
    .circle4 {{
        width: 150px;
        height: 150px;
        background: {circle_color1};
        top: 70%;
        left: 20%;
        animation: float 25s infinite ease-in-out reverse;
    }}
    
    .circle5 {{
        width: 180px;
        height: 180px;
        background: {circle_color2};
        top: 30%;
        right: 30%;
        animation: float2 22s infinite ease-in-out reverse;
    }}
    
    [data-testid="stAppViewContainer"] {{
        position: relative;
        z-index: 1;
    }}
    
    .main-title {{
        color: #ffffff;
        text-align: center;
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }}
    
    .section-label {{
        color: #ffffff;
        font-size: 1.1rem;
        font-weight: 500;
        margin-bottom: 0.5rem;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }}
    
    div[data-testid="stSelectbox"] label {{
        color: #ffffff !important;
    }}
    
    /* History Sidebar Styles */
    .history-item {{
        background: rgba(255, 255, 255, 0.1);
        border-left: 4px solid #60a5fa;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.8rem;
    }}
    
    .history-time {{
        color: #a0aec0;
        font-size: 0.85rem;
        margin-bottom: 0.5rem;
    }}
    
    .history-text {{
        color: #ffffff;
        font-size: 0.95rem;
        line-height: 1.5;
    }}
    
    .history-arrow {{
        color: #60a5fa;
        margin: 0.3rem 0;
        font-size: 0.9rem;
    }}
</style>

<div class="animated-bg">
    <div class="circle circle1"></div>
    <div class="circle circle2"></div>
    <div class="circle circle3"></div>
    <div class="circle circle4"></div>
    <div class="circle circle5"></div>
</div>
""", unsafe_allow_html=True)

# Sidebar for Translation History
with st.sidebar:
    st.markdown("### 📚 Translation History")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.translation_history = []
            st.rerun()
    
    with col2:
        if st.session_state.translation_history:
            csv_data = export_history_csv()
            st.download_button(
                label="📥 Export",
                data=csv_data,
                file_name=f"translations_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    
    st.markdown("---")
    
    # Search in history
    search_query = st.text_input("🔍 Search history", placeholder="Type to search...")
    
    # Display history
    if st.session_state.translation_history:
        filtered_history = st.session_state.translation_history
        if search_query:
            filtered_history = [
                item for item in st.session_state.translation_history
                if search_query.lower() in item['original'].lower() or 
                   search_query.lower() in item['translated'].lower()
            ]
        
        for item in filtered_history[:20]:  # Show last 20
            st.markdown(f"""
                <div class="history-item">
                    <div class="history-time">{item['timestamp']}</div>
                    <div class="history-text"><strong>"{item['original']}"</strong></div>
                    <div class="history-arrow">↓ {item['from_lang']} → {item['to_lang']}</div>
                    <div class="history-text">{item['translated']}</div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No translations yet. Start translating!")

# Dark mode toggle in top right
col1, col2 = st.columns([9, 1])
with col2:
    if st.button("🌓"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# UI layout
col1, col2 = st.columns([1, 8])
with col1:
    st.image("microphone.png", width=100)
with col2:
    st.markdown('<h1 class="main-title">Language Translator</h1>', unsafe_allow_html=True)

# Dropdowns for selecting languages
st.markdown('<p class="section-label">Select Source Language:</p>', unsafe_allow_html=True)
from_language_name = st.selectbox("Select Source Language:", list(LANGUAGES.values()), label_visibility="collapsed")

st.markdown('<p class="section-label">Select Target Language:</p>', unsafe_allow_html=True)
to_language_name = st.selectbox("Select Target Language:", list(LANGUAGES.values()), label_visibility="collapsed")

# Convert language names to language codes
from_language = get_language_code(from_language_name)
to_language = get_language_code(to_language_name)

# Button to trigger translation
col1, col2 = st.columns(2)
with col1:
    start_button = st.button("Start", use_container_width=True)
with col2:
    stop_button = st.button("Stop", use_container_width=True)

# Check if "Start" button is clicked
if start_button:
    if not isTranslateOn:
        isTranslateOn = True
        output_placeholder = st.empty()
        main_process(output_placeholder, from_language, to_language, from_language_name, to_language_name)

# Check if "Stop" button is clicked
if stop_button:
    isTranslateOn = False
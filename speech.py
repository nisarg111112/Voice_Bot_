import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import time
from googletrans import Translator
from langdetect import detect
from interrupt_handler import InterruptHandler

# Initialize components
recognizer = sr.Recognizer()
translator = Translator()
pygame.mixer.init()
interrupt_handler = InterruptHandler()

def text_to_speech(text, language_code='en'):
    """Convert text to speech with interrupt handling"""
    try:
        # If text is not in target language, translate it
        detected_lang = detect(text)
        if detected_lang != language_code:
            text = translator.translate(text, dest=language_code).text
        
        # Create gTTS object and save to file
        tts = gTTS(text=text, lang=language_code)
        temp_file = "temp_speech.mp3"
        tts.save(temp_file)
        
        # Start interrupt listener if not already running
        if not interrupt_handler.is_listening:
            interrupt_handler.start_listening(language_code)
        
        # Play the audio with interrupt handling
        pygame.mixer.music.load(temp_file)
        pygame.mixer.music.play()
        
        # Monitor playback with interrupt checking
        while pygame.mixer.music.get_busy():
            # Check for interrupts
            command = interrupt_handler.check_for_interrupt()
            #print(f"Processing command: {command}")  # Debug log
            
            if command == 'pause':
                print("Pausing speech...")  # Debug log
                pygame.mixer.music.pause()
                while interrupt_handler.is_paused and not interrupt_handler.should_exit:
                    command = interrupt_handler.check_for_interrupt()
                    time.sleep(0.1)
                if not interrupt_handler.should_exit:
                    print("Resuming speech...")  # Debug log
                    pygame.mixer.music.unpause()
            
            elif command == 'exit':
                print("Exiting speech...")  # Debug log
                pygame.mixer.music.stop()
                break
                
            time.sleep(0.1)
            
        # Clean up
        pygame.mixer.music.unload()
        os.remove(temp_file)
        
        # Check if we should exit
        if interrupt_handler.should_exit:
            exit()
            
    except Exception as e:
        print(f"Text-to-speech error: {e}")

def speech_to_text(language_code='en'):
    """Convert speech to text in the specified language"""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        listening_messages = {
            'en': "Listening... Speak now!",
            'hi': "सुन रहा हूं... अब बोलिए!",
            'mr': "ऐकत आहे... आता बोला!"
        }
        text_to_speech(listening_messages[language_code], language_code)
        print(listening_messages[language_code])
        
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            text = recognizer.recognize_google(audio, language=language_code)
            print(f"You said: {text}")
            return text
        except sr.WaitTimeoutError:
            error_messages = {
                'en': "You didn't speak in time. Please try again.",
                'hi': "आपने समय पर नहीं बोला। कृपया पुनः प्रयास करें।",
                'mr': "तुम्ही वेळेत बोलला नाहीत. कृपया पुन्हा प्रयत्न करा."
            }
            text_to_speech(error_messages[language_code], language_code)
            return None
        except sr.UnknownValueError:
            error_messages = {
                'en': "Sorry, I couldn't understand what you said.",
                'hi': "क्षमा करें, मैं समझ नहीं पाया आपने क्या कहा।",
                'mr': "क्षमस्व, तुम्ही काय म्हणालात ते मला समजले नाही."
            }
            text_to_speech(error_messages[language_code], language_code)
            return None
        except sr.RequestError as e:
            print(f"Speech recognition API error: {e}")
            return None

def select_language():
    """Prompt user to select language and return language code"""
    text_to_speech("Please select your preferred language: English, Hindi, or Marathi", 'en')
    text_to_speech("कृपया अपनी पसंदीदा भाषा चुनें: अंग्रेजी, हिंदी, या मराठी", 'hi')
    text_to_speech("कृपया तुमची पसंतीची भाषा निवडा: इंग्रजी, हिंदी किंवा मराठी", 'mr')
    
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        print("Listening for language selection...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            language = recognizer.recognize_google(audio).lower()
            
            # Map common variations to supported languages
            if 'english' in language or 'inglis' in language:
                return 'en'
            elif 'hindi' in language or 'हिंदी' in language:
                return 'hi'
            elif 'marathi' in language or 'मराठी' in language:
                return 'mr'
            else:
                text_to_speech("Language not recognized. Defaulting to English.", 'en')
                return 'en'
        except:
            text_to_speech("Language not recognized. Defaulting to English.", 'en')
            return 'en'
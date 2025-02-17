#from music_player import play_music
from google_search import google_search
from weather import fetch_weather
from speech import text_to_speech, speech_to_text
import webbrowser
import cv2
from difflib import get_close_matches
from reminder import handle_reminder
from maps import open_in_maps, get_directions
from camera import handle_camera

COMMANDS = {
    'en': {
        #'play_music': ['play music', 'play song', 'start music', 'start song'],
        # 'stop_music': ['stop music', 'stop song', 'pause music', 'pause song'],
        'question': ['question', 'ask question', 'search', 'find'],
        'youtube': ['open youtube', 'youtube', 'start youtube', 'search youtube'],
        'wikipedia': ['open wikipedia', 'wikipedia', 'search wikipedia'],
        'weather': ["what's the weather", 'current weather', 'weather', 'temperature'],
        'reminder': ['set a reminder', 'reminder', 'remind me'],
        'camera': ['open camera', 'camera', 'start camera'],
        'map': ['show map', 'find location', 'locate', 'show on map', 'find on map', 'map'],
        'directions': ['get directions', 'show directions', 'how to go', 'route to'],
        'exit': ['exit', 'end', 'stop', 'quit', 'close']
    },
    'hi': {
        'map': [
            'नक्शा दिखाओ', 'लोकेशन ढूंढो', 'मैप पर दिखाओ', 
            'स्थान खोजो', 'map देखो', 'location बताओ'
        ],
        'directions': [
            'रास्ता दिखाओ', 'दिशा दिखाओ', 'कैसे जाएं',
            'मार्ग बताओ', 'directions बताओ'
        ],
        # 'play_music': [
        #     'गाना बजाओ', 'संगीत चलाओ', 'गाना चलाओ', 'music चलाओ', 
        #     'gaana bajao', 'sangeet chalao', 'song chalao', 
        #     'music start', 'गाना start', 'music शुरू करो'
        # ],
        # 'stop_music': ['गाना बंद करो', 'संगीत बंद करो', 'music बंद करो'
        # ],
        'question': [
            'सवाल', 'प्रश्न', 'कुछ पूछना है', 'search', 
            'sawal', 'prashn', 'question', 'search karo'
        ],
        'youtube': [
            'यूट्यूब खोलो', 'यूट्यूब', 'youtube खोलो',
            'youtube chalao', 'youtube start', 'youtube shuru karo',
            'search youtube'
        ],
        'wikipedia': [
            'विकिपीडिया खोलो', 'विकिपीडिया', 'wikipedia खोलो',
            'wikipedia search', 'wikipedia देखो'
        ],
        'weather': [
            'मौसम', 'मौसम कैसा है', 'तापमान', 'weather', 
            'mausam', 'weather batao', 'temperature'
        ],
        'reminder': [
            'रिमाइंडर', 'याद दिलाओ', 'reminder set', 
            'reminder लगाओ', 'याद रखो'
        ],
        'camera': [
            'कैमरा खोलो', 'कैमरा', 'camera', 'photo', 
            'camera on', 'camera खोलो'
        ],
        'exit': [
            'बंद करो', 'समाप्त', 'exit', 'band', 'stop', 
            'बाहर', 'खत्म'
        ]
    },
    'mr': {
        'map': [
            'नकाशा दाखवा', 'स्थान शोधा', 'मॅप वर दाखवा',
            'ठिकाण शोधा', 'map दाखवा', 'location शोधा'
        ],
        'directions': [
            'मार्ग दाखवा', 'दिशा दाखवा', 'कसे जायचे',
            'रस्ता दाखवा', 'directions दाखवा'
        ],
        # 'play_music': [
        #     'गाणे लाव', 'संगीत लाव', 'गाणे चालू कर', 
        #     'music लाव', 'gaane laav', 'sangeet chalu kar',
        #     'music start', 'गाणे start'
        # ],
        # 'stop_music': ['गाणे बंद कर', 'संगीत बंद कर', 'music बंद कर'
        # ],
        'question': [
            'प्रश्न', 'विचार', 'शोध', 'search', 
            'prashna', 'vichar', 'shodh', 'search kar'
        ],
        'youtube': [
            'यूट्यूब उघडा', 'यूट्यूब', 'youtube उघडा',
            'youtube laav', 'youtube chalu kar', 'search youtube'
        ],
        'wikipedia': [
            'विकिपीडिया उघडा', 'विकिपीडिया', 'wikipedia उघडा',
            'wikipedia bagha', 'wikipedia search'
        ],
        'weather': [
            'हवामान', 'हवामान काय आहे', 'तापमान', 'weather',
            'havaman', 'temperature', 'हवामान सांग'
        ],
        # 'reminder': [
        #     'रिमाइंडर', 'आठवण करून दे', 'reminder set', 
        #     'reminder लाव', 'आठवण ठेव'
        # ],
        'camera': [
            'कॅमेरा उघडा', 'कॅमेरा', 'camera', 'photo',
            'camera chalu kar', 'camera उघडा'
        ],
        'exit': [
            'बंद करा', 'थांबा', 'exit', 'band', 'stop',
            'बाहेर', 'संपवा'
        ]
    }
}


def find_closest_command(spoken_text, language_code):
    """Find the closest matching command using fuzzy matching"""
    spoken_words = spoken_text.lower().split()
    
    for command_type, variations in COMMANDS[language_code].items():
        # Check for exact matches first
        for variation in variations:
            if variation in spoken_text.lower():
                return command_type
        
        # Check each word in the spoken text against command variations
        for word in spoken_words:
            matches = get_close_matches(word, variations, n=1, cutoff=0.7)
            if matches:
                return command_type
                
    return None

def handle_task(command, language_code):
    """Handle tasks based on voice commands with improved recognition"""
    command_type = find_closest_command(command, language_code)
    
    if command_type == 'map':
        messages = {
            'en': "Which location would you like to find?",
            'hi': "आप कौन सी जगह ढूंढना चाहेंगे?",
            'mr': "तुम्हाला कोणती जागा शोधायची आहे?"
        }
        text_to_speech(messages[language_code], language_code)
        location = speech_to_text(language_code)
        
        if location:
            result = open_in_maps(location)
            if result:
                success_messages = {
                    'en': f"Opening maps for {result}",
                    'hi': f"{result} के लिए मैप खोल रहा हूं",
                    'mr': f"{result} साठी नकाशा उघडत आहे"
                }
                text_to_speech(success_messages[language_code], language_code)
            else:
                error_messages = {
                    'en': "Sorry, I couldn't find that location. Please try again.",
                    'hi': "क्षमा करें, वह स्थान नहीं मिल सका। कृपया पुनः प्रयास करें।",
                    'mr': "क्षमस्व, ते स्थान सापडले नाही. कृपया पुन्हा प्रयत्न करा."
                }
                text_to_speech(error_messages[language_code], language_code)
    
    elif command_type == 'directions':
        start_messages = {
            'en': "What's your starting location?",
            'hi': "आपका शुरुआती स्थान क्या है?",
            'mr': "तुमचे सुरुवातीचे ठिकाण कोणते आहे?"
        }
        text_to_speech(start_messages[language_code], language_code)
        origin = speech_to_text(language_code)
        
        if origin:
            dest_messages = {
                'en': "What's your destination?",
                'hi': "आपकी मंजिल क्या है?",
                'mr': "तुमचे गंतव्य स्थान कोणते आहे?"
            }
            text_to_speech(dest_messages[language_code], language_code)
            destination = speech_to_text(language_code)
            
            if destination:
                if get_directions(origin, destination):
                    success_messages = {
                        'en': f"Getting directions from {origin} to {destination}",
                        'hi': f"{origin} से {destination} तक का रास्ता दिखा रहा हूं",
                        'mr': f"{origin} पासून {destination} पर्यंतचा मार्ग दाखवत आहे"
                    }
                    text_to_speech(success_messages[language_code], language_code)
                else:
                    error_messages = {
                        'en': "Sorry, I couldn't get the directions. Please try again.",
                        'hi': "क्षमा करें, मैं दिशा-निर्देश नहीं दिखा सका। कृपया पुनः प्रयास करें।",
                        'mr': "क्षमस्व, मी दिशा दाखवू शकलो नाही. कृपया पुन्हा प्रयत्न करा."
                    }
                    text_to_speech(error_messages[language_code], language_code)
    
    # elif command_type == 'play_music':
    #     messages = {
    #         'en': "What song would you like to play?",
    #         'hi': "आप कौन सा गाना सुनना चाहेंगे?",
    #         'mr': "तुम्हाला कोणते गाणे ऐकायचे आहे?"
    #     }
    #     text_to_speech(messages[language_code], language_code)
    #     song_name = speech_to_text(language_code)
    #     if song_name:
    #         result = play_music(song_name)
    #         text_to_speech(result, language_code)
    
    # elif command_type == 'stop_music':
    #     result = stop_music()
    #     text_to_speech(result, language_code)
    
    elif command_type == 'question':
        messages = {
            'en': "What would you like to know?",
            'hi': "आप क्या जानना चाहेंगे?",
            'mr': "तुम्हाला काय जाणून घ्यायचे आहे?"
        }
        text_to_speech(messages[language_code], language_code)
        question = speech_to_text(language_code)
        if question:
            answer = google_search(question)
            text_to_speech(answer, language_code)
    
    elif command_type == 'weather':
        messages = {
            'en': "Which city's weather would you like to know?",
            'hi': "किस शहर का मौसम जानना चाहेंगे?",
            'mr': "कोणत्या शहराचे हवामान जाणून घ्यायचे आहे?"
        }
        text_to_speech(messages[language_code], language_code)
        city = speech_to_text(language_code)
        if city:
            weather_info = fetch_weather(city)
            text_to_speech(weather_info, language_code)
    
    elif command_type == 'youtube':
        text_to_speech("Opening YouTube. What would you like to search for?", language_code)
        search_query = speech_to_text(language_code)
        if search_query:
            formatted_query = search_query.replace(" ", "+")
            youtube_search_url = f"https://www.youtube.com/results?search_query={formatted_query}"
            text_to_speech(f"Searching for {search_query} on YouTube.", language_code)
            webbrowser.open(youtube_search_url)
        else:
            text_to_speech("I couldn't understand your search query. Please try again.", language_code)

    elif command_type == 'wikipedia':
        text_to_speech("Opening Wikipedia. What would you like to search for?", language_code)
        search_query = speech_to_text(language_code)
        if search_query:
            formatted_query = search_query.replace(" ", "_")
            wikipedia_search_url = f"https://en.wikipedia.org/wiki/{formatted_query}"
            text_to_speech(f"Searching for {search_query} on Wikipedia.", language_code)
            webbrowser.open(wikipedia_search_url)
        else:
            text_to_speech("I couldn't understand your search query. Please try again.", language_code)
    
    elif command_type == 'camera':
        handle_camera(language_code)
    
    elif command_type == 'reminder':
        handle_reminder(language_code)
       
    elif command_type == 'exit':
        messages = {
            'en': "Thank you!",
            'hi': "धन्यवाद!",
            'mr': "धन्यवाद!"
        }
        text_to_speech(messages[language_code], language_code)
        exit()
    
    else:
        messages = {
            'en': "Sorry, I didn't understand that command. Please try again.",
            'hi': "क्षमा करें, मैं आपका आदेश नहीं समझ पाया। कृपया दोबारा कहें।",
            'mr': "क्षमा करा, मला तुमची आज्ञा समजली नाही. कृपया पुन्हा प्रयत्न करा."
        }
        text_to_speech(messages[language_code], language_code)

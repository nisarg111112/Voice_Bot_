from speech import speech_to_text, text_to_speech, select_language
from utils import handle_task

def main():
    welcome_messages = {
        'en': "Welcome to VOICE BOT",
        'hi': "वॉइस बॉट में आपका स्वागत है",
        'mr': "व्हॉइस बॉटमध्ये आपले स्वागत आहे"
    }
    
    # First, select language
    language_code = select_language()
    
    # Welcome message in selected language
    text_to_speech(welcome_messages[language_code], language_code)
    
    while True:
        continue_messages = {
            'en': "\nPress Enter to start or type 'exit' to quit.",
            'hi': "\nशुरू करने के लिए एंटर दबाएं या बाहर निकलने के लिए 'exit' टाइप करें।",
            'mr': "\nसुरू करण्यासाठी एंटर दाबा किंवा बाहेर पडण्यासाठी 'exit' टाइप करा."
        }
        
        text_to_speech(continue_messages[language_code], language_code)
        user_input = input().strip()
        if user_input.lower() == 'exit':
            thank_you_messages = {
                'en': "Thank you!",
                'hi': "धन्यवाद!",
                'mr': "धन्यवाद!"
            }

            text_to_speech(thank_you_messages[language_code], language_code)
            break

        # Get the command from the user in their selected language
        command = speech_to_text(language_code)
        if command:
            handle_task(command, language_code)

if __name__ == "__main__":
    main()
from datetime import datetime, timedelta
import re
from speech import speech_to_text, text_to_speech
import time

def parse_time(input_time, language_code):
    """
    Parse the user's time input to a valid 24-hour datetime object.
    Supports both relative and absolute time formats.
    """
    try:
        # Clean up the input time string
        input_time = input_time.lower().replace('.', '').strip()
        
        # Check for relative time input like "in 10 minutes" or "in 2 hours"
        relative_time_match = re.match(r'(\d+)\s*(minute|hour|day)s?\s*(from now|later)?', input_time)
        if relative_time_match:
            num, unit, _ = relative_time_match.groups()
            num = int(num)
            if unit == 'minute':
                return datetime.now() + timedelta(minutes=num)
            elif unit == 'hour':
                return datetime.now() + timedelta(hours=num)
            elif unit == 'day':
                return datetime.now() + timedelta(days=num)

        # Try parsing 24-hour format, e.g., "18:00"
        try:
            parsed_time = datetime.strptime(input_time, "%H:%M")
            return parsed_time
        except ValueError:
            pass

        # Try parsing 12-hour format with AM/PM, handling various formats
        time_formats = [
            "%I:%M %p",    # 8:00 PM
            "%I:%M%p",     # 8:00PM
            "%I %M %p",    # 8 00 PM
            "%I %M%p",     # 8 00PM
            "%I:%M %p.",   # 8:00 P.M.
            "%I:%M%p.",    # 8:00P.M.
            "%I:%M %a.m.", # 8:00 A.m.
            "%I:%M %a.m",  # 8:00 A.m
            "%I:%M %p.m.", # 8:00 p.m.
            "%I:%M %p.m",  # 8:00 p.m
            "%I%M %p.m",  # 800 p.m
            "%I%M %p.m.", # 800 p.m.
            "%I%M %a.m",  # 800 a.m
            "%I%M %a.m.", # 800 a.m.
        ]
        
        for fmt in time_formats:
            try:
                parsed_time = datetime.strptime(input_time, fmt)
                return parsed_time
            except ValueError:
                continue

        # If parsing fails, ask the user to clarify
        clarification_message = {
            'en': "I couldn't understand the time. Could you please specify it more clearly?",
            'hi': "मुझे समय समझ में नहीं आया। क्या आप इसे और स्पष्ट रूप से बता सकते हैं?",
            'mr': "मला वेळ समजला नाही. कृपया तो स्पष्टपणे सांगा."
        }
        text_to_speech(clarification_message[language_code], language_code)
        clarified_time = speech_to_text(language_code)
        return parse_time(clarified_time, language_code)  # Recursive call with clarified input

    except Exception as e:
        # Fallback error handling
        clarification_message = {
            'en': "I couldn't understand the time. Could you please specify it more clearly?",
            'hi': "मुझे समय समझ में नहीं आया। क्या आप इसे और स्पष्ट रूप से बता सकते हैं?",
            'mr': "मला वेळ समजला नाही. कृपया तो स्पष्टपणे सांगा."
        }
        text_to_speech(clarification_message[language_code], language_code)
        clarified_time = speech_to_text(language_code)
        return parse_time(clarified_time, language_code)  # Recursive call with clarified input

def set_reminder(reminder_text, reminder_time, language_code):
    """
    Set a reminder for the specified time and display a message when the time is reached.
    """
    current_time = datetime.now()
    target_time = datetime(
        current_time.year,
        current_time.month,
        current_time.day,
        reminder_time.hour,
        reminder_time.minute
    )

    # Adjust target time if it's already passed today
    if target_time <= current_time:
        target_time += timedelta(days=1)

    wait_time = (target_time - current_time).total_seconds()

    confirmation_message = {
        'en': f"Reminder set for {target_time.strftime('%I:%M %p')}.",
        'hi': f"रिमाइंडर {target_time.strftime('%I:%M %p')} पर सेट कर दिया गया है।",
        'mr': f"रिमाइंडर {target_time.strftime('%I:%M %p')} साठी सेट केला आहे."
    }
    text_to_speech(confirmation_message[language_code], language_code)

    # Wait until the target time
    time.sleep(wait_time)

    # Notify the user when the time is reached
    notification_message = {
        'en': f"Reminder: {reminder_text}",
        'hi': f"रिमाइंडर: {reminder_text}",
        'mr': f"स्मरणपत्र: {reminder_text}"
    }
    text_to_speech(notification_message[language_code], language_code)


def handle_reminder(language_code):
    """
    Handles setting a reminder by asking the user for details.
    """
    ask_time_message = {
        'en': "At what time should I remind you? You can say 'in 30 minutes' or 'at 5 PM'.",
        'hi': "मैं आपको किस समय याद दिलाऊं? आप '30 मिनट में' या '5 बजे' कह सकते हैं।",
        'mr': "तुम्हाला कोणत्या वेळी आठवण करून द्यायची आहे? तुम्ही '30 मिनिटांमध्ये' किंवा '5 वाजता' असे सांगू शकता."
    }
    text_to_speech(ask_time_message[language_code], language_code)
    time_input = speech_to_text(language_code)

    reminder_time = parse_time(time_input, language_code)

    ask_text_message = {
        'en': "What should I remind you about?",
        'hi': "मुझे आपको किस बारे में याद दिलाना है?",
        'mr': "तुम्हाला कशाबद्दल आठवण करून द्यायची आहे?"
    }
    text_to_speech(ask_text_message[language_code], language_code)
    reminder_text = speech_to_text(language_code)

    set_reminder(reminder_text, reminder_time, language_code)


import speech_recognition as sr
import threading
import queue
from difflib import get_close_matches

class InterruptHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.is_listening = False
        self.is_paused = False
        self.should_exit = False
        self.command_queue = queue.Queue()
        
    def start_listening(self, language_code='en'):
        """Start listening for interruptions in a separate thread"""
        self.is_listening = True
       # print("Interrupt handler started listening...")  # Debug log
        self.thread = threading.Thread(target=self._listen_for_commands, args=(language_code,))
        self.thread.daemon = True
        self.thread.start()
        
    def stop_listening(self):
        """Stop listening for interruptions"""
        self.is_listening = False
        if hasattr(self, 'thread'):
            self.thread.join(timeout=1)
    
    def _listen_for_commands(self, language_code):
        """Background thread that listens for voice commands"""
        interrupt_commands = {
            'en': {
                'pause': ['pause', 'stop', 'wait', 'hold on'],
                'resume': ['resume', 'continue', 'start', 'go on'],
                'exit': ['exit', 'quit', 'close', 'bye']
            },
            'hi': {
                'pause': ['रुको', 'थांबो', 'बंद करो', 'wait'],
                'resume': ['चालू करो', 'जारी रखो', 'शुरू करो', 'आगे बढ़ो'],
                'exit': ['बंद करो', 'बाहर जाओ', 'exit', 'quit']
            },
            'mr': {
                'pause': ['थांबा', 'रोका', 'बंद करा', 'wait'],
                'resume': ['चालू करा', 'सुरू करा', 'पुढे चला', 'start'],
                'exit': ['बंद करा', 'बाहेर पडा', 'exit', 'quit']
            }
        }
    
        with sr.Microphone() as source:
            while self.is_listening:
                try:
                    audio = self.recognizer.listen(source, timeout=4, phrase_time_limit=3)
                    command = self.recognizer.recognize_google(audio, language=language_code).lower()
                    print(f"Detected command: {command}")  # Debug log
                    
                    # Check for matching commands
                    for cmd_type, variations in interrupt_commands[language_code].items():
                        if any(cmd in command for cmd in variations) or get_close_matches(command, variations, n=1, cutoff=0.7):
                           # print(f"Matched command: {cmd_type}")  # Debug log
                            self.command_queue.put(cmd_type)
                            break
                            
                except (sr.WaitTimeoutError, sr.UnknownValueError):
                    continue
                except Exception as e:
                    print(f"Error in interrupt listener: {e}")
                    continue

    def check_for_interrupt(self):
        """Check if there are any pending interrupt commands"""
        try:
            command = self.command_queue.get_nowait()
            if command == 'pause' or command == 'stop' or command == 'wait':
                self.is_paused = True
            elif command == 'resume':
                self.is_paused = False
            elif command == 'exit':
                self.should_exit = True
            return command
        except queue.Empty:
            return None
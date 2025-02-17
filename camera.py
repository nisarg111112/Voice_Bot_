import sys
import cv2
from speech import text_to_speech

def handle_camera(language_code):
    """Handle camera operations with proper error handling"""
    try:
        # Check if we're running on Windows
        if sys.platform.startswith('win'):
            # Try DirectShow backend on Windows
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        else:
            cap = cv2.VideoCapture(0)
            
        if not cap.isOpened():
            error_messages = {
                'en': "Could not open camera. Please check if it's connected properly.",
                'hi': "कैमरा नहीं खुल सका। कृपया जांचें कि यह सही तरीके से जुड़ा है।",
                'mr': "कॅमेरा उघडू शकलो नाही. कृपया तो योग्यरित्या जोडला आहे का ते तपासा."
            }
            text_to_speech(error_messages[language_code], language_code)
            return

        success_messages = {
            'en': "Camera is now open. Press 'q' to quit.",
            'hi': "कैमरा खुल गया है। बंद करने के लिए 'q' दबाएं।",
            'mr': "कॅमेरा आता उघडला आहे. बंद करण्यासाठी 'q' दाबा."
        }
        text_to_speech(success_messages[language_code], language_code)

        while True:
            ret, frame = cap.read()
            if not ret:
                break
                
            try:
                cv2.imshow("Camera", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            except cv2.error:
                # If GUI fails, try saving a photo instead
                photo_path = "captured_photo.jpg"
                cv2.imwrite(photo_path, frame)
                photo_messages = {
                    'en': f"GUI display not available. Photo saved as {photo_path}",
                    'hi': f"GUI प्रदर्शन उपलब्ध नहीं है। फोटो {photo_path} के रूप में सहेजा गया",
                    'mr': f"GUI प्रदर्शन उपलब्ध नाही. फोटो {photo_path} म्हणून जतन केला"
                }
                text_to_speech(photo_messages[language_code], language_code)
                break

    except Exception as e:
        error_messages = {
            'en': f"Camera error: {str(e)}. Please make sure OpenCV is installed correctly.",
            'hi': f"कैमरा त्रुटि: {str(e)}। कृपया सुनिश्चित करें कि OpenCV सही तरीके से इंस्टॉल है।",
            'mr': f"कॅमेरा त्रुटी: {str(e)}. कृपया OpenCV योग्यरित्या स्थापित केले आहे याची खात्री करा."
        }
        text_to_speech(error_messages[language_code], language_code)
    
    finally:
        if 'cap' in locals():
            cap.release()
        cv2.destroyAllWindows()
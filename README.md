# Multilingual Voice Assistant Bot

A versatile voice assistant that supports English, Hindi, and Marathi, capable of handling various tasks through voice commands. The bot uses speech recognition and text-to-speech capabilities to provide a hands-free interface for common tasks.

## Features

- **Multilingual Support**
  - English
  - Hindi
  - Marathi
  - Automatic language detection and translation

- **Core Functionalities**
  - Location Services
    - Show locations on map
    - Get directions between places
  - Information Queries
    - Google search integration
    - Wikipedia search
    - YouTube search
  - Weather Updates
    - Current temperature
    - Weather conditions
    - Wind speed and humidity
  - Utility Features
    - Camera control
    - Reminder setting
    - Voice interrupt handling

## Prerequisites

- Python 3.7 or higher
- Operating system: Windows/Linux/MacOS
- Working microphone
- Internet connection
- Camera (optional, for camera features)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/voice-bot.git
cd voice-bot
```

2. Create and activate a virtual environment:

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

For Linux/MacOS:
```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up API keys:
   - Create a file named `.env` in the project root
   - Add your API keys:
   ```
   OPENCAGE_API_KEY=your_opencage_key
   GOOGLE_API_KEY=your_google_key
   GOOGLE_CX=your_google_cx
   LASTFM_API_KEY=your_lastfm_key
   ```

## Usage

1. Ensure your virtual environment is activated:

For Windows:
```bash
venv\Scripts\activate
```

For Linux/MacOS:
```bash
source venv/bin/activate
```

2. Start the voice bot:
```bash
python main.py
```

3. Select your preferred language when prompted (English/Hindi/Marathi)

4. Available voice commands:
   - "Show map" / "नक्शा दिखाओ" / "नकाशा दाखवा" - Find locations
   - "Get directions" / "रास्ता दिखाओ" / "मार्ग दाखवा" - Get route directions
   - "Search" / "खोज" / "शोध" - Google search
   - "Weather" / "मौसम" / "हवामान" - Check weather
   - "Open camera" / "कैमरा खोलो" / "कॅमेरा उघडा" - Access camera
   - "Set reminder" / "रिमाइंडर" / "आठवण" - Set reminders

5. Interrupt Commands:
   - "Pause" / "रुको" / "थांबा" - Pause current action
   - "Resume" / "जारी रखो" / "सुरू करा" - Resume paused action
   - "Exit" / "बंद करो" / "बंद करा" - Close the application

6. To deactivate the virtual environment when done:
```bash
deactivate
```

## Project Structure

```
voice-bot/
├── venv/             # Virtual environment directory
├── main.py           # Main application entry point
├── speech.py         # Speech recognition and synthesis
├── camera.py         # Camera handling
├── maps.py           # Location services
├── weather.py        # Weather information
├── reminder.py       # Reminder functionality
├── config.py         # Configuration and API keys
├── utils.py          # Utility functions
└── requirements.txt  # Package dependencies
```

## Troubleshooting

### Common Virtual Environment Issues:

1. **Permission Issues (Linux/MacOS)**:
   ```bash
   chmod +x venv/bin/activate
   ```

2. **Execution Policy (Windows)**:
   If you encounter execution policy errors, run PowerShell as administrator and execute:
   ```powershell
   Set-ExecutionPolicy RemoteSigned
   ```

3. **Package Installation Errors**:
   If you encounter package installation errors, upgrade pip:
   ```bash
   python -m pip install --upgrade pip
   ```

### General Issues:

- Network connectivity issues
- API failures
- Device access problems
- Speech recognition errors
- Language processing errors

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenCage for geocoding services
- Open-Meteo for weather data
- Google Cloud Services for speech recognition
- gTTS (Google Text-to-Speech) for voice synthesis

## Security Note

This application requires various API keys to function. Never commit your API keys to version control. Use environment variables or a secure configuration file to store sensitive information.

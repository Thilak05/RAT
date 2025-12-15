# RAT (Python 3.12 Updated)

**⚠️ DISCLAIMER: THIS SOFTWARE IS FOR EDUCATIONAL PURPOSES ONLY.**
This project is created to demonstrate how Remote Administration Tools (RATs) work and how to defend against them. The author is not responsible for any misuse of this tool. Do not use this on any system you do not own or have explicit permission to test.

## 📖 About
This project is a Telegram-based Remote Administration Tool (RAT) written in Python. It allows you to control a computer remotely using a Telegram bot.

This version is an update of the original [TeleRAT by henry-richard7](https://github.com/henry-richard7/TeleRAT).

### 🚀 Key Updates & Changes
- **Python 3.12+ Support**: The codebase has been updated to work with modern Python versions (fixing `asyncio` and `python-telegram-bot` v20+ issues).
- **Improved Eavesdropping**: Added "Start" and "Stop" recording functionality. The bot sends the audio file immediately after stopping.
- **PowerShell Access**: Added a silent `/ps` command to execute PowerShell commands without triggering a visible window.
- **System Control**: Added functionality to remotely shut down the system.
- **Keylogger**: Added start/stop keylogging capability with log retrieval.
- **Media Player**: Added hidden audio playback and video playback commands.
- **File Upload**: Added ability to upload files to the target by sending them to the bot.
- **Cleanup**: Removed unstable or redundant modules (Chat, Random Mouse, Type String) to focus on core functionality.

## 🛠️ Features
- **📟 Get IP**: Retrieve the target's public IP and geolocation.
- **📸 Get Screenshot**: Capture the current screen.
- **📷 Webcam Snap**: Take a picture using the webcam.
- **👂 Eavesdrop**: Record audio from the microphone (Start/Stop control).
- **🗣️ Text to Speech**: Make the target computer speak a sentence.
- **🖥️ System Info**: Get detailed hardware and software information.
- **💻 Shell/PowerShell**: Execute CMD or PowerShell commands remotely.
- **🗊 File Access**: Download specific files from the target.
- **📤 File Upload**: Upload files to the target (supports Documents, Images, Audio, Video).
- **⌨️ Keylogger**: Record keystrokes (Start/Stop control).
- **🎵 Play Audio**: Play audio files silently in the background.
- **🎬 Play Video**: Launch video files on the target.
- **🌐 Open Website**: Open a specific URL on the target's browser.
- **⚠️ Show Alert**: Display a popup message box.
- **📋 Clipboard**: Retrieve current clipboard content.
- **🗝️ Wi-Fi Passwords**: Extract saved Wi-Fi passwords.
- **🔌 Shutdown**: Remotely shut down the computer.

## ⚙️ Installation & Usage

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd rat
   ```

2. **Install Dependencies**
   Make sure you have Python installed.
   ```bash
   pip install -r requirements.txt
   ```
   *Note: You may need to install `pyaudio` separately or use a pre-built wheel if `pip install pyaudio` fails on Windows.*

3. **Configuration**
   Open `main.py` and update the following lines with your Telegram Bot details:
   ```python
   API_KEY = "YOUR_BOT_TOKEN"
   CHAT_ID = "YOUR_CHAT_ID"
   ```

4. **Run the RAT**
   ```bash
   python main.py
   ```

5. **Control**
   Open your Telegram Bot and send `/start` to see the menu.

## 🤖 Bot Commands
| Command | Description |
| :--- | :--- |
| `/start` | Show the main menu |
| `/ps <command>` | Execute a PowerShell command silently |
| `/shell <command>` | Execute a CMD command |
| `/speak <text>` | Speak text on target machine |
| `/show_popup <msg>` | Show an alert box |
| `/open_website <url>` | Open a website |
| `/get_file <path>` | Download a file |
| `/playaudio <path>` | Play audio file (hidden) |
| `/playvideo <path>` | Play video file |
| `/startkeylog` | Start recording keystrokes |
| `/stopkeylog` | Stop recording and get log file |

### 📤 File Upload
To upload a file to the target machine:
1. Send the file (Document, Photo, Audio, or Video) to the bot.
2. **Optional**: Add a caption to specify the save path (e.g., `C:\Temp\` or `C:\Users\Public\file.exe`).
3. If no caption is provided, it saves to the current working directory.

## 🤝 Credits
- Original Project: [henry-richard7](https://github.com/henry-richard7)
- Updates & Refactoring: [Thilak](https://github.com/Thilak05).

---
*Created for learning and security research.*

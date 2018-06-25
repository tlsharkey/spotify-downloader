import os, sys, pip

OS = sys.platform.lower()
print("you seem to be running", OS)
print("checking your libraries and installing dependencies")

if OS == 'linux' or OS == 'darwin' or OS == 'dos' or OS == 'windows':
    import shutil
    installed_dir = os.getcwd()[:os.getcwd().rfind('/')]
    path = os.getcwd()
    shutil.copytree(os.getcwd(), os.path.expanduser("~")+"/spotify-downloader")

    print("\nInstalling... You may be asked for a password.")
    #ffmpeg
    if OS == 'linux':
        os.system("sudo apt-get install ffmpeg > /dev/null")
    elif OS == 'darwin':
        os.system("brew install ffmpeg --with-libmp3lame --with-libass --with-open --with-fdk-aac > /dev/null")
    elif OS == 'windows':
        os.system("""@"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin" """.strip(' '))
        os.system("choco install ffmpeg")
    # python libs
    pip.main(['install', '-q', '-Ur', 'requirements.txt'])
	
    # shell script
    with open('../SpotifySync.sh', 'w') as file:
	file.write('cd ~/spotify-downloader')
        file.write('python3 SpotifySync.py')
    os.chmod("../SpotifySync.sh", 777)
    
    print("\nyou can now delete this folder. You will find a shell script that will run the sync in the directory above this (directory selected for download)")
	
	
elif OS == 'dos':
    #ffmpeg
    print("OH WINDOWS... WHY.")
    print("download from this link: http://ffmpeg.zeranoe.com/builds/")
    print("copy ffmpeg.exe from ffmpeg-xxx-winxx-static/bin/ffmpeg.exe to {} and you *SHOULD* be good".format(os.getcwd()))
    print("if that doesn't work try the parent directory to the one listed.")
    print("if that doesn't work try C:/Windows/System32")
    print("if that doesn't work... open cmd.exe as administrator (right click on cmd.exe) and paste this mess in:")
    print("""  @"%SystemRoot%\System32\WindowsPowerShell\v1.0\powershell.exe" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command "iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))" && SET "PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\bin" """)
    print("choco install ffmpeg")
    print("\n\nif that still doesn't work, download linux.")
    
    # python libs
    pip.main(['install', '-U', '-r', 'requirements.txt'])

    print("need an exe file")
    
else:
    print("Since you're running some odd ball OS, I assume you can figure out how to set everything up yourself.")
    print("Move this folder wherever you want it")
    print("git clone https://github.com/tlsharkey/spotify-downloader")
    print("cd spotify-downloader")
    print("pip install -U -r requirements.txt  <-- I'm doing this for you right now")
    pip.main(['install', '-U', '-r', 'requirements.txt'])

    

#! /usr/bin/python3

import sys, os

saveLocation = ''

spotdl_loc = ''
spotdl = 'python3 {}spotdl.py'.format(spotdl_loc)

playlists = []

def setConfig_commandLine():
    print("\n\n\nThe Graphic Interface failed, here is the backup")
    print("This is the configuration program for syncing spotify playlists")
    print("First,", end=' ')
    def getSaveLoc():
        print("where would you like to save the downloaded songs? (FULL PATH, please)")
        saveLoc = str(input("path: "))
        if saveLoc == 'q':
            sys.quit()
        try:
            os.chdir(saveLoc)
        except:
            print("That location doesn't exist. Enter a currently existing path")
            print("Enter the full path examples: /home/username/Music  or  C:/Users/usename/Music")
            print("typing 'q' will exit")
            getSaveLoc()
        return saveLoc

    saveLoc = getSaveLoc()
    
    playlists[]
    def getPlaylist():
        name = str(input("Playlist Name: "))
        link = str(input("Playlist URL: "))
        playlists.append((name, link))
        another = str(input("Add another playlist?\n\t (y/n) --> "))
        if another[0].lower() == 'y':
            getPlaylist()

    print("""\n\n ----- PLAYLISTS -----
This program only syncs playlists.
You can put all of your music into a playlist, and sync that if you choose.
If you don't want to do that, you can make your music public and download it.

To sync playlists, the name of the playlist, and its link is needed.
The name is simply the name you see in the spotify app
the link can be gotten by opening the playlist, clicking the '...',
clicking 'share' and finding the 'copy playlist link' button.
""")
    getPlaylist()

    # save
    with open('SpotifySync_Config.txt', 'w') as config:
        config.write("___Save Location:\n")
        config.write(saveLoc+"/\n")
        config.write("___Playlists:\n")
        for playlist in playlists:
            config.write(playlist[0].get() + " | " + playlist[1].get() + "\n")
        config.write("___End of Playlists___")
    
def setConfig():
    try:
        import tkinter as tk
    except ModuleNotFoundError:
        setConfig_commandLine()
        return
    from tkinter import filedialog
    global rows_used, playlist_data, saveLab, saveLoc
    
    
    print("Configuring...")

    # setup tkinter
    window = tk.Tk()
    window.title("Playlists")
    mainframe = tk.Frame(window)
    mainframe.grid(column=3, row=100)

    # save location
    saveLoc = ''
    def getSaveLocation():
        global saveLoc
        tk.Tk().withdraw()
        saveLoc = str(filedialog.askdirectory())
        global saveLab; saveLab.config(text='not saved')
        
    tk.Button(mainframe, text="Set Save Location", command=getSaveLocation).grid(column=0, row=0, columnspan=2)
    

    # get playlist information
    playlist_data = []
    rows_used = 1
    def getInputBoxes():
        global rows_used, playlist_data, saveLab
        row = rows_used
        name = tk.StringVar(master=mainframe, value='My Playlist')
        link = tk.StringVar(master=mainframe, value='https://open.spotify.com/user/12345678910/playlist/1vgf25da1f221df2d')

        name_entry = tk.Entry(mainframe, textvariable=name)
        name_entry.grid(column=0, row=row)
        link_entry = tk.Entry(mainframe, textvariable=link)
        link_entry.grid(column=1, row=row)

        rows_used += 1
        playlist_data.append((name, link, name_entry, link_entry))
        
        saveLab.config(text='not saved')
        
    tk.Button(mainframe, text="Add Playlist", command=getInputBoxes).grid(column=3, row=0)

    # save button
    saveLab = tk.Label(mainframe, text="not saved")
    saveLab.grid(column=3, row=1)
    def save():
        global saveLab, saveLoc
        with open('SpotifySync_Config.txt', 'w') as config:
            config.write("___Save Location:\n")
            config.write(saveLoc+"/\n")
            config.write("___Playlists:\n")
            for playlist in playlist_data:
                config.write(playlist[0].get() + " | " + playlist[1].get() + "\n")
            config.write("___End of Playlists___")
        saveLab.config(text='saved.')
    tk.Button(mainframe, text="Save", command=save).grid(column=3, row=2)
    getInputBoxes()

    #Add space
    tk.Canvas(mainframe, width=100, height=0).grid(column=2, row=0)
    tk.Canvas(mainframe, width=0, height=20).grid(column=0, row=99)
    tk.Canvas(mainframe, width=200, height=0).grid(column=0, row=99)


def getConfig():
    global saveLocation
    global playlists

    try:
        with open('SpotifySync_Config.txt', 'r') as config:
            config_lines = config.readlines()
    except:
        setConfig()
        return False

    gettingPlaylists = False
    for i in range(len(config_lines)):
        try:
            if "___Save Location:" in config_lines[i]:
                saveLocation = config_lines[i+1].strip()
                if "___Playlists:" in saveLocation:
                    # if no save location there...
                    setConfig()
                    return False
            elif "___Playlists:" in config_lines[i]:
                gettingPlaylists = True
            elif "___End of Playlists___" in config_lines[i]:
                gettingPlaylists = False

            if gettingPlaylists and "___Playlists:" not in config_lines[i]:
                # divide line into playlist name and playlist url
                playlist = config_lines[i].strip().split("|")
                playlist = [elm.strip() for elm in playlist]
                
                playlist[0] = playlist[0].lower().replace(' ','-') #remove spaces
                
                if '?' in playlist[1]:
                    playlist[1] = playlist[1][:playlist[1].find('?')] #remove identifier
                    
                playlists.append(playlist)
        except IndexError:
            setConfig()
            return False


def download(playlist):
    if not os.path.exists(saveLocation+playlist[0]):
        os.mkdir(saveLocation+playlist[0])

    with open(playlist[0]+'.txt', 'r') as songs:
        song_list = songs.readlines()

    print("{} songs to download".format(len(song_list)))
    for url in song_list:
        url = url.strip()

        try:
            result = os.popen("{} -s {} -f {} --overwrite skip".format(spotdl, url, saveLocation+playlist[0])).read().split('\n')
            name = 'song'
            if 'SONGNAME:' in result[0]:
                name = result[0][len('SONGNAME:'):]
                
            if "FAILED to get artwork" in result[-2]:
                # print and save the track in 'playlistName_failed.txt'
                print("\n\tCouldn't get artwork for {}".format(name))
                with open(playlist[0]+'_failed.txt', 'a') as failed:
                    failed.write("No album artwork:", pop(playlist[0]+'.txt'))
            elif "SUCCESS" in result[-2]:
                # save url to downloadHistory for that playlist
                print(name, end=", ")
                with open(playlist[0]+"_downloadHistory.txt", 'a') as success:
                    success.write( pop(playlist[0]+'.txt') )
            elif len(result) == 2:
                # if song already downloaded
                print("\nalready had {}".format(name),)
                with open(playlist[0]+"_downloadHistory.txt", 'a') as success:
                    success.write( pop(playlist[0]+'.txt') )
            #else:
                #print(result)
        except:
            print("\nERROR, skipping song - check {} for failures".format(os.getcwd()+'/'+playlist[0]+'_failed.txt'))
            with open(playlist[0]+'_failed.txt', 'a') as failed:
                failed.write("ERROR on song: {}".format( pop(playlist[0]+'.txt') ))
    print("\n----- Completed. -----\n\n")
        

def getSongs(playlist):
    before = set(os.listdir())

    os.system("{} --playlist {}".format(spotdl, playlist[1]))

    # checking to make sure names match up
    after = os.listdir()
    for file in after:
        if file not in before:
            newfile = file
    else:
        return
    
    if newfile != playlist[0]+'.txt':
        print("Filename from program: {}\nFilename from config: {}".format(newfile, playlist[0]))
        print("using {}.txt".format(playlist[0]))
        os.rename(newfile, playlist[0]+'.txt')
    

    
def updateList(playlist):
    # check files exist
    ls = os.listdir()
    if playlist[0]+"_downloadHistory.txt" not in ls:
        #os.system("touch "+playlist[0]+"_downloadHistory.txt")
        histFile = open(playlist[0]+"_downloadHistory.txt", 'w')
        histFile.close()
    
    #slurp download history
    alreadyDownloaded = open(playlist[0]+"_downloadHistory.txt", 'r')
    links_AD = set(alreadyDownloaded.readlines())
    alreadyDownloaded.close()
    #slurp songs on playlist to download
    toDownload = open(playlist[0]+'.txt', 'r')
    links_TD = toDownload.readlines()
    toDownload.close()

    # remove all links which have previously been downloaded
    for i in range(len(links_TD)-1, -1, -1):
        if links_TD[i] in links_AD:
            links_TD.pop(i)
    ##else:
        ##print("No Overlap Found in trimming download list")

    # update the songs to download and download history text files
    toDownload = open(playlist[0]+'.txt', 'w') #clobber
    for link in links_TD:
        toDownload.write(link)
    toDownload.close()
    ##print("Lists Synced.".format(len(links_TD)))


def sync():
    if getConfig() is False:
        return
    
    for playlist in playlists:
        print("Syncing '{}'".format(playlist[0]), end='')
        # check if need to resume
        if os.path.exists(playlist[0]+'.txt'):
            with open(playlist[0]+'.txt', 'r') as todl:
                urls = todl.readlines()
        if 'urls' in locals() and len(urls) > 0:
            print(" - resuming")
            resume(playlist)
            del urls
        else:
            print(" - syncing")
            getSongs(playlist)
            #print("Got Song List, now syncing...")
            updateList(playlist)
            #print("Now downloading... This will take time.")
            download(playlist)
            
    print("Sync Complete.")
    print("Music saved to {}".format(saveLocation))


def resume(playlist):
    download(playlist)


def resume_skip(playlist):
    with open(playlist[0]+'_failed.txt', 'a') as failed:
        failed.write( pop(playlist[0]+'.txt') )
    #os.system("head -n 1 {}.txt >> {}_failed.txt".format(playlist[0], playlist[0]))
    #os.system("sed -i 1d [].txt".format(playlist[0]))
    download(playlist)


def pop(filename, linenumber=0):
    with open(filename, 'r') as file:
        lines = file.readlines()
    popped = lines.pop(linenumber)

    with open(filename, 'w') as file:
        file.writelines(lines)
    return popped



if __name__ == "__main__":
    sync()

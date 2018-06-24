#! /usr/bin/python3

import sys, os

saveLocation = ''

spotdl_loc = ''
spotdl = 'python3 {}spotdl.py'.format(spotdl_loc)

dlHistory = "downloadHistory.txt"

playlists = []

def getConfig():
    global saveLocation
    global playlists
    
    config = open('SpotifySync_Config.txt', 'r')
    config_lines = config.readlines()
    config.close()

    gettingPlaylists = False
    for i in range(len(config_lines)):
        if "___Save Location:" in config_lines[i]:
            saveLocation = config_lines[i+1].strip()
        elif "___Playlists:" in config_lines[i]:
            gettingPlaylists = True
        elif "___End of Playlists___" in config_lines[i]:
            gettingPlaylists = False

        if gettingPlaylists:
            # divide line into playlist name and playlist url
            playlist = config_lines[i].strip().split("|")
            playlist = [elm.strip() for elm in playlist]
            
            playlist[0] = playlist[0].lower().replace(' ','-') #remove spaces
            
            if '?' in playlist[1]:
                playlist[1] = playlist[1][:playlist[1].find('?')] #remove identifier
                
            playlists.append(playlist)

def download(playlist):
    while True:
        try:
            if not os.path.exists(saveLocation+playlist[0]):
                os.mkdir(saveLocation+playlist[0])
            # importing spotdl doesn't work - library error
            os.system("{} --list={} -f {} --overwrite skip".format(spotdl, playlist[0]+'.txt', saveLocation+playlist[0]))
            break
        except:
            print("\n\n\tSomething Failed\n\n")
            os.system("head -n 1 {}.txt >> {}_failed.txt".format(playlist[0], playlist[0]))
            os.system("sed -i 1d [].txt".format(playlist[0]))
            continue

def download_bySong(playlist):
    if not os.path.exists(saveLocation+playlist[0]):
        os.mkdir(saveLocation+playlist[0])

    songs = open(playlist[0], 'r')
    song_list = songs.readlines()
    songs.close()

    for url in song_list:
        url = url.strip()
        #os.system("{} -s {} -f {} --overwrite skip".format(spotdl, url, saveLocation+playlist[0]))

        result = os.popen("{} -s {} -f {} --overwrite skip".format(spotdl, url, saveLocation+playlist[0])).read().split('\n')
        name = 'song'
        if 'SONGNAME:' in result[0]:
            name = result[0][len('SONGNAME:'):]
        if "FAILED to get artwork" in result[-2]:
            print("\n\tCouldn't get artwork for {}".format(name))
            with open('failed.txt', 'a') as failed:
                failed.write(url+'\n')
        elif "SUCCESS" in result[-2]:
            print("got {}".format(name), end=", ")
            with open(dlHistory, 'a') as success:
                success.write(url+'\n')
            

def getSongs(playlist):
    os.system("{} --playlist {}".format(spotdl, playlist[1]))

def updateLists(playlist):
    # check files exist
    ls = os.listdir()
    if dlHistory not in ls:
        os.system("touch "+dlHistory)
    
    #slurp download history
    alreadyDownloaded = open(dlHistory, 'r')
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
    else:
        print("No Overlap Found in trimming download list")

    # update the songs to download and download history text files
    toDownload = open(playlist[0]+'.txt', 'w') #clobber
    alreadyDownloaded = open(dlHistory, 'a') #append
    for link in links_TD:
        toDownload.write(link)
        alreadyDownloaded.write(link)
    toDownload.close()
    alreadyDownloaded.close()
    print("Synced. {} songs to download.".format(len(links_TD)))
    
def updateLists_songs(playlist):
    # check files exist
    ls = os.listdir()
    if dlHistory not in ls:
        os.system("touch "+dlHistory)
    
    #slurp download history
    alreadyDownloaded = open(dlHistory, 'r')
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
    else:
        print("No Overlap Found in trimming download list")

    # update the songs to download and download history text files
    toDownload = open(playlist[0]+'.txt', 'w') #clobber
    for link in links_TD:
        toDownload.write(link)
    toDownload.close()
    print("Lists Synced. {} songs to download.".format(len(links_TD)))



def sync():
    for playlist in playlists:
        getSongs(playlist)
        print("Got Song List, now syncing...")
        updateLists(playlist)
        print("Now downloading... This will take time.")
        download(playlist)
        print("Download Complete.")
        print("Music saved to {}".format(saveLocation))

def resume(playlist):
    download(playlist)

def resume_skip(playlist):
    os.system("head -n 1 {}.txt >> {}_failed.txt".format(playlist[0], playlist[0]))
    os.system("sed -i 1d [].txt".format(playlist[0]))
    download(playlist)


if __name__ == "__main__":
    sync()

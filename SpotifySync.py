#! /usr/bin/python3

import sys, os

saveLocation = ''

spotdl_loc = ''
spotdl = 'python3 {}spotdl.py'.format(spotdl_loc)

playlists = []



def getConfig():
    global saveLocation
    global playlists
    
    with open('SpotifySync_Config.txt', 'r') as config:
        config_lines = config.readlines()

    gettingPlaylists = False
    for i in range(len(config_lines)):
        if "___Save Location:" in config_lines[i]:
            saveLocation = config_lines[i+1].strip()
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
            print("\nERROR, skipping song - check {} for failures".format(os.getcwd()+playlist[0]+'_failed.txt'))
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
    getConfig()
    
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

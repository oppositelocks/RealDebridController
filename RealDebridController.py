import pyinotify
import os
import requests
import time

#Folder this script will watch for torrents/magnets
pathtowatch = "/mnt/local/downloads/torrents"

#Your RealDebrid Api key
rdapikey = ""

handler = EventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(pathtowatch, mask, rec=True)
notifier.loop()

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_DELETE | pyinotify.IN_CREATE  # watched events


class EventHandler(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        head, tail = os.path.split(event.pathname)
        filename = (tail)
        extension = os.path.splitext(filename)[1][1:]
        if extension == "torrent":
            print("Torrent file detected ",tail)
            torrent=(event.pathname)
            addtorrenturl = ("https://api.real-debrid.com/rest/1.0/torrents/addTorrent?auth_token="+rdapikey)
            with open(torrent, 'rb') as finput:
                response = requests.put(addtorrenturl, data=finput.read())
                responsefromrd = (response.json())
                myid = responsefromrd['id']
                head, tail = os.path.split(torrent)
                filename=tail
                print ("Submitted to RD")
                attemptstogetlink=0
                rderror=" "
                completedtask="No"
                time.sleep(2)
                selectfiles = ("https://api.real-debrid.com/rest/1.0/torrents/selectFiles/" + myid + "?auth_token=" + rdapikey)
                allfiles = {"files": "all"}
                response = requests.post(selectfiles, data=allfiles)

        elif extension == "magnet":
            print("Magnet file detected ",tail)
            magnetlink = (event.pathname)
            addmagneturl = ("https://api.real-debrid.com/rest/1.0/torrents/addMagnet?auth_token="+ rdapikey)
            magnetaddjson = {"magnet": magnet}
            response = requests.post(addmagneturl, data=magnetaddjson)
            responsefromrd = (response.json())
            myid = responsefromrd['id']
            head, tail = os.path.split(magnet)
            filename = tail
            print("Submitted to RD")
            attemptstogetlink=0
            rderror=" "
            completedtask="No"
            time.sleep(2)
            selectfiles = ("https://api.real-debrid.com/rest/1.0/torrents/selectFiles/" + myid + "?auth_token=" + rdapikey)
            allfiles = {"files": "all"}
            response = requests.post(selectfiles, data=allfiles)

        else:
            print("IGNORE Not suitable - " , tail)

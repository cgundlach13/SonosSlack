import soco
import os
import slack
import time
from soco import SoCo

slack_token="SLACK-TOKEN"   #Bot token for sonosupdates
client = slack.WebClient(slack_token)
lastArtist = ""  #what the app thinks is currently playing, checked against and updated every checkFreq interval
lastTitle = ""
track = {}  #create track dictionary object
sonosIp = "SONOS-IP"   #IP of master sonos amp
checkFreq = 1.5   #Seconds to wait in between song checks
sonosChannel = 'SLACK CHANNEL'  #Channel to post to, accepts Public/private channels, and direct messages



def main(lastArtist,lastTitle):
    
    while True:   #always true
        getSong()  #get the current song info in track form

        if track['title'] != lastTitle or track['artist'] != lastArtist:  #check if ether title or artist is different from last check
            postSong(track)   #if different, post to slack
            lastArtist = track['artist']   #update what the app thinks is playing
            lastTitle = track['title']
        else:
            lastArtist = track['artist']   #update what the app thinks is playing
            lastTitle = track['title']

        time.sleep(checkFreq)  #GTFTS 
    


def getSong(): 

    global track

    speaker = SoCo(sonosIp)  #create SoCo object
    track = speaker.get_current_track_info()  #create track dict from current track info
    return track


def postSong(track):
    
    client.chat_postMessage(
        channel = sonosChannel,
        blocks = [
            
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Song Title:*\n" + track['title']
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Artist:*\n" + track['artist']
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Album:*\n" + track['album']
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Length:*\n" + track['duration']
                    }
                ]
            
            },
            {
                "type": "divider"
        }
        ]
    )


main(lastArtist, lastTitle)  #Run main, it'll take over from there

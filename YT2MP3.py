###############################
### YT2MP3                  ###
### By: Ruined1 aka DeeJayh ###
###############################
### This program allows you ###
### to queue up a list of   ###
### YouTube MP4s to convert ###
### to MP3s.                ###
###############################

## System Requirements:
## Windows 7 or Newer, 64-bit only
## Does not currently support 32-bit, linux, mac, or any other OS

## Using FFMPEG by the FFmpeg team.
## Purpose in this project: Convert mp4 files to mp3 audio.
## Website: https://www.ffmpeg.org/
## Build: ffmpeg-20190211-6174686-win64-static
## Source code available from the official repositories: https://www.ffmpeg.org/download.html#repositories
## I am using FFmpeg unmodified and so no source changes have been made.
##
## ffmpeg version N-93109-g6174686bc3 Copyright (c) 2000-2019 the FFmpeg developers. I take no credit for their
## hard work and dedication.
##
## If you are an FFmpeg developer/team member/etc and I have not properly accredited your work, please advise
## me how to correct it and I will be happy to oblige.

from threading import Thread
import pytube as pt
import sys
import os
import tempfile
import base64
import subprocess
import ffmpeg_encoded

#Instantiate variables
downloadList = []
convertList = []
threads = []
dir = os.getcwd()

#program introduction
print("Welcome to YT2MP3.\nAutomatically downloads "
      "and converts YouTube videos to MP3 format.\n"
      "No malware, no nonsense, just a clean and "
      "simple, open-source client.")

#function to download mp4s from urls provided
def Download_mp4(url,downloadList):
    print("[{0} of {1}] {2} Downloading...".format(downloadList.index(url)+1,len(downloadList),url))

    try:
        pt.YouTube(url).streams.first().download()
    except:
        print("{0} is not a complete, valid youtube link.".format(url))

    print("[{0} of {1}] {2} Complete.".format(downloadList.index(url)+1,len(downloadList),url))

#function to use ffmpeg to convert mp4 to mp3
def Convert_mp3(file, path):
    newfile = file.split(".")[0] + ".mp3"
    print("Converting {0} -> {1}".format(file,newfile))
    result = subprocess.call([path, "-i", file, newfile], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    os.remove(os.getcwd() + "\\" + file)
    print("Converted {0} -> {1}".format(file,newfile))

#function to start all threads in a provided list of threads
def start_threads(threads):
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

#start a list of entries to process
while True:
    video = input("Paste a youtube link and hit enter, or leave blank to begin converting:\n")
    if video != "":
        downloadList.append(video)
        print("Added {0} to list of videos to download.".format(video))
    else:
        print("Finished adding videos to be downloaded.")
        break

#build a thread list to utilize pytube library to download as many
#videos as possible at once
for url in downloadList:
    thread = Thread(target = Download_mp4, args = (url,downloadList))
    threads.append(thread)

start_threads(threads)

print("Converting MP4s in directory: {0}".format(dir))

threads = []

##Unpack ffmpeg
print("Unpacking ffmpeg.")
fd, path = tempfile.mkstemp(suffix='.exe')
code = base64.b64decode(ffmpeg_encoded.encoded)
os.write(fd, code)
os.close(fd)
print("Unpack Complete")

#build a thread list to utilize ffmpeg to convert as many
#videos as possible at once
for file in os.listdir(dir):
    if file.endswith(".mp4"):
        print("Queueing file {0} for conversion.".format(file))
        thread = Thread(target = Convert_mp3, args = (file, path))
        threads.append(thread)
   
start_threads(threads)

os.remove(path)

print("---YT2MP3 Finished---")
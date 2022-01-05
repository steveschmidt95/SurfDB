# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 22:40:12 2021

@author: piasm1
"""

from youtube_dl import YoutubeDL
import ffmpeg
import time
from pathlib import Path
import os
def hidden_video_url_extractor(youtube_url="https://www.youtube.com/watch?v=NqhAaA2mGcA"):
    """
    #inputs: youtube_url(str) - the url you see in browser when you go to the required video
    #outputs: info['url'] (str - the underlying url for the video needed by ffmpeg 
    #This function takes the URL for a video (i.e. from your browser) and
    #provide the MUX or hidden URL or whatever is needed by ffmpeg
    """
    ydl_options = {}
    #youtube_url = "https://www.youtube.com/watch?v=NqhAaA2mGcA"
    with YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
    return info['url']


def get_video_frame(hidden_url,output_file_name=time.time(),image_save_dir="C:\\Users\\piasm1\\Downloads"):
    #inputs: hidden_url(str) - the MUX/url output by youtube-dl and needed by ffmpeg
    #        output_file_name(float/int) - usually unix timestamp that is assigned to the output image file
    #outputs: stderr_content(str) - one subprocess error from ffmpeg (default None)
    #         stdout_content(str) - the other subprocess error from ffmpeg (default None)
    #This function takes the hidden url for the needed live video and takes a live screenshot
    # and saves it to the input directory
    
    output_file_name = str(output_file_name)+".png"
    stderr_content = None
    stdout_content = None
    
    output_file_path = image_save_dir + '\\' + output_file_name
    try:
         ffmpeg.input(hidden_url) \
             .output(output_file_path, vframes=1) \
             .run(capture_stdout= False,capture_stderr= True)
    except ffmpeg.Error as e:
        print(e.stderr)
        stderr_content = str(e.stderr)
        stdout_content = str(e.stdout)
    
    return stderr_content, stdout_content


def main():
    hidden_url=hidden_video_url_extractor()
    stderr_content,stdout_content = get_video_frame(hidden_url,int(time.time()))
    return stderr_content, stdout_content

stderr_content, stdout_content = main()

# hidden_url=hidden_video_url_extractor()
# hidden_url = "https://manifest.googlevideo.com/api/manifest/hls_playlist/expire/1640314471/ei/B-LEYbi-M4eF6QKjyamABw/ip/216.75.211.6/id/NqhAaA2mGcA.1/itag/95/source/yt_live_broadcast/requiressl/yes/ratebypass/yes/live/1/sgoap/gir%3Dyes%3Bitag%3D140/sgovp/gir%3Dyes%3Bitag%3D136/hls_chunk_host/rr5---sn-jvhj5nu-cvnk.googlevideo.com/playlist_duration/30/manifest_duration/30/vprv/1/playlist_type/DVR/initcwndbps/31600/mh/ml/mm/44/mn/sn-jvhj5nu-cvnk/ms/lva/mv/m/mvi/5/pl/22/dover/11/keepalive/yes/fexp/24001373,24007246/mt/1640292522/sparams/expire,ei,ip,id,itag,source,requiressl,ratebypass,live,sgoap,sgovp,playlist_duration,manifest_duration,vprv,playlist_type/sig/AOq0QJ8wRgIhAL4qgz7pmbc4EL6W3eSjbSU1f0NofSkclptwH0TlzFkqAiEAjNoMrcd6P78b9BNzLWK33cT72DbmT0H2vQT-R5UJH3o%3D/lsparams/hls_chunk_host,initcwndbps,mh,mm,mn,ms,mv,mvi,pl/lsig/AG3C_xAwRQIhAKsV98toIVn8MliBZ1Aak4xQ6yRGqJEPjzCpNLFFI5VYAiAGpl8Z5yTzwmtLOzdhXCALer0IcYd344CZnekyczopsQ%3D%3D/playlist/index.m3u8"
# out,err = get_video_frame(hidden_url,int(time.time()))

# ffmpeg -ss 00:00:15.00 -i "OUTPUT-OF-FIRST URL" -t 00:00:10.00 -c copy out.mp4
# ffmpeg -i "output URL" -vf fps=1/5 out%d.png
# process = (
# try:
    
#      ffmpeg.input(hidden_url) \
#          .output('output%d.png', vframes=1) \
#          .run(capture_stdout= False,capture_stderr= True)
# except ffmpeg.Error as e:
#     print(e.stderr)
#     a = e.stderr
#     b = e.stdout
 # )
# out, err = process.communicate()
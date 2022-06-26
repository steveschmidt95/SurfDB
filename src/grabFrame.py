# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 22:40:12 2021
sad
@author: piasm1
"""

from youtube_dl import YoutubeDL
import ffmpeg
import time
import os


def hidden_video_url_extractor(youtube_url="https://www.youtube.com/watch?v=NqhAaA2mGcA"):
    """
    Parameters
    ----------
    youtube_url : TYPE, optional
        DESCRIPTION. The default is "https://www.youtube.com/watch?v=NqhAaA2mGcA".
    Returns
    -------
    TYPE
        DESCRIPTION.
    """
    """Convert the URL for a video (i.e. from your browser) and provides the MUX or hidden URL or whatever is needed by ffmpeg
    Keyword arguments:
        youtube_url (str) -- the url you see in browser when you go to the subject video (default https://www.youtube.com/watch?v=NqhAaA2mGcA)
    Outputs:
        info['url'] (str) --  the underlying url for the video needed by ffmpeg
    """

    ydl_options = {}
    with YoutubeDL(ydl_options) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
    return info['url']


def get_video_frame(hidden_url, image_save_dir, output_file_path):
    """Take a live screenshot using the hidden url (MUX( for the needed live video and save it to the specified directory

    Keyword arguments:
        hidden_url (str) --  the MUX/url output by youtube-dl and needed by ffmpeg
        image_save_dir (str) -- the directory you want the image saved to
        output_file_name (float/int) -- usually unix timestamp that is assigned to the output image file

    Outputs:
        stderr_content (str) -- one subprocess error from ffmpeg (default None)
        stdout_content (str) -- the other subprocess error from ffmpeg (default None)

    """
    # Check if there is already a output type specified in file name
    output_file_name = str(output_file_path)
    if output_file_name.find('.') == -1:
        output_file_name = output_file_name + ".png"
    stderr_content = None
    stdout_content = None
    image_save_dir = os.path.join(image_save_dir,output_file_name)
    # try to capture a single image frame from the video. Print ffmpeg failure if failed
    try:
        ffmpeg.input(hidden_url) \
            .output(image_save_dir, vframes=1) \
            .run(capture_stdout=False, capture_stderr=True)
    
    except ffmpeg.Error as e:
        print(e.stderr)
        stderr_content = str(e.stderr)
        stdout_content = str(e.stdout)

    return stderr_content, stdout_content
hidden = hidden_video_url_extractor()

get_video_frame(hidden, 'C:\\Users\\Matt', 'nok')
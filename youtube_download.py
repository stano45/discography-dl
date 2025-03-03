from __future__ import unicode_literals

import os
import sys
from contextlib import contextmanager

import yt_dlp as youtube_dl


class YTDL:

    def __init__(self, ydl_opts):
        self.ydl_opts = ydl_opts

    @contextmanager
    def suppress_stdout(self):
        with open(os.devnull, "w") as devnull:
            old_stdout = sys.stdout
            sys.stdout = devnull
            try:
                yield
            finally:
                sys.stdout = old_stdout

    def download_track(
        self,
        target_path,
        artist_name,
        album_title,
        track_title,
        just_meta=False,
    ):
        # append track name to ytsearch option in ytdl
        track_url = "ytsearch1:{} {} {}".format(
            artist_name, album_title, track_title
        )

        # set output path using the user's home directory
        # for cross-platform compatibility
        if not target_path:
            target_path = os.path.join(
                os.path.expanduser("~"),
                "Desktop",
                "discography-dl",
                artist_name,
                album_title,
            )

        # create directory if it doesn't exist
        if not os.path.exists(target_path):
            print("Directory not found, attempting to create it...")
            try:
                os.makedirs(target_path, exist_ok=True)
            except OSError:
                print("Creation of the directory %s failed" % target_path)
            else:
                print("Successfully created the directory %s" % target_path)

        # set the output template using os.path.join
        self.ydl_opts["outtmpl"] = os.path.join(
            target_path,
            "{}.%(ext)s".format(track_title),
        )

        # check if the song is already downloaded
        for file in os.listdir(target_path):
            filename = os.fsdecode(file)
            if filename == "{}.mp3".format(track_title):
                print("File already cached.")
                return None

        try:
            print("-" * 60)
            with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(track_url, download=not just_meta)
        except youtube_dl.utils.DownloadError:
            print("-" * 60)
            print("Video not found.")
            return None
        else:
            print("-" * 60)
            return info_dict["entries"][0]

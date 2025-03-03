from __future__ import unicode_literals

import os
import sys
from contextlib import contextmanager

import yt_dlp


class YoutubeAPI:
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

    def _prepare_target_directory(
        self, target_path, artist_name=None, album_title=None
    ):
        if not target_path:
            if artist_name and album_title:
                target_path = os.path.join(
                    os.path.expanduser("~"),
                    "Desktop",
                    "discography-dl",
                    artist_name,
                    album_title,
                )
            else:
                target_path = os.path.join(
                    os.path.expanduser("~"), "Desktop", "discography-dl"
                )
        if not os.path.exists(target_path):
            print("Directory not found, attempting to create it...")
            try:
                os.makedirs(target_path, exist_ok=True)
            except OSError:
                print("Creation of the directory %s failed" % target_path)
            else:
                print("Successfully created the directory %s" % target_path)
        return target_path

    def _set_output_template(self, target_path, output_name):
        self.ydl_opts["outtmpl"] = os.path.join(
            target_path,
            "{}.%(ext)s".format(output_name),
        )

    def _file_already_downloaded(self, target_path, output_name):
        for file in os.listdir(target_path):
            filename = os.fsdecode(file)
            if filename == "{}.mp3".format(output_name):
                print("Track already downloaded, skipping.")
                return True
        return False

    def download_from_track_title(
        self,
        target_path,
        artist_name,
        album_title,
        track_title,
        just_meta=False,
    ):
        # Construct the search URL
        track_url = "ytsearch1:{} {}".format(artist_name, track_title)

        # Prepare the target directory
        target_path = self._prepare_target_directory(
            target_path, artist_name, album_title
        )

        # Set the output file template
        self._set_output_template(target_path, track_title)

        # Check if the file already exists
        if self._file_already_downloaded(target_path, track_title):
            return None

        try:
            print("-" * 60)
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(track_url, download=not just_meta)
        except yt_dlp.utils.DownloadError:
            print("-" * 60)
            print("Video not found.")
            return None
        else:
            print("-" * 60)
            return info_dict["entries"][0]

    def download_from_url(
        self,
        target_path,
        url,
        output_name,
        artist_name=None,
        album_title=None,
        just_meta=False,
    ):
        # Prepare the target directory using provided artist
        # and album if available
        target_path = self._prepare_target_directory(
            target_path, artist_name, album_title
        )

        # Set the output file template using output_name
        self._set_output_template(target_path, output_name)

        # Check if the file already exists
        if self._file_already_downloaded(target_path, output_name):
            return None

        try:
            print("-" * 60)
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=not just_meta)
        except yt_dlp.utils.DownloadError:
            print("-" * 60)
            print("Video not found.")
            return None
        else:
            print("-" * 60)
            # If the info_dict contains multiple entries, return the first one
            if "entries" in info_dict:
                return info_dict["entries"][0]
            return info_dict

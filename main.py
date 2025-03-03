import sys

from musicbrainz import TrackQuery
from youtube_download import YTDL

ydl_opts = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }
    ],
}
yt = YTDL(ydl_opts)


def enter_artist():
    while True:
        artist_name = input("\nEnter artist name: \n")
        if artist_name:
            return artist_name


def try_again():
    while True:
        return (
            True
            if input(
                "\nScraping unsuccessful, try again?\n"
                "(type y for yes; press any key for no)\n"
            ).lower()
            == "y"
            else False
        )


def confirm_download(meta_data):
    answer = input(
        "\nIs this the correct video?:"
        "\n Name: {}"
        "\n Duration: {}"
        "\n YT URL: {}"
        "\n (type y for yes; any key for no; q to quit)\n".format(
            meta_data["title"], meta_data["duration"], meta_data["webpage_url"]
        )
    ).lower()
    if answer == "y":
        return True
    elif answer == "q":
        sys.exit()
    else:
        return False


def enter_path():
    answer = input(
        "\nEnter path for discography-dl to save albums "
        "(leave empty to create folder on desktop): \n"
    )
    return answer


def select_mode():
    answer = input(
        "\nEnable interactive mode?\n"
        "Note: some tracks might be incorrectly chosen in automatic mode.\n"
        "(type y for interactive; any key for automatic)\n"
    )
    return True if answer.lower() == "y" else False


def download_track(target_path, artist_name, album_title, track_title):
    print(f"\nDownloading track: {track_title}")
    if yt.download_track(
        album_title=album_title,
        target_path=target_path,
        track_title=track_title,
        artist_name=artist_name,
    ):
        print("\nDownload successful.\n")
    else:
        print("\nDownload unsuccessful.\n")
    print("---------------------------------------------------------------")


def main():
    target_path = enter_path()
    is_interactive = select_mode()

    while True:
        artist_name = enter_artist()
        track_query = TrackQuery(artist_name)
        # Replace artist name with the one returned by the scraper
        artist_name, album_title, track_list = track_query.get_album_tracks()
        if len(track_list) < 1:
            if try_again():
                main()
            else:
                sys.exit()
        for track_title in track_list:
            if is_interactive:
                print("-" * 60)
                print(
                    "\nDownloading info about track: {}\n".format(track_title)
                )
                meta = yt.download_track(
                    album_title=album_title,
                    target_path=target_path,
                    track_title=track_title,
                    artist_name=artist_name,
                    just_meta=True,
                )
                if meta and confirm_download(meta):
                    download_track(
                        album_title=album_title,
                        target_path=target_path,
                        track_title=track_title,
                        artist_name=artist_name,
                    )
            else:
                download_track(
                    album_title=album_title,
                    target_path=target_path,
                    track_title=track_title,
                    artist_name=artist_name,
                )

        answer = input(
            "\nEnd of track list reached. Do you want to continue with"
            " another album? (press y for yes; press any key for no)\n"
        )
        if answer != "y":
            break


if __name__ == "__main__":
    main()

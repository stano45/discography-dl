import requests


class TrackQuery:
    def __init__(self, artist):
        self.artist = artist

    def _search_artists(self):
        """Search for artists by name."""
        url = "https://musicbrainz.org/ws/2/artist"
        headers = {
            "User-Agent": "MusicBrainzPythonApp/1.0 (example@example.com)"
        }
        params = {
            "query": f"artist:{self.artist}",
            "fmt": "json",
            "limit": 10,  # limit results for simplicity
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error fetching artist information.")
            return []
        data = response.json()
        return data.get("artists", [])

    def _choose_from_list(self, items, item_type="item"):
        """Display a list of items and prompt the user to choose one."""
        if item_type == "album":
            # Sort albums by 'first-release-date'
            items = sorted(
                items, key=lambda x: x.get("first-release-date", "")
            )
        elif item_type == "release":
            # Sort releases by 'date'
            items = sorted(items, key=lambda x: x.get("date", ""))

        for i, item in enumerate(items):
            if item_type == "artist":
                display = item.get("name", "Unknown")
                if "disambiguation" in item:
                    display += f" ({item['disambiguation']})"
                elif "country" in item:
                    display += f" ({item['country']})"
            elif item_type == "album":
                display = item.get("title", "Unknown Title")
                if "first-release-date" in item:
                    display += f" (Release Date: {item['first-release-date']})"
            elif item_type == "release":
                display = item.get("title", "Unknown Title")
                if "country" in item:
                    display += f" (Country: {item['country']})"
                if "date" in item:
                    display += f" (Release Date: {item['date']})"
            else:
                display = item
            print(f"{i+1}. {display}")

        choice = None
        while choice is None:
            try:
                selection = int(
                    input(f"Select a {item_type} by number (1-{len(items)}): ")
                )
                if 1 <= selection <= len(items):
                    choice = items[selection - 1]
                else:
                    print("Invalid selection, try again.")
            except ValueError:
                print("Please enter a valid number.")

        return choice

    def _browse_release_groups(self, artist_mbid):
        """Retrieve release groups (albums) for an artist."""
        url = "https://musicbrainz.org/ws/2/release-group"
        headers = {
            "User-Agent": "MusicBrainzPythonApp/1.0 (example@example.com)"
        }
        params = {
            "artist": artist_mbid,
            "type": "album",
            "fmt": "json",
            "limit": 100,
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error fetching release groups.")
            return []
        data = response.json()
        return data.get("release-groups", [])

    def _lookup_release_group(self, release_group_mbid):
        """Lookup a release group to get its releases."""
        url = (
            f"https://musicbrainz.org/ws/2/release-group/{release_group_mbid}"
        )
        headers = {
            "User-Agent": "MusicBrainzPythonApp/1.0 (example@example.com)"
        }
        params = {"inc": "releases", "fmt": "json"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error fetching release group details.")
            return []
        data = response.json()
        return data.get("releases", [])

    def _lookup_release(self, release_mbid):
        """Lookup a release to retrieve its track list."""
        url = f"https://musicbrainz.org/ws/2/release/{release_mbid}"
        headers = {
            "User-Agent": "MusicBrainzPythonApp/1.0 (example@example.com)"
        }
        params = {"inc": "recordings", "fmt": "json"}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print("Error fetching release details.")
            return None
        data = response.json()
        tracks = []
        media_list = data.get("media", [])
        for media in media_list:
            for track in media.get("tracks", []):
                tracks.append(track.get("title", "Unknown"))
        return tracks

    def get_album_tracks(self):
        artists = self._search_artists()
        if not artists:
            print("No artists found.")
            return

        # If multiple artists are found, let the user choose one.
        if len(artists) > 1:
            print("\nMultiple artists found:")
            chosen_artist = self._choose_from_list(artists, item_type="artist")
        else:
            chosen_artist = artists[0]
        artist_name = chosen_artist.get("name", "Unknown")
        print(f"Selected artist: {artist_name}")
        artist_mbid = chosen_artist.get("id")

        # Retrieve albums (release groups) for the selected artist.
        release_groups = self._browse_release_groups(artist_mbid)
        if not release_groups:
            print("No albums found for this artist.")
            return
        print("Albums found:")
        chosen_release_group = self._choose_from_list(
            release_groups, item_type="album"
        )
        album_title = chosen_release_group.get("title", "Unknown")
        print(f"Selected album: {album_title}")
        release_group_mbid = chosen_release_group.get("id")

        # Get releases for the chosen album.
        releases = self._lookup_release_group(release_group_mbid)
        if not releases:
            print("No releases found for this album.")
            return
        if len(releases) > 1:
            print("\nMultiple releases found for this album:")
            chosen_release = self._choose_from_list(
                releases, item_type="release"
            )
        else:
            chosen_release = releases[0]
        release_title = chosen_release.get("title", "Unknown")
        print(f"Selected release: {release_title}")
        release_mbid = chosen_release.get("id")

        # Retrieve and display the track listing.
        tracks = self._lookup_release(release_mbid)
        if tracks:
            print("Tracks: ", tracks)
        else:
            print("No tracks found.")
        return artist_name, album_title, tracks

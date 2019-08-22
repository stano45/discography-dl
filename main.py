from scraper import SongScraper
from youtube_download import YTDL
import sys

ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [
				{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
				 'preferredquality': '192',
				}
			]
		}
yt = YTDL(ydl_opts)		

def enter_artist():
	while(True):
		artist_name = input("\nEnter name of your artist (how you want it to be written in mp3 files): \n")
		if artist_name:
			return artist_name
def try_again():
	while(True):
		return True if input("\nScraping unsuccessful, try again? (press y for yes; press any key for no)\n").lower() == 'y' else False

def confirm_download(meta_data):
	answer = input("\nDo you want to download song?: \n Name: {} \n Duration: {} \n YT URL: {}  \n (press y for yes; any key for no; q to quit)\n".format(meta_data['title'], meta_data['duration'], meta_data['webpage_url'])).lower()
	if answer == 'y':
		return True
	elif answer == 'q':
		sys.exit()
	else:
		return False

def enter_path():
	answer = input("\nEnter absolute path to save songs (leave empty to create folder on desktop): \n")
	return answer

def choose_songs():
	answer = input("Do you wanna choose songs or just download everything? (some songs aren't gonna be what they are supposed to be)\n (press y for yes; any key for no")
	return True if answer.lower() == 'y' else False

def download_song(song, path, artist):
	print("\nDownloading song...")
	if yt.download_song(song_title = song, target_path = path, artist = artist):
		print("\nDownload successful.\n")
	else:
		print("\nDownload unsuccessful.\n")
	print("---------------------------------------------------------------")

def main():
	path = enter_path()
	artist = enter_artist()
	choice_on = choose_songs()
	song_scraper = SongScraper(artist)
	song_list = song_scraper.scrape_songs()
	if len(song_list) < 1:
		if try_again:
			main()
		else:
			sys.exit()
	for song in song_list:
		if choice_on:
			print("---------------------------------------------------------------")
			print("\nDownloading info about song: {}\n".format(song))
			meta = yt.download_song(song_title = song, just_meta = True, artist = artist)
			if meta:
				if confirm_download(meta):
					download_song(song, path, artist)
				else:
					continue
		else:
			download_song(song, path, artist)
				

	answer = input("\n\nEnd of song list reached. Do you want to continue with another arist? (press y for yes; press key for no)")
	if answer == 'y':
		main()
	else:
		sys.exit()

if __name__ == "__main__":
	main()
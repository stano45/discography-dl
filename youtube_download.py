from __future__ import unicode_literals
import youtube_dl, sys, os
from contextlib import contextmanager

class YTDL():

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
	
	def download_song(self, song_title, target_path = None, just_meta = False, artist = ""):
		
		#downloads a song using song title

		#appends song name to ytsearch option in ytdl
		song_url = "ytsearch1:{} {}".format(song_title, artist)
		
		#sets output path
		if not target_path:
			target_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop\\song_script\\{}'.format(artist)) 
		
		if not os.path.exists(target_path):
			print("Dir not found, attempting to create it...")
			try:
				os.mkdir(target_path)
			except OSError:
				print ("Creation of the directory %s failed" % target_path)
			else:
				print ("Successfully created the directory %s " % target_path)
			
		self.ydl_opts['outtmpl'] = '{}\\{} - {}.%(ext)s'.format(target_path, artist, song_title)
		#print (self.ydl_opts['outtmpl'])

		#checks if the song is not already downloaded
		for file in os.listdir(os.path.join(target_path)):
			filename = os.fsdecode(file)
			if filename == "{} - {}.mp3".format(artist, song_title):
				print("File already cached.") 
				return None

		#downloads
		try:
			print("---------------------------------------------------------------")
			with youtube_dl.YoutubeDL(self.ydl_opts) as ydl:
				info_dict = ydl.extract_info(song_url, download = not just_meta) 
		except youtube_dl.utils.DownloadError:
			print("---------------------------------------------------------------")
			print("Video not found.")
			return None
		else:
			print("---------------------------------------------------------------")
			return info_dict['entries'][0]
	
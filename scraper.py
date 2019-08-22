import requests
import urllib.request
from bs4 import BeautifulSoup

class SongScraper():
	def __init__(self, artist):
		#edit artist name so it can be inserted into link
		self.artist = artist.replace(" ", "").lower()

	def has_href_but_no_id(self, tag):
		#find all tags with song names
	    return tag.has_attr('href') and not tag.has_attr('rel') and not tag.has_attr('style')

	def scrape_songs(self):
		#append artist name to song database url
		url = "http://www.song-list.net/{}/songs".format(self.artist)
		
		#get html doc
		try:
			response = requests.get(url)
		except requests.exceptions.RequestException as e: 
			print(e)
		soup = BeautifulSoup(response.text, "html.parser")

		#find all elements that match function
		names = soup.find_all(self.has_href_but_no_id)

		#append all of them into a list (except last two which aren't song names)
		song_list = []
		for song_name in names:
			song_list.append(song_name.string)
		return song_list[:len(song_list)-2]

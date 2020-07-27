import os
import re
import json
import urllib
import argparse

from web_crawl_tools import (soup_maker, download_file, search_for)
from ui_tools import (print_progress_bar, get_input)

def main_finder (players: dict) -> list:
	'''
	Takes players dict in {player_name: url_to_playlist}  format
	returns mp3 files from all players pages
	'''
	
	download_musics = []
	
	for player_name, player_url in players.items() :
		print(f"-[*] CHECKING: [{player_name}] MUSICS ")
		musics = search_for(player_url, '.mp3', depth = 1, excludes=['remix', '320'], _debug=True)

		for music_url in musics:
			music_name = urllib.parse.unquote(music_url.split('/')[-1])
			#TODO better file search (may be downloaded from diffrent site) can cheack size or msuics meta data for pure music name
			#TODO make a dict with keys = player_name and values = list of music_url
			if music_name not in os.listdir("downloads"):
				download_musics.append(music_url)
				print(f'-[*] FOUND: music_num = {len(download_musics)} / name = {music_name}')
	
	return download_musics
	
if __name__ == "__main__":
	players = {}
	#TODO correct first line of rad (update.txt first line have some symbols wich shold be deleted)
	#TODO add update_method : takes a player name and searches google for playlist
	#TODO argparse to manage output . download links or save them . all/ none/ specified
	 
	#Reads players data from file and pu them in players dictionory
	with open('update_list.json') as f :
		try:
			players = json.load(f)
		except json.decoder.JSONDecodeError :
			players = {}

	downloadable_links = main_finder(players)
	
	#from this part code customize output with user inputs 
	if downloadable_links:	

		output_choice = input("""-[?] Do you want links be saved in output.txt ? 
	-a to save all musics links
	-n to don't save any music links
	-s {musics nums with space betwine} to save specefic musics links\n-> """)

		if '-a' in output_choice :
			output_links = downloadable_links
		elif '-n' in output_choice :
			output_links = []
		elif '-s' in output_choice :
			output_choiced_nums = output_choice.split(' ')[1:]
			output_links = [link for num, link in enumerate(downloadable_links) if str(num+1) in output_choiced_nums]
					
		with open('output.txt', 'a') as file :
			for link in output_links:
				file.write(str(link.encode()))
		print(f'-[*] {len(output_links)} Links saved in output.txt')

		download_choice = input("""-[?] Do you want links be downloaded ? 
	-a to download all musics
	-n to don't download any music
	-d {musics nums with space betwine} to download specefic musics\n-> """)

		
		if 'downloads' not in os.listdir():
			os.mkdir('downloads')
	
		if '-a' in download_choice :
			download_links = downloadable_links
		elif '-n' in download_choice :
			download_links = []
		elif '-s' in download_choice :
			download_choiced_nums = download_choice.split(' ')[1:]
			download_links = [link for num, link in enumerate(downloadable_links) if str(num+1) in download_choiced_nums]
		
		for link in download_links:
			download_file(link, dir='downloads/', verbose=True)
			print(f"-[*] {link.split('/')[-1]} downloaded")

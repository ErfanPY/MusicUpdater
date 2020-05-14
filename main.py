import os
import re
import urllib

from web_crawl_tools import (soup_maker, download_file, search_for)
from ui_tools import (print_progress_bar, get_input)

def main (players: dict) -> list:
	'''
	Takes players dict in {player_name: url_to_playlist}  
	returns mp3 files from all players pages
	'''
	
	download_musics = []
	
	for player_name, player_url in players.items() :
		print(f'checking for {player_name} musics')
		musics = search_for(player_url, '.mp3', depth = 0, excludes=['remix', '320'])
		for music_url in musics:
			music_name = urllib.parse.unquote(music_url.split('/')[-1])
			#TODO better file search (may be downloaded from diffrent site) can cheack size or msuics meta data for pure music name
			#TODO make a dict with keys = player_name and values =list of music_url
			if music_name not in os.listdir("downloads") :
				download_musics.append(music_url)
				print(f'#ADED: {music_name}')
	
	return download_musics
	
if __name__ == "__main__":
	players = {}
	#TODO correct first line of rad (first line have some symbols wich shold be deleted)
	#Reads players data from file and pu them in players dictionory
	with open("update_list.txt") as file:
		for line in file.readlines() :
			name , url = line.split(':', maxsplit=1)
			players[name] = url
	
	download_links = main(players)
	
	print(f'-[*] {len(download_links)} music found ')

	if download_links and input('-[?] Do you want links be saved in output.txt ? (y/n)') in ['y', '']:
		with open('output.txt', 'a') as file :
			for link in download_links:
				file.write(str(link.encode()))
		print('-[*] Links saved in output.txt')

	if  download_links and  input('-[?] Do you want to musics be dowloaded ? (y/n)').lower() in ['y', '']:
		if 'downloads' not in os.listdir():
			os.mkdir('downloads')
		for link in download_links:
			download_file(link, dir='downloads/', verbose=True)
			print(f"-[*] {link.split('/')[-1]} downloaded")

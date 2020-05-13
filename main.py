import os
import re
import urllib

from web_crawl_tools import (soup_maker, download_file, type_finder)
from ui_tools import (print_progress_bar, get_input)

def main ():
	'''
	Takes players name with a url to page of their music list from update_list.txt and 
	 adds all mp3 files to output.txt 
	'''
	
	if 'downloads' not in os.listdir():
		os.mkdir('downloads')
	players = {}
	#TODO correct first line of rad (first line have some symbols wich shold be deleted)
	
	#Reads playesrs data from file and pu them in players dictionory
	with open("update_list.txt")as file:
		for   line in file.readlines() :
			name , url = line.split(':', maxsplit=1)
			players[name] = url

	download_musics = []
	for player_name, player_url in players.items() :
		print(f'checking for {player_name} musics')
		musics = type_finder(player_url, '.mp3')
		for music_url in musics:
			music_name = urllib.parse.unquote(music_url.split('/')[-1])
			#TODO better file search (may be downloaded from diffrent site) can cheack size or msuics meta data for pure music name
			#TODO make a dict with keys = player_name and values =list of music_url
			if music_name not in os.listdir("downloads") :
				download_musics.append(music_url)
				print(f'#ADED: {music_name}')

	with open('output.txt', 'w') as file :
		for link in download_musics:
			file.write(str(link.encode()))
	
	print(f'[ {len(download_musics)} ] music aded. ')
	if  download_musics and  input('Do you want to musics be dowloaded ? (y/n)').lower() == 'y':
		for link in download_musics:
			download_file(link, dir='downloads/', verbose=True)
			print(f"[*] {link.split('/')[-1]} downloaded")

if __name__ == "__main__":
	type_finder('https://birseda.net/tag/%D8%AC%D8%AF%D9%8A%D8%AF%D8%AA%D8%B1%D9%8A%D9%86-%D8%A2%D9%87%D9%86%DA%AF-%D8%A7%D9%85%DB%8C%D8%B1-%D8%AA%D8%AA%D9%84%D9%88/', '')
	#link, quality = get_input()

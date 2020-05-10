from extra import (usage, get_music_links, get_input, os, argparse, sys)

#players file contains data of musicplayers and url to 
#[["name", "url"], ["name", "url"], ["name", "url"]]

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
		for line in file.readlines() :
			name , url = line.split(':', maxsplit=1)
			players[name] = url

	download_musics = []
	for player_name, player_url in players.items() :
		print(f'checking for {player_name} musics')
		musics = get_music_links(url = player_url)
		for music_url in musics:
			music_name = music_url.split('/')[-1]
			#TODO better file search (may be downloaded from diffrent site) can cheack size or msuics meta data for pure music name
			#TODO make a dict with keys = player_name and values =list of music_url
			if music_name not in os.listdir("downloads") :
				download_musics.append(music_url)
				print(f'#ADED: {music_name}')

	with open('output.txt', 'w') as file :
		for link in download_musics:
			file.write(str(link.encode()))
	
	print(f'[ {len(download_musics)} ] music aded. ')

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		get_input()
	else :
		main()

from extra import (usage, get_music_links, os, argparse, sys)

#profile file contains data of musicplayers and url to 
#[["name", "url"], ["name", "url"], ["name", "url"]]

def main ():
	if 'downloads' not in os.listdir():
		os.mkdir('downloads')
	profile = {}
	#TODO correct first line of rad (first line have some symbols wich shold be deleted)
	with open("update_list.txt")as file:
		for line in file.readlines() :
			name , url = line.split(':', maxsplit=1)
			profile[name] = url

	download_musics = []
	print(profile)
	for player_name, player_url in profile.items() :
		print(f'checking for {player_name} musics')
		musics = get_music_links(url = player_url)
		for music_url in musics:
			music_name = music_url.split('/')[-1]
			#TODO better file search (may be downloaded from diffrent site) can cheack size or msuics meta data for pure music name
			#TODO make a dict with keys = player_name and values =list of music_url
			if music_name not in os.listdir("downloads") :
				download_musics.append(music_url)
	with open('output.txt', 'w') as file :
		for link in download_musics:
			file.write(str(link.encode()))

#TODO correct get_input function and CLI interface
def get_input() :
	"""inputs :
	1) path to music play list
	2) list of singers
	3) list of sites to check for specefic singers
	4)
	arguments :
	1) -d download files
	2) -s save this template for next updates
	3)  
	"""
	parser = argparse.ArgumentParser(description="Music Assistant", usage=usage())
	parser.add_argument("link", help="main page Link")
	parser.add_argument("-q", "--quality", help="eg: [124, 360, 480, 720, ...]", default='480')
	'''parser.add_argument("--debug", action="store_true")'''
	args = parser.parse_args()
	link = args.link
	quality = args.quality

	if args.quality :
		main()
	else:
		usage()

if __name__ == "__main__":
	if len(sys.argv) >= 2:
		get_input()
	else :
		main()

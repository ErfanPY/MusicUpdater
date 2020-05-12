from extra import (soup_maker usage, get_music_links, get_input, os, argparse, sys, download_file, urllib)

def type_finder (url, file_format):
	soup = soup_maker(url= url)
    if soup :
        links = [i.get('href') for i in soup.find_all('a')]
    else :
        return
    
    type_links = []
	
    for limk in links :
        if link and file_format in link:
            type_links.append(link)
    
	return (type_links)

def search_for (base_url, file_format = 'mp3', depth = 0):
	"""
	search for a spesefic file_format in all page from base_url to all link in that page until reach the depth
	@params:
	base_url    - Required  : page to start searching (Str)
	file_format - Optional  : type of file to search in pages (default = mp3) (Str)
	depth       - Optional  : how much deep should search (default = 0) (Int)
	"""
	res = []

	res.append(type_finder(base_url, file_format))
	childs = type_finder(base_url)#TODO find html page from link of site
	for child in childs:
		res.append(search_for(child))#TODO search for in all link in this page for file types
	return res

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
		musics = get_music_links(url = player_url)
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
	if len(sys.argv) >= 2:
		get_input()
	else :
		main()

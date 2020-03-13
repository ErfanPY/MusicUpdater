import os
import re
import io
import time
import argparse
import requests
import urllib.parse

#import pyautogui
#from googlesearch import search
from bs4 import BeautifulSoup as bs


# two level page search to find music files 

#functions [labtar:downloader(*soupMaker, *printProgressBar, *resume_download, *download_file),
#           justsayname:(googleReq, getRightOneNum, *checkMusicLinks, siteDownload)]

def soup_maker(url=None, html=None):
	#Make a soup obj from url or html file
	if html :
		data = html
	else : 
		try :
			data = requests.get(url, timeout=10).content
		except requests.exceptions.ReadTimeout:
			return 
	soup = bs(data, 'html.parser')
	return (soup)

def get_music_links (url=None, html=None):
    #Checking for musicS link
    soup = soup_maker(url= url, html=html)
    if soup :
        links = [i.get('href') for i in soup.find_all('a')]
    else :
        return
    
    download_links = []
    for i in links :
        if i and ( '.zip' in i or '.rar' in i and not '128' in i):
            download_links.append(i)
        elif i and '.mp3' in i and not '128' in i :
            download_links.append(i)

    return (download_links)

def download_file(url, dir='download/', verbose=True):
	""" download file in specefic directory will log what do if verbose is True"""
	start = time.time()
	# NOTe the stream=True parameter below

	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with io.BytesIO() as f:
			iter_num = 0
			size = int(r.headers['content-length'] )
			total = size // 1000000
			if verbose : print_progress_bar(iter_num, total, prefix = 'Progress', suffix = 'Complete', length = 50)

			for chunk in r.iter_content(chunk_size=4096*4096):
				if chunk: # filter out keep-alive new ch
					f.write(chunk)
					iter_num += 1
					if verbose : print_progress_bar(iter_num, total, prefix = 'Progress', suffix = 'Complete', length = 50)
					f.flush()

			filename = url.split('/')[-1]
			file_path = str(dir) + str(filename)
			open(file_path, 'ab').write(f.getvalue())
	end = time.time()
	if verbose : print('##########{}##########'.format((end-start)))
	return file_path

def resume_download(fileurl, resume_byte_pos):
    resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
    return requests.get(fileurl, headers=resume_header, stream=True,  verify=False, allow_redirects=True)

def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█'):
	"""
	Call in a loop to create terminal progress bar
	@params:
	iteration   - Required  : current iteration (Int)
	total       - Required  : total iterations (Int)
	prefix      - Optional  : prefix string (Str)
	suffix      - Optional  : suffix string (Str)
	decimals    - Optional  : positive number of decimals in percent complete (Int)
	length      - Optional  : character length of bar (Int)
	fill        - Optional  : bar fill character (Str)
	"""
	percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
	filledLength = int(length * iteration // total)
	bar = fill * filledLength + '-' * (length - filledLength)
	print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = '\r')
	# Print New Line on Complete
	if iteration == total:
		print()

#TODO
def usage():
    return """
        Use "" around link to avoid bad things :>
        adp.py "{Link}" [quality]
        python apd.py "https://www.aparat.com/v/d13rh3"
        python apd.py "https://www.aparat.com/v/d13rh3" -q 480

        The default quality is 480.
    """

def main ():
	pass

if __name__ == "__main__":
	"""inputs :
	1) path to music play list
	2) list of singers
	3) list of sites to check for specefic singers
	4)
	arguments :
	1) -d download files
	2) -s save thsi tanplate for next updates
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

	test = 'http://iranjavanmusic.com/playlist/%d8%a7%d9%85%db%8c%d8%b1-%d8%aa%d8%aa%d9%84%d9%88/'
	req = requests.get(test).content
	soup = bs(req, features="html.parser")
	musics_container = soup.find(name='div', attrs={"class":"cplayer"})
	musics_list = list(musics_container.find_all(name='div', attrs={"class":"item"}))
	musics_dict = {}
	for music in musics_list :
		href = music.find(name='a', attrs={"title":"Mp3 320"}).get("href")
		name = href.split("/")[-1]
'''
with open("updateList.txt", 'r') as file:
for line in file.readlines():
	print(line)
'''
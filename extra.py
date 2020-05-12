import os
import re
import io
import time
import sys
import argparse
import urllib.parse

import requests
from bs4 import BeautifulSoup as bs

#functions [labtar:downloader(*soupMaker, *printProgressBar, *resume_download, *download_file),
#           justsayname:(googleReq, getRightOneNum, *checkMusicLinks, siteDownload)]
	
def soup_maker(url=None, html=None):
	#Make a soup obj from url or html file
	#TODO error reporting
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
	#TODO chose quality for music links
    for i in links :
        if i and ( '.zip' in i or '.rar' in i and not '128' in i):
            download_links.append(i)
        elif i and '.mp3' in i and '128' in i :
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

			filename = urllib.parse.unquote(url.split('/')[-1])
			file_path = str(dir) + str(filename)
			with open(file_path, 'ab') as output:
				output.write(f.getvalue())
	end = time.time()
	if verbose : print(f'[*] Download taked {end-start} s\n')
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


def usage():
    return """
        Use "" around link to avoid bad things :>
        adp.py "{Link}" [quality]
        python apd.py "https://www.aparat.com/v/d13rh3"
        python apd.py "https://www.aparat.com/v/d13rh3" -q 480

        The default quality is 480.
    """

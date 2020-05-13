import io
import time
import requests
from urllib.parse import urlparse, unquote

from bs4 import BeautifulSoup as bs

from ui_tools import print_progress_bar

#TODO search from google
#TODO search for a content is site (soup.select)(with css selector)
#a = soup_maker('https://www.mtvpersian.net/artist/amir-tataloo/?mp3s=1').select('html body main div.wrapper a.artistpro b')

def soup_maker(url=None, html=None):
	#Make a soup obj from url or html file
	#TODO error reporting
	if html :
		data = html
	else : 
		try :
			data = requests.get(url, timeout=10).content
		except Exception:
			return 
	soup = bs(data, 'html.parser')
	return (soup)

def type_finder (url: str, file_format: str) -> list:
	#TODO add filter list for better search : a filter list for words wich should be in link and a filter list to not be in link
	# e.g : for music file a filter can be music quality if 320 in link it sould be appended
	#TODO multy file_format search 
	soup = soup_maker(url= url)
	if soup :
		links = set([i.get('href') for i in soup.find_all('a')])
	else :
		return
    
	found_links = list()
	base_netloc = urlparse(url).netloc.split('.')[-2:]

	for link in links :
		if not link : continue
		link_type = urlparse(link).path.split('/')[-1]
		link_netloc = urlparse(link).netloc.split('.')[-2:]
		if link != url and base_netloc == link_netloc and link_type.endswith(file_format) and not link in found_links:
			found_links.append(link)

	return found_links

def search_for (base_url: str, file_format: str, depth: int = 0, _far: int =0, _debug: bool =False) -> list:
	"""
	search for a spesefic file_format in all page from base_url to all link in that page until reach the depth
	@params:
	base_url    - Required  : page to start searching (Str)
	file_format - Required  : type of file to search in pages (Str)
	depth       - Optional  : how much deep should search (default = 0) (Int)
	"""
	res = list()
	if _debug : print(f"[*] {'-'*_far} fearching for [{file_format}] in \"{unquote(base_url)}\"")
	#TODO make a tree of what pages we searched and show it in cli
	[res.append(i) for i in type_finder(base_url, file_format) if i and not i in res]
	if depth > 0:
		childs = type_finder(base_url, '')#matchs any link of any page
		for child in childs:
			[res.append(i) for i in search_for(child, '.mp3', depth-1, _far+1) if i and not i in res]
	return res

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

			filename = unquote(url.split('/')[-1])
			file_path = str(dir) + str(filename)
			with open(file_path, 'ab') as output:
				output.write(f.getvalue())
	end = time.time()
	if verbose : print(f'[*] Download taked {end-start} s\n')
	return file_path


def resume_download(fileurl, resume_byte_pos):
    resume_header = {'Range': 'bytes=%d-' % resume_byte_pos}
    return requests.get(fileurl, headers=resume_header, stream=True,  verify=False, allow_redirects=True)

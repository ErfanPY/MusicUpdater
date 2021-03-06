import io
import time
import requests
from urllib.parse import urlparse, unquote

from bs4 import BeautifulSoup as bs

from ui_tools import print_progress_bar

#TODO search from google
#TODO search for a content is site (soup.select)(with css selector)
#a = soup_maker('https://www.mtvpersian.net/artist/amir-tataloo/?mp3s=1').select('html body main div.wrapper a.artistpro b')

def inc_exc_filter (text, includes, excludes):
    '''
    checks if all includes are in text and no one from excludes is in text
    '''
    for inc in includes:
        if not inc.lower() in text.lower():
            return False
    for exc in excludes:
        if exc.lower() in text.lower():
            return False
    return True

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

def _type_finder (url: str, file_format: str,
				includes: list =[], excludes: list =[]) -> list:
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
		if (not link) and (link == url) and (link in found_links) and (not inc_exc_filter(link, includes, excludes)): continue
		link_type = urlparse(link).path.split('/')[-1]
		link_netloc = urlparse(link).netloc.split('.')[-2:]
		if (link_type.endswith(file_format)) and (base_netloc == link_netloc):
			found_links.append(link)

	return found_links

def search_for (base_url: str, file_format: str, depth: int = 0,
				includes: list =[], excludes: list =[],
				_far: int =0, _debug: bool =False) -> list:
	"""
	search for a spesefic file_format in all page from base_url to all link in that page until reach the depth
	@params:
	base_url    - Required  : page to start searching (Str)
	file_format - Required  : type of file to search in pages (Str)
	depth       - Optional  : how much deep should search (default = 0) (Int)
	includes    - Optional  : list of str (utf-8 encoded) words should be in result (default = []) (List)
	excludes    - Optional  : list of str (utf-8 encoded) words should not be in result (default = []) (List)
	"""
	results = list()
	if _debug : print(f"[*] {'-'*_far} fearching for [{file_format}] in \"{unquote(base_url)}\"")
	#TODO make a tree of what pages we searched and show it in cli
	#TODO add a max_page param to limitait the number of page search
	#TODO add include exclude filter

	for i in _type_finder(base_url, file_format, includes = includes, excludes = excludes):
		if i and not i in results:
			results.append(i)

	if depth > 0:
		childs = _type_finder(base_url, '')#matchs links to other pages (not files)
		for child in childs:
			child_returns = search_for(child, '.mp3', depth= depth-1, _far= _far+1, includes = includes, excludes = excludes)
			[results.append(i) for i in child_returns if i and not i in results]

	return results

def download_file(url, dir='download/', verbose=True):
	""" download file in specefic directory will log what do if verbose is True"""
	start = time.time()
	#NOTE the stream=True parameter below

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

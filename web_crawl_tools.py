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


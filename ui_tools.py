
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

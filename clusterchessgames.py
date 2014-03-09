from datetime import datetime
startTime = datetime.now()
from pprint import pprint

def compression_distance(data_x, data_y, compressor = "zlib", level = 6, precompressed = 0):
	if compressor == "zlib":
		#print "Using ZLIB"
		from zlib import compress
		from zlib import decompress
	if compressor == "bz2":
		#print "Using BZIP"
		from bz2 import compress
		from bz2 import decompress
	if compressor == "lzo":
		#print "Using LZO"
		from lzo import compress
		from lzo import decompress
	if compressor == "pylzma":
		#print "Using PYLZMA"
		from pylzma import compress
		from pylzma import decompress
	if precompressed == 0:
		c_x = len(compress(data_x, level))
		c_y = len(compress(data_y, level))
		c_x_y = len(compress(data_x + " " + data_y, level))
	else:
		c_x = len(data_x)
		c_y = len(data_y)
		c_x_y = len(compress(decompress(data_x) + " " + decompress(data_y), level))
	ncd = (c_x_y - min(c_x, c_y)) / float(max(c_x, c_y))
	return ncd

def clean_chess_games(data):
	from random import shuffle
	games = ""
	lines = data.split('\n')
	shuffle(lines)
	for line in lines:
		if line[0:2] == "1.":
			games += " " + line
	return games
	
def ncd_cluster_files_3(glob_files, compressor = "zlib", level = 6, precompressed = 0):
	from glob import glob
	from itertools import combinations
	file_datas = {}
	files = glob(glob_files)
	for filec in files:
		file_datas[filec] = clean_chess_games(open(filec).read())
	i =0
	scores = []
	single_scores = {}
	for combo in combinations(files, 2):
		distance_single_link = compression_distance(file_datas[combo[0]], file_datas[combo[1]], compressor, level)
		#print combo[0], combo[1], distance_single_link
		single_scores[combo[0]+combo[1]] = distance_single_link
		single_scores[combo[1]+combo[0]] = distance_single_link

	for combo in combinations(files, 3):
		#print combo[0], combo[1], combo[2]
		v1 = single_scores[combo[0]+combo[1]]
		v2 = single_scores[combo[0]+combo[2]]
		v3 = single_scores[combo[1]+combo[2]]
		score = (v1 + v2 + v3) / float(3)
		scores.append((score, combo[0], combo[1], combo[2]))
		#print score, i
		i += 1
	done = []
	print "Using compressor:", compressor
	for item in sorted(scores):
		if item[1] not in done and item[2] not in done and item[3] not in done:
			done.append(item[1])
			done.append(item[2])
			done.append(item[3])
			print item
	print "Script execution time:", str(datetime.now()-startTime)[0:7]

ncd_cluster_files_3("data/chessgames/*_.txt", "bz2", 9)
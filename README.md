#Normalized Compression Distance#
Experiments and research into Normalized Compression Distance (NCD).

##What is NCD?##
NCD, in layman terms, works on the principle that two files which share data patterns compress better when you add them together, than two files which don't share data patterns, since compressors are more efficient when dealing with repeating data patterns.

Further reading:
- [http://en.wikipedia.org/wiki/Normalized_Compression_Distance](http://en.wikipedia.org/wiki/Normalized_Compression_Distance)
- [http://complearn.org/ncd.html](http://complearn.org/ncd.html)
- [Clustering by compression [pdf]](http://homepages.cwi.nl/~paulv/papers/cluster.pdf)

###Very simple example###
File A contents

	CCCCCCCCCCCC
	
File B contents

	CCCCCCCCCCCA
	
File C contents

	AAAABBBBBBPQ

Using a very basic compressor called a Run-Length Encoder (RLE) we can compress these file contents.

File A contents compressed

	12xC
	
File B contents compressed

	11xC,A
	
File C contents compressed

	4xA,6xB,PQ

To get a similarity measure between files, you add two files together and look at the length of their compression.

File A contents + File B contents

	CCCCCCCCCCCCCCCCCCCCCCCA
	
File A + File B compressed

	23xC,A
	
Which gives a compressed length of 6.

File B contents + File C contents

	CCCCCCCCCCCAAAAABBBBBBPQ

File B + File C compressed
	
	11xC,5xA,6xB,PQ
	
Which gives a compressed length of 15.

As the files are already of equal length, we don't need normalization to spot that File A and File B are more alike, than File B and File C.

NCD is an approximation. We would like to use the Kolmogorov Complexity (KC) for a string, but KC is incomputable. Better compressors are valuable to increase NCD's accuracy and AI in general, so much so that Marcus Hutter made a price for it [50'000€ Prize for Compressing Human Knowledge](http://prize.hutter1.net/)

###Uses of NCD###
NCD gives a similarity measure between two files or data streams which can be used to cluster, classify, compare, or even fed to autonomous agents.

##clusterchessgames.py##
###Description###
Clusters 21 files containing game data from 7 Grandmasters. All games played by a Grandmaster with the white pieces are stored inside a .txt file. This .txt file is split up in 3 smaller .txt files, which are randomized and stripped of meta-data (like the dates, locations, tournament or player names). 

The challenge is to create 7 clusters containing the game data files belonging to the same Grandmaster. Opponent moves not stripped from the data. This makes the data less indicative of the Grandmaster's unique style (data patterns) we hope to find. This adds to the challenge.

Expert knowledge or chess domain knowledge isn't required for good results. An International Master confronted with this challenge claimed the challenge is impossible to do by hand and would take hours to even analyze.
###Dependancies###
datetime, pprint, random, glob, itertools, and at least one of the following compression libs: zlib, bz2, lzo, pylzma

###Sample input###
	1.Sf3 Sf6 2.c4 b6 3.g3 Lb7 4.Lg2 c5 5.0-0 g6 6.b3 Lg7 7.Lb2 0-0 8.Sc3 Sa6 9.d4 d5 10.dxc5 Sxc5 11.Sxd5 Sxd5 12.Lxg7 Kxg7 13.cxd5 Dxd5 14.Dxd5 Lxd5 15.Tfd1 ½-½ 1.d4 e6 2.e4 d5 3.Sd2 c5 4.exd5 exd5 5.Lb5+ Ld7 6.De2+ Le7 7.dxc5 Sf6 8.Sb3 0-0 9.Le3 Te8 10.Sf3 a6 11.Lxd7 Sbxd7 12.0-0 Sxc5 13.Sfd4 ½-½ 1.e4 c5 2.Sf3 Sc6 ...

###Sample output###
Using the following 7 Grandmasters, inspired by some of Fischer's favorite opponents:
- (A) Gligoric
- (B) Petrosian
- (C) Reshevsky
- (D) Spassky
- (E) Tal
- (F) Botvinnik
- (G) Larsen

this script gives us the following clusters, together with their fitness/similarity score:

	Using compressor: bz2
	(0.9187782850134746, 'data/chessgames\\C1_.txt', 'data/chessgames\\C2_.txt', 'data/chessgames\\F1_.txt')
	(0.9213097232083918, 'data/chessgames\\D2_.txt', 'data/chessgames\\E1_.txt', 'data/chessgames\\E2_.txt')
	(0.9255006608357625, 'data/chessgames\\B1_.txt', 'data/chessgames\\B2_.txt', 'data/chessgames\\B3_.txt')
	(0.9275354033562815, 'data/chessgames\\G1_.txt', 'data/chessgames\\G2_.txt', 'data/chessgames\\G3_.txt')
	(0.9286958400620074, 'data/chessgames\\A1_.txt', 'data/chessgames\\A2_.txt', 'data/chessgames\\A3_.txt')
	(0.931262816636599, 'data/chessgames\\C3_.txt', 'data/chessgames\\F2_.txt', 'data/chessgames\\F3_.txt')
	(0.9343742509153218, 'data/chessgames\\D1_.txt', 'data/chessgames\\D3_.txt', 'data/chessgames\\E3_.txt')
	Script execution time: 0:00:37

Worst possible result is 7 correct guesses. This would mean all clusters contain files from different Grandmasters.

Best possible result is 21 correct guesses. This would mean all clusters contain the files from the same Grandmaster.

The script scores 17 correct guesses for a score of 10/14 or 71%. 

Preliminary observations: Bz2 outperforms other compressors with regards to speed and accuracy. Clustering 15 files or less often results in perfectly correct clusters. Clustering 24 files or more starts to give poor results.

TODO: Look if it is possible to use other cluster algorithms, like k-means, and subdivide the larger clusters using NCD-based clustering. Look at better compressors like PAQ8.
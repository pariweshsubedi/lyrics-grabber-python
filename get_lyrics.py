import os,sys,re,StringIO,urllib2
from lxml import etree

global path

def call_eyed3(f):
	try:
		import eyeD3
		tag = eyeD3.Tag()
		tag.link(f)
		artist = tag.getArtist().lower()
		album = ''.join(tag.getAlbum())
		title = re.sub('[\(\)\{\}\,\.<>]', '', ''.join(tag.getTitle().split(' '))).lower()
		print "\n\nArtist: " + artist + " Title: "+ title	

		get_lyrics(artist,title)
	except:
		print "tag recognition error"
		exit()

def get_lyrics(artist,title):	
	generate_url = 'http://azlyrics.com/lyrics/'+artist+'/'+title +'.html'
	print generate_url
	processing(generate_url, artist, title)
	
def processing(generate_url, artist, title):
	try :
		print "Fetching lyrics to "+ path + "lyrics/"+artist + '_' + title + '.txt'
		print "from " + generate_url 
		response = urllib2.urlopen(generate_url)
		read_lyrics = response.read()
		parser = etree.HTMLParser()
		tree = etree.parse(StringIO.StringIO(read_lyrics), parser)
		lyrics = tree.xpath('''//div[@style='margin-left:10px;margin-right:10px;']/text()''') 
		printing(artist, title, lyrics)
	except:
		"Error fetching from web."

def printing(artist, title, lyrics):
	for words in lyrics:
		# print str(words).strip()
		saving(artist, title, lyrics)
	

def saving(artist, title, lyrics):
	filename = path + "lyrics/"+artist + '_' + title + '.txt'
	f = open(filename, 'w')
	f.write("\n".join(lyrics).strip())
	f.close()

print len(sys.argv)
if len(sys.argv)==1:					#for the working directory
	path = os.path.abspath(__file__)
	print path
	path = path.split("/")[:-1]
	path = '/'.join(path)+"/"
	files = next(os.walk(path))[2]
elif len(sys.argv)==2:
	path = os.path.abspath(__file__)	#for single audio file
	path = path.split("/")[:-1]
	path = '/'.join(path)+"/"				
	single_file = sys.argv[1]
	call_eyed3(single_file)
	exit()
elif (sys.argv[1])=='-d' and len(sys.argv)==3: #for a directory
	path = sys.argv[2]
	print path
	files = next(os.walk(path))[2]
else:
	print "\n Usage: \n \n 1) python get_lyrics.py [-d] [path to audio directory] \n 2) python get_lyrics.py filename \n "
	exit()

for f in files:
	print f
	call_eyed3(f)


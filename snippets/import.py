import magic
import codecs

def iconv(sourceFilename, sourceEncoding, targetFilename, targetEncoding):
  BLOCKSIZE = 1048576 # or some other, desired size in bytes
  with codecs.open(sourceFilename, "r", sourceEncoding) as sourceFile:
    with codecs.open(targetFilename, "w", targetEncoding) as targetFile:
      while True:
        contents = sourceFile.read(BLOCKSIZE)
        if not contents:
          break
        targetFile.write(contents)

def translate(sourceFilename, targetFilename):
  f = open(sourceFilename, "rb")
  buffer = f.read(1024)
  while buffer:
    
        
    # Do stuff with byte.
    buffer = f.read(1024)


def guess_mime(filename):
  blob = open(filename).read()
  m = magic.open(magic.MAGIC_MIME)
  m.load()
  encoding = m.buffer(blob)
  keywords = encoding.split(';')
  for keyword in keywords:
    if 'charset' in keyword:
      return keyword.split('=')[1]
  

def guess_delimiter(filename):
  f = open(filename,'rb')
  line = f.readline()
  f.close()
  characters = []
  for s in line:
    found = False
    for c in characters:
      if c[0]==s:
        found = True
      c[1]=c[1]+1
    if not found and s in [';',':',' ','|','~','#']:
      characters.append([s,1])
      characters.sort(reverse=True)
  return characters[0][0] 

def load_header(filename, delimiter):
  f = open(filename,'rb')
  line = f.readline()
  f.close()
  headers = line.split(delimiter)
  return headers



client = MongoClient('mongodb://localhost:27017/')
db = client.mydb
collection = db['campaigns']

sourceFilename = 'CLC_Fulfillment_KALCS_2015-02-13_14-07-26_137657_1.txt'
sourceEncoding = guess_mime(sourceFilename)
filename = 'CLC_Fulfillment_KALCS_2015-02-13_14-07-26_137657_1_UTF-8.txt'
iconv(sourceFilename,sourceEncoding,filename,'utf-8')
delimiter = guess_delimiter(filename)
headers = load_header(filename, delimiter)
print headers
print delimiter
print collection

f = open(filename,'rb')
i=0
for line in f:
  if not i==0:    
    columns = line.split(delimiter)
    h = 0
    result = {}
    for c in columns:      
      result[headers[h]]=c
      h = h + 1 
    post_id = collection.insert(result)
  i=i+1
f.close()

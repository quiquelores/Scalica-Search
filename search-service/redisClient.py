import redis
import re
from nltk.stem.porter import PorterStemmer

r_client = redis.Redis('localhost')
r_pipeline = r_client.pipeline()

def tokenize(text):
	preproc = re.sub(r"[^a-zA-Z\d\s]", " ", text)
	words = preproc.lower().split()
	return words

def stem(words):
	newwords=[]
	for word in words:
		newwords.append(PorterStemmer().stem_word(word))
	return newwords

def addToIndex(id, text):
    tokentext = tokenize(text)
    words = stem(tokentext)
    for word in words:
        r_pipeline.sadd(word, id)
    try:
        r_pipeline.execute()
        return
    except Exception as e:
        print "Error adding words to redis index with exception: ", e

def getFromIndex(text):
    try:
        intersection = r_client.sinter(stem(tokenize(text)))
        response = tuple(list(intersection))
        return response
    except Exception as e:
        print "Error retrieving intersection from redis db with exception: ", e
        return ()

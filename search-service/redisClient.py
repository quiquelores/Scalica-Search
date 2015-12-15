import redis
import re

r_client = redis.Redis('localhost')
r_pipeline = r_client.pipeline()

def tokenize(text):
	preproc = re.sub(r"[^a-zA-Z\d\s]", " ", text)
	words = preproc.lower().split()
	return words

def addToIndex(id, text):
    words = tokenize(text)
    for word in words:
        r_pipeline.sadd(word, id)
    r_pipeline.execute()

def getFromIndex(text):
    intersection = r_client.sinter(tokenize(text))
    response = tuple(list(intersection))
    return response

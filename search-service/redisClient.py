import redis

r_client = redis.Redis('localhost')
r_pipeline = r_client.pipeline()

def addToIndex(id, text):
    words = text.split()
    for word in words:
        r_pipeline.sadd(word, id)
    r_pipeline.execute()

def getFromIndex(text):
    intersection = r_client.sinter(text.split())
    response = tuple(list(intersection))
    return response

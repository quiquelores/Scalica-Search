import search_pb2
import sys

from grpc.beta import implementations

channel = implementations.insecure_channel('localhost', 50051)
stub = search_pb2.beta_create_Search_stub(channel)

def search(query):
    try:
        response  = stub.Search(search_pb2.SearchRequest(query=query), 100)
        return response.post_ids
    except Exception as e:
        print "Error calling search on RPC Server with exception: ", e
        return []

def index(id, text):
    try:
        stub.Index(search_pb2.IndexRequest(post_id=str(id), text=text), 100)
        return
    except Exception as e:
        print "Error calling index on RPC Server with exception: ", e

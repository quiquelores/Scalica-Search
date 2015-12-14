import search_pb2
import sys

from grpc.beta import implementations

channel = implementations.insecure_channel('localhost', 50051)
stub = search_pb2.beta_create_Search_stub(channel)

def search(query):
    response  = stub.Search(search_pb2.SearchRequest(query=query), 100)
    return response.post_ids

def index(id, text):
    stub.Index(search_pb2.IndexRequest(post_id=str(id), text=text), 100)

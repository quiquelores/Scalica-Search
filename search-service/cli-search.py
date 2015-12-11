import search_pb2
import sys

from grpc.beta import implementations

def run():

    channel = implementations.insecure_channel('localhost', 50051)
    stub = search_pb2.beta_create_Search_stub(channel)

    if(sys.argv[1] == "index"):
        response = stub.Index(search_pb2.IndexRequest(post_id=sys.argv[2], text=sys.argv[3]), 100)
        print response.status


    elif(sys.argv[1] == "search"):
        response  = stub.Search(search_pb2.SearchRequest(query=sys.argv[2]), 100)
        if(len(response.post_ids)>0):
            print response.post_ids[0]
        else:
            print "No results"

if __name__ == '__main__':
  run()

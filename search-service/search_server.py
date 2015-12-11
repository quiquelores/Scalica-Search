import search_pb2

import time
import random
import grpc
import indexer

from grpc.beta import implementations

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class SearchServicer(search_pb2.BetaSearchServicer):
    def Index(self, request, context):
        indexer.addToIndex(request.post_id, request.text)
        return search_pb2.IndexReply(status=1)

    def Search(self, request, context):
        response = indexer.getFromIndex(request.query)
        return search_pb2.SearchReply(post_ids=response)

def serve():
  server = search_pb2.beta_create_Search_server(SearchServicer())
  server.add_insecure_port('[::]:50051')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(1)

if __name__ == '__main__':
  serve()

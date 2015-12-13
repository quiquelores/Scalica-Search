# Will delete. Just needed to check if requests could be made

import time
import search_pb2
from random import randint
from grpc.beta import implementations

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class Search(search_pb2.BetaSearchServicer):

  def Index(self, request, context):

    return search_pb2.IndexReply(status=300)


  def Search(self, request, context):

    return search_pb2.SearchReply(post_ids=[555])



def serve():
  server = search_pb2.beta_create_Search_server(Search())
  server.add_insecure_port('[::]:50052')
  server.start()
  try:
    while True:
      time.sleep(_ONE_DAY_IN_SECONDS)
  except KeyboardInterrupt:
    server.stop(0)

if __name__ == '__main__':
  serve()
import search_pb2

import time
import grpc
import redisClient


from grpc.beta import implementations

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class SearchServicer(search_pb2.BetaSearchServicer):
    def Index(self, request, context):
        print("Indexing post:" + request.post_id)
        redisClient.addToIndex(request.post_id, request.text)
        return search_pb2.IndexReply(status=1)

    def Search(self, request, context):
        print("Searching for posts containing: " + request.query)
        response = redisClient.getFromIndex(request.query)
        return search_pb2.SearchReply(post_ids=response)

    #Sort by follower
    def SearchFollowers(self,request,context,group):
        print("Matching the followeres list for query: " + request.query)
        ids = []
        print 'getting %s ids' % group
        downloadCursor = -1;
        while downloadCursor != 0:
            data = (Post.objects.filter(id__in=post_ids).order_by('-pub_date')[0:10], { 'downloadCursor' : downloadCursor })

            print 'Data downloaded.Enter for next: %s (%s)' % (len(data['ids']), data['next_downloadCursor'])

            ids.extend(data['ids'])
            downloadCursor = data['next_downloadCursor']

        print 'Total length of data %s: %s' % (group, len(ids))

        #Getting follow list
        alreadyPresent = r.zrevrange(group, 0, -1)
        print '%s is already presnt: %s' % (group, len(alreadyPresent))
        print 'Validating Subtractions'
        unfollow_ids = []
        follow_ids = []

        for uid in alreadyPresent:
            if long(uid) in ids: continue

            # update array
            print 'Subtracted: %s' % uid
            unfollow_ids.append(uid)
            r.zrem(group, uid)

        # New entries addition
        print 'Finding whats added already'
        for uid in ids:
            if (r.zrank(group, uid) > 0):
                continue

            print 'Added: %s' % uid
            follow_ids.append(uid)
            r.zadd(group, time(), uid)

        #call match words for follow list
        if follow_ids:
            mathcWords(follow_ids)

        print '\n'.join(body)

    def matchWords(follow_ids):
        print "Mathing Words in post"
        for ids in idCrawler(follow_ids, 100):
            stringUserId = ','.join(map(str, ids))
            print stringUserId
            userData = (Post.objects.filter(id__in=post_ids).order_by('-pub_date')[0:10], { 'user_id' : stringUserId })
       
        for user in userData:
            if (user['post'] == userData:user['post'])
             print "Success for id " + stringUserId
            else
             print "Unsuccessfull for id " + stringUserId

def idCrawler(seq, size):
    return (seq[pos:pos + size] for pos in xrange(0, len(seq), size))

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

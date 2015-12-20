from .models import Post

def sort(posts, query):
    #sort based of adjancy of words
    posts = sorted(posts, key=lambda x: num_of_adjacent_words_from_query(x.text, query), reverse=True)
    #sort based on order of words
    posts = sorted(posts, key=lambda x: are_words_in_order_of_query(x.text, query), reverse=True)

    return posts

#HELPER FUNCTIONS

#returns the number of adjacent words in the post from the query
def num_of_adjacent_words_from_query(post, query):
    max_adjacent = 0
    post_array = post.split()
    query_array = query.split()

    index_query = 0
    index_post = 0

    while index_query<len(query_array):
        while index_post<len(post_array):
            curr = 0
            while index_query+curr<len(query_array) and index_post+curr<len(post_array) and query_array[index_query+curr]==post_array[index_post+curr]:
                curr += 1
            if(curr>max_adjacent):
                max_adjacent = curr
            index_post += 1
        index_query += 1
    return max_adjacent

#returns 1 if the words in the post are in the same order as the query
def are_words_in_order_of_query(post, query):
    post_array = post.split()
    query_array = query.split()
    q_i = 0
    p_i = 0
    i = 0
    j = 0

    while q_i < len(query_array):
        while query_array[q_i]!=post_array[p_i]:
            p_i+= 1
            if p_i == len(post_array):
                return 0;
        q_i+= 1
    return 1;

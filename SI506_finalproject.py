# import Python packages/modules
import requests
import json

# ========== Facebook ==========
## PART 1. DATA REQUEST
## a function to get data (posts on my wall) from the Facebook API
def request_my_facebook_data():
    # set up the access token
    # this new long-lived access token will expire on February 12th, 2018
    facebook_access_token = "EAAH5wRVZCn2EBAFt54m8CKxAGpBZCAu3zFOMwN8bOv3b8YmoISvZATdwaZBgLAklt0edThcy1ZBL0NoKQi3uJqcTM3UZCUO8QZBHAPH8GAhAh2ZBKim5LQ9NIhqdQMz8oojtrwjIfz59Xvvf0OWjxa34ICRZBERBzFIMZD"

    # set up the base URL
    base_url = 'https://graph.facebook.com/me/feed'

    # set up a dictionary of parameters
    params_diction = {}
    params_diction["access_token"] = facebook_access_token
    params_diction["limit"] = 50
    params_diction["fields"] = "message, link, name, comments, likes"

    # request data
    results = requests.get(url = base_url, params = params_diction)
    facebook_data_py = json.loads(results.text)

    return facebook_data_py

## PART 2. POST CLASS
class Post:
    def __init__(self, post_diction):
        # message
        if 'message' in post_diction:
            self.message = post_diction['message']
        else:
            self.message = ''

        # link
        if "link" in post_diction:
            self.link = post_diction['link']
        else:
            self.link = ''

        # title (the name of the link)
        if "name" in post_diction:
            self.title = post_diction['name']
        else:
            self.title = ''

        # comments
        if "comments" in post_diction:
            self.comments = post_diction['comments']['data']
        else:
            self.comments = []

        # likes
        if "likes" in post_diction:
            self.likes = post_diction['likes']['data']
        else:
            self.likes = []

    def __str__(self):
        return "* Message: {}\n* Link: {}\n* Title: {}\n* Comments: {}\n* Likes: {}\n".format(self.message, self.link, self.title, len(self.comments), len(self.likes))

    # a class method to examine a post and generate a list of words that are not stopwords
    def stopwords_remover(self):
        # a list of stopwords
        stopwords_lst = ["the", "a", "and", "is", "are", "that", "i", "my", "when", "which", "this", "of", "to", "will", "for", "you", "your", "from", "so", "it", "all", "she", "her", "he", "his", "we", "us", "our", "in", "me", "on", "must", "by", "have", "own", "out", "be"]

        message_content = self.message.lower().replace(".", "").replace(",", "").replace("?", "").replace("!", "").split()
        post_without_stopwords = []
        for word in message_content:
            if word not in stopwords_lst:
                post_without_stopwords.append(word)
        return post_without_stopwords

## STEP 3. FIND THE MOST COMMON WORD
## request the data from the Facebook API
my_facebook_posts = request_my_facebook_data()
## create two lists: one for the original posts, the other for the messages
posts_lst = []
modified_messages_lst = []
for message_diction in my_facebook_posts['data']:
    # create a Post instance
    inst = Post(message_diction)
    posts_lst.append(inst)
    # use the class method to remove the stopwords and then append the edited message to the list
    modified_messages_lst.append(inst.stopwords_remover())

## create a dictionary to count how many times each non-stopword word shows up
word_counts = {}
for message in modified_messages_lst:
    for word in message:
        if word not in word_counts:
            word_counts[word] = 0
        word_counts[word] += 1

most_common_word = ""
frequency_value = 0

## go through the dictionary (word_counts) and find the most common word
for word in word_counts:
    if word_counts[word] > frequency_value:
        frequency_value = word_counts[word]
        most_common_word = word

print("* REQUEST DATA FROM THE FACEBOOK API:")
print("The most common word among the latest 50 posts is: \n'{}'\n".format(most_common_word))


# ========== iTunes ==========
## PART 1. DATA REQUEST & CACHING
## set up a file for caching
itunes_cache_file = "SI506finalproject_cache.json"
try:
    cache_file = open(itunes_cache_file, 'r')
    cache_content = cache_file.read()
    CACHE_DICTION = json.loads(cache_content)
    cache_file.close()
except:
    CACHE_DICTION = {}

## a function to generate a unique id of a request
def unique_id_generator(base_url, params_diction):
    alphabetized_keys = sorted(params_diction.keys())
    lst = []
    for key in alphabetized_keys:
        lst.append("{}-{}".format(key, params_diction[key]))

    # combine the baseurl and the formatted pairs of keys and values
    unique_id = base_url + "_".join(lst)

    # return a unique id of the request
    return unique_id

## a function to get data from the iTunes API
def request_itunes_data(search_string, search_type = "song"):
    # set up the base URL
    base_url = "https://itunes.apple.com/search"

    # set up a dictionary of parameters
    params_diction = {}
    params_diction["format"] = "json"
    params_diction["term"] = search_string
    params_diction["entity"] = search_type

    # generate a unique id of this search
    unique_id = unique_id_generator(base_url, params_diction)

    # request/cache data
    if unique_id in CACHE_DICTION:
        print("Getting data from the cache file...")
        return(CACHE_DICTION[unique_id])
    else:
        print("Making new data request...")
        results = requests.get(url = base_url, params = params_diction)
        itunes_data_py = json.loads(results.text)
        CACHE_DICTION[unique_id] = itunes_data_py

        cache_file = open(itunes_cache_file,"w")
        cache_string = json.dumps(CACHE_DICTION)
        cache_file.write(cache_string)
        cache_file.close()

        return CACHE_DICTION[unique_id]

## PART 2. SONG CLASS
class Song:
    def __init__(self, song_diction):
        self.title = song_diction["trackName"]
        self.artist = song_diction["artistName"]
        self.album = song_diction["collectionName"]
        self.length = song_diction["trackTimeMillis"] # milliseconds

    # a class method to convert milliseconds to minutes and seconds
    # this class method will be used in the __str__ method
    def convert_track_time(self):
        track_time_min = int(self.length/1000/60)
        track_time_sec = int(self.length/1000 % 60)
        return "{} min {} sec".format(track_time_min, track_time_sec)

    def __str__(self):
        return "* Title: {}\n* Artist: {}\n* Album: {}\n* Length: {}\n".format(self.title, self.artist, self.album, self.convert_track_time())

## PART 3. SORTING
## request the data from the Facebook API
print("* REQUEST DATA FROM THE ITUNES API:")
search_itunes_songs = request_itunes_data(most_common_word)

## create a list to keep the search results
songs_lst = []
for song_diction in search_itunes_songs['results']:
    # create a Song instance
    inst = Song(song_diction)
    # append each Song instance to the list
    songs_lst.append(inst)

## sort the list by the song length (from longest to shortest)
print("Sorting the results by the song length...")
sorted_songs_lst = sorted(songs_lst, key = lambda x: x.length, reverse = True)

## PART 4. CREATE .CSV FILE
print("Creating a file...")
itunes_data_file = open("itunes_sorted_results.csv", "w")
itunes_data_file.write('Title, Artist, Album, Length\n')
for song in sorted_songs_lst:
    itunes_data_file.write("%s, %s, %s, %s\n" % ("".join(song.title.split(",")), "".join(song.artist.split(",")), "".join(song.album.split(",")), song.convert_track_time()))
itunes_data_file.close()
print("The file has been created successfully. Let's open the 'itunes_sorted_results.csv' file to see the sorted, and well-formatted results!")

# import Python packages/modules
import requests
import json

# ===== Facebook =====
# PART 1. DATA REQUEST
def request_facebook_data(page_link):
    facebook_access_token = "EAAH5wRVZCn2EBACR8Kf22u1FP9ZBaCo8085HhSWlasuRwllOZCuBvhDpK8h705eXhupZCxG3D9DkoGvt5sSYyZCwkZCJzZC8CTePH5gs1LJoyvkEc8HjHIFe1BOeO9GZCGvlLOgMVXKXNi75wQqH18oJSR9TRmGr4QkakqKZBdKQkPpVi1GgrwDTXTzmJnTrJXkMZD"

    params_diction = {}
    params_diction["access_token"] = facebook_access_token
    params_diction["limit"] = 1
    params_diction["fields"] = "name, message, link, comments"

    results = requests.get(url = page_link, params = params_diction)
    facebook_data_py = json.loads(results.text)

    return facebook_data_py

# ===== iTunes =====
# PART 1. DATA REQUEST & CACHING
# set up a file for caching
itunes_cache_file = "itunes_cache_data.csv"
try:
    cache_file = open(itunes_cache_file, 'r')
    cache_content = cache_file.read()
    CACHE_DICTION = json.loads(cache_content)
    cache_file.close()
except:
    CACHE_DICTION = {}

# a function to generate a unique id of a request
def unique_id_generator(base_url, params_diction):
    alphabetized_keys = sorted(params_diction.keys())
    lst = []
    for key in alphabetized_keys:
        lst.append("{}-{}".format(key, params_diction[key]))

    # combine the baseurl and the formatted pairs of keys and values
    unique_id = base_url + "_".join(lst)

    # return a unique id of the request
    return unique_id

# a function to get data from the iTunes API
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
        print("Making data request...")
        results = requests.get(url = base_url, params = params_diction)
        itunes_data_py = json.loads(results.text)
        CACHE_DICTION[unique_id] = itunes_data_py

        cache_file = open(itunes_cache_file,"w")
        cache_string = json.dumps(CACHE_DICTION)
        cache_file.write(cache_string)
        cache_file.close()

        return CACHE_DICTION[unique_id]

# PART 2. SONG CLASS
class Song:
    def __init__(self, song_diction):
        self.title = song_diction["trackName"]
        self.artist = song_diction["artistName"]
        self.album = song_diction["collectionName"]
        self.length = song_diction["trackTimeMillis"]

    def __str__(self):
        return "* Title: {}\n* Artist: {}\n* Album: {}\n* Length: {}\n".format(self.title, self.artist, self.album, self.length)




# ===== TESTING =====
# ===== iTunes =====
# itunes_test_data_1 = request_itunes_data("Adele")
# itunes_test_data_2 = request_itunes_data("Jack White")
# itunes_test_data_3 = request_itunes_data("Spiritualized")
#
# for diction in itunes_test_data_1['results']:
#     inst = Song(diction)
#     print(inst)

# ===== Facebook =====
# source_1 = 'https://graph.facebook.com/me/feed'
# source_2 = 'https://graph.facebook.com/nmemagazine/feed'
# facebook_test_data_1 = request_facebook_data(source_1)
# facebook_test_data_2 = request_facebook_data(source_2)
# print(facebook_test_data_1)
# print(facebook_test_data_2)

# import Python packages/modules
import requests
import json

# ===== iTunes =====

# PART 1. DATA REQUEST & CACHING
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

    # request data using the base URL and the params
    results = requests.get(url = base_url, params = params_diction).json()

    # return the result
    return results

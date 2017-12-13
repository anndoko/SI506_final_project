# import Python packages/modules
import requests
import json

# ===== iTunes =====

# Part 1. a function to get data from the iTunes API
def request_itunes_data(search_string, search_type = "song"):
    # set up the base URL
    base_url = "https://itunes.apple.com/search"

    # set up a dictionary of parameters
    url_params = {}
    url_params["format"] = "json"
    url_params["term"] = search_string
    url_params["entity"] = search_type

    # request data using the base URL and the params
    result_data = requests.get(url = base_url, params = url_params).json()

    # return the result
    return result_data

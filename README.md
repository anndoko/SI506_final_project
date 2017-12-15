SI 506 FINAL PROJECT README

* **What does this project do?**

  By requesting data from the Facebook API, the project will find the most common word among the last 50 posts on my Facebook wall. The project will then use that word as a search string to request data from the iTunes, and then it will sort the results by the song length and store the sorted results in a .cvs file.

* **What files are included in this project?**
  1. README.txt
  2. SI506_finalproject.py: this is a .py file that should be used to run the program
  3. SI506finalproject_cache.json: this is provided as a sample file that the program outputs
  4. itunes_sorted_results.csv: this is provided as a sample file that the program outputs

* **What Python modules are used in this project?**
  1. requests
  2. json

* **How to run the code?**

  Simply download the file "SI506_finalproject.py" and enter the command line "python3 SI506_finalproject.py" in your terminal to run the code.

* **REQUIREMENTS LIST:**
  * **Get and cache data from 2 REST APIs (list the lines where the functions to get & cache data begin and where they are invoked):**
    1. Get data from the Facebook API without caching data:

      1. Define a function for requesting data: *8*
      2. Get data by invoking the function: *78*

    2. Get and cache data from the iTunes API:

      1. Set up a file for caching: *113*
      2. Define a function for requesting and caching data: *136*
      3. Get and cache data by invoking the function: *187*

  * **Define at least 2 classes, each of which fulfill the listed requirements:**
    1. Define Post class: *29*
    2. Define Song class: *167*

  * **Create at least 1 instance of each class:**
    1. Create instances of Post: *84*
    2. Create instances of Song: *193*

  * **Invoke the methods of the classes on class instances:**
    1. Invoke the additional method "stopwords_remover" of the Post class: *87*
    2. Invoke the additional method "convert_track_time" of the Song class: *182* and *206*

  * **At least one sort with a key parameter:** *199*

  * **Define at least 2 functions outside a class (list the lines where function definitions begin):**
    1. def request_my_facebook_data(): *8*
    2. def unique_id_generator(base_url, params_diction): *123*
    3. def request_itunes_data(search_string, search_type = "song"): *136*

  * **Invocations of functions you define:**
    1. Invoke the function "request_my_facebook_data": *78*
    2. Invoke the function "unique_id_generator": *147*
    3. Invoke the function "request_itunes_data": *187*

  * **Create a readable file:** *203*

END REQUIREMENTS LIST

* **What happen as a result of the code?**
  1. The following strings will be printed in your terminal, showing you the most common word in the last 50 posts, the process of requesting/caching data from the iTunes API, and the process of creating the .cvs file:
      \n
      \* REQUEST DATA FROM THE FACEBOOK API:
      The most common word among the latest 50 posts is:
      'mom'
      \n
      \* REQUEST DATA FROM THE ITUNES API:      
      Getting data from the cache file...
      Sorting the results by the song length...
      Creating a file...
      The file has been created successfully. Let's open the 'itunes_sorted_results.csv' file to see the sorted, and well-formatted results!

  2. Two files will be created after you run the program:
      1. SI506finalproject_cache.json: this is a file that stores cached data
      SAMPLE:
      https://github.com/anndoko/SI506_final_project/blob/master/SI506finalproject_cache.json

      2. itunes_sorted_results.csv: this is a .cvs file that stores the sorted results
      SAMPLE:
      https://github.com/anndoko/SI506_final_project/blob/master/itunes_sorted_results.csv

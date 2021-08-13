# Shorten URL API

## Introduction

 The Shorten URL API is an API that takes an input of a long URL and it produces a short URL with a base URL (here -> https://abdullah.app). The shortened URLs as well as their corresponding original URLs are saved in a table in the database and the visits for the short URLs are saved in another table. The API also can redirect the user to the original long URL if you access it with the short URL. In this Readme file, I will explain the structure of the files I added and the part each component plays in the task. The python code I created is also commented.

## Files Structure

The files are saved into 3 locations, app folder, the test folder, and the root folder. 

- app
This folder contains api.py and db.py.
  - api.py
  api.py is concerned with configuring the API endpoints, its configurations and the structure of the requests and responses.
  - db.py
  db.py is concerned with defining the database connection. It included also functions to create the tables where the long URLs and short URLs are mapped (short_URLs table) and the table where visits are tracked (URL_visits table). It also include the function needed to insert the new shortened_URLs along with their corresponding long_URLs (short_URLtable_insert function). It also increments the visits in the visit table (increment_URL_visits function) and retreives the number of visits to a specific short URL. It has also functions to retrieve a saved shortened URL of a given long URL and vice versa (get_db_original_URL and get_db_shortened_url functions respectively). Finally "check_uniqueness" function to check whether a long or a short URL already exist in the shortURLs table or not

- test
This folder contains conftest.py and test_api.py
  - conftest.py
  Shared resources for tests
  - test_api.py
  This python file contains test to be performed to ensure that the API is working correctly
- root folder
  - database.sqlite
  The sqlite database
  - docker-compose.yml
  Contains the definitions for different services needed to run the API.
  - Dockerfile
  The dockerfile containing command to define the image.
  - Makefile
  This docker Makefile are used to compile parts of the code such as tests for testing the API, setup for setting up the dependencies and run for running the API.
  - poetry.*
  For installing the dependencies
  - README_Abdullah.md (this file)
  A file containing explanation of the code setup and function


## Assumptions:

1- A long URL cannot have more than one short URL (This can be easily changed).

2- The visits are calculated on the short URL, and since each long URL has only one corresponding short URL, it is the same. It can be also easily changed

3- I assumed the HTTP URL should contain "https://..." to be valid/well-formed.

4- I stored the short URLs without the "app.py" part or the "https://" in the table as they are not necessary, but the JSON responses contains them for better user experience.

5- For the redirection method where the user enters the short_URL, you don't need anything returned, but from the browser the user will be directed to the

designated long URL.


## How to run

1- Run `make setup` to initialize the envoirment and install dependencies.

2- Run `make run` to run the API. while the API is running, you can do one of two requests:

2.1- "POST" resquest, through Postman or curl, for ex. -> curl -X POST -v -d '{"long_url": "https://youtube.com"}' http://0.0.0.0:8080/api/shorten_url
This will retreive the long URL, short URL including https://abdullah.com and whether it was stored before or it is the first time. Additionally if you run this command for example more than one time, the output response of stored before will change to True.

2.2- "GET" request, through curl, or using the URL given through the browser, for ex. -> curl http://0.0.0.0:8080/visits/VKT85U . This will retreive the number of times the short URL "VKT85U" was visited as per the URL_visits table, if it doesn't exist it will output an error. You can invoke a visit to a short URL via curl http://0.0.0.0:8080/VKT85U or better via the browser! -> http://localhost:8080/VKT85U and it will redirect you to the corresponding URL, in our case youtube!, and will increment the number of visits to this short URL. Finally, get_health can be invoked via a "GET" request through curl or through the browser, for ex. http://0.0.0.0:8080/health. If the message dispalyed is "API is healthy", then the API is healthy.

3- Run `make test` to test the API. I added 6 tests to test some functions. Definitely more tests should be added but I ran out of the time I have for the task.

## Closure

The API was tested and "make run" runs the API sucessfully and the post requests inserts sucessfully to the table in the database, and the get requests retreives the number of visits sucessfully. "make test" invokes the tests and the tests passed sucesfully.

In case you encountered an error or a bug, or you have an idea to enhance the API, please report an issue!

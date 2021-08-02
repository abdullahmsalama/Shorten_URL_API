"""
This file includes the API requests and their configurations, along with
the configuration of the requests and responses.
"""

from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import random
import validators
import string
from fastapi.responses import RedirectResponse
from app.db import SessionLocal, get_db,\
 create_shortURL_table, create_URLvisits_table,\
 short_URLtable_insert, increment_URL_visits,\
 retreive_shortURL_visits, get_db_original_URL, get_db_shortened_url,\
 check_uniqueness

app = FastAPI()

@app.on_event("startup")
def startup():
    session = SessionLocal()
    session.execute("select 1")
    create_shortURL_table()
    create_URLvisits_table()
    session.close()


class ShortenRequest(BaseModel):
    long_url: str


class ShortenResponse(BaseModel):
    long_url: str
    short_url: str
    stored_before: bool


class CountResponse(BaseModel):
    short_url: str
    visits_count: int

@app.get("/health", response_model=str)
async def get_health():
    """
    check for API health
    """
    return "API is healthy"

def is_valid_url(url):
    if validators.url(url) == True:
        return True
    else:
        raise HTTPException(status_code=422, detail="Invalid URL format")
        

# In case of a post request, this function runs
@app.post("/api/shorten_url", response_model=ShortenResponse)
async def shorten_url(request_payload: ShortenRequest):
    is_valid_url(request_payload.long_url)
    # check if this long_url has been shortened before or not
    ## Can of course also be done through "ON CONFLICT"
    base_url = 'https://abdullah.app/'
    if check_uniqueness(url = request_payload.long_url, url_type = 'long_url'):
        # if not shortened before, shorten it
        while True:
            # keep producing shortened URLs until a unique shortened URL is produced
            generated_url = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            shortened_url = base_url + generated_url
            # stop if the produced shortened URL is unique
            if check_uniqueness(url = generated_url, url_type = 'short_url'):
                break
    # if it was shotened before, then return the shortened URL from the table and that it was
    #shortened and stored before
    else:
        return {'long_url': request_payload.long_url, \
        'short_url': base_url + get_db_shortened_url(long_url = request_payload.long_url),\
        'stored_before': True}

    # resume the stream of not shortened before, inserting the newly shortened URL to the table
    ## It is important to mention that there is no need to store the https://tier.app/, but only
    ### the additional short part
    short_URLtable_insert(long_url = request_payload.long_url, short_url = generated_url)

    # return the newly shortened URL and that it was not shortened before
    return {'long_url': request_payload.long_url, \
    'short_url': shortened_url,\
    'stored_before': False}


""" For redirection once we enter the short url, the original one has to be retreived
and one visit has to be added in the visits table """
@app.get("/{short_url}")
async def redirect_to_long_URL(
    short_url: str, sessions: Session = Depends(get_db)):
    # increment the visits
    increment_URL_visits(short_url = short_url)  
    # return the original long URL, he method "get_db_original_URL" is written in db.py
    long_url = get_db_original_URL(short_url)
    return RedirectResponse(url=long_url)


""" To get the number of visits to a certain shortened URL """
@app.get("/visits/{short_url}", response_model=CountResponse)
async def count_number_of_visits(
    short_url: str, sessions: Session = Depends(get_db)):

    # the method "retreive_shortURL_visits" is written in db.py
    return {'short_url': short_url,\
     'visits_count': int(retreive_shortURL_visits(short_url = short_url))}
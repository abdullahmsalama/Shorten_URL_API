""" This file is used for defining the database connection"""
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException


engine = create_engine("sqlite:///./database.sqlite", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# This function create the shortURL table (if not already exists)
def create_shortURL_table():
    session = SessionLocal()
    try:
        session.execute("""CREATE TABLE IF NOT EXISTS short_URLs (
                                        long_URL varchar(255),
                                        short_URL varchar(20),
                                        PRIMARY KEY (long_URL, short_URL)); """)
    except Exception as e:
        print(e)

    finally:
        session.close()


# This function create the URL visits table (if not already exists)
def create_URLvisits_table():
    session = SessionLocal()
    try:
        session.execute("""CREATE TABLE IF NOT EXISTS URL_visits (
                                        short_URL varchar(20),
                                        visits int,
                                        PRIMARY KEY (short_URL)); """)
    except Exception as e:
        print(e)

    finally:
        session.close()


""" This function inserts into the shortURL table based on the
long URL provided and its shortened URL, and also inserts into
the visits table"""
def short_URLtable_insert(long_url, short_url):
    try:
        engine.execute("""INSERT INTO "short_URLs"
               (long_URL, short_URL) VALUES (?,?)""",[long_url, short_url])     
    except Exception as e:
        print(e)
    try:
        engine.execute("""INSERT INTO "URL_visits"
               (short_URL,visits) VALUES (?,?)""",[short_url,0])     
    except Exception as e:
        print(e)

""" This function counts the enteries in the short_URLs table and 
the visits table that was stored before, this function is only created
to be used in testing """
def count_enteries_tables():
    try:
        query_shorturls = engine.execute("""SELECT count(*) as short_urls_count from short_URLs""")
        for query_result in query_shorturls:    
            short_urls_count = query_result['short_urls_count']
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,
         detail="""Item not found, The short_URLs table was not created yet""")

    try:
        query_visits = engine.execute("""SELECT count(*) as url_visits_count from URL_visits""")
        for query_result in query_visits:    
            visits_count = query_result['url_visits_count']
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,
         detail="""Item not found, The URL_visits table was not created yet""")

    return short_urls_count, visits_count

""" This function increments the number of user visits to a specific
short URL"""
def increment_URL_visits(short_url):
    try:
        engine.execute("""UPDATE URL_visits Set visits = visits + 1
            WHERE short_URL = '{}'""".format(short_url))
               #.format(id, prediction))        
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,
            detail="""short URL not found, so couldn't update visits""")
    
""" This function retreives the number of visits to a short URL """
def retreive_shortURL_visits(short_url):
    try:
        query = engine.execute("""SELECT visits from URL_visits
            WHERE short_URL = '{}'""".format(short_url))
        for query_result in query:    
            visits = query_result['visits']
        return visits
    except Exception as e:
        raise HTTPException(status_code=404,
            detail="""short URL not found, hence not visited""")


""" This function retreive the long_url of its corresponding short url """
def get_db_original_URL(short_url):
    try:
        query = engine.execute("""SELECT long_URL from short_URLs 
            WHERE short_URL = '{}'""".format(short_url))
        for query_result in query:    
            long_url = query_result['long_URL']
        return long_url
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404, detail="""Item not found,
            This short URL doesn't correspond to any long URL that has been shortened before""")


""" This function retreive the shortened_URL that was stored before """
def get_db_shortened_url(long_url):
    try:
        query = engine.execute("""SELECT short_URL from short_URLs 
            WHERE long_URL = '{}'""".format(long_url))
        for query_result in query:    
            short_url = query_result['short_URL']
        return short_url
    except Exception as e:
        print(e)
        raise HTTPException(status_code=404,
         detail="""Item not found, This URL has not been shortened before""")


""" This function checks whether a url (log or short), is unique or not 
(saved in the table or not) """
def check_uniqueness(url, url_type):
    if url_type == "long_url":
        try:
            query = engine.execute("""SELECT count(long_URL) as url_count from short_URLs 
            WHERE long_URL = '{}'""".format(url))
            for query_result in query:    
                url_count = query_result['url_count']
            if url_count == 0:
                return True
            elif url_count == 1:
                return False
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="LONG URL INPUT ERROR")
    elif url_type == "short_url":
        try:
            query = engine.execute("""SELECT count(short_URL) as url_count from short_URLs 
            WHERE short_URL = '{}'""".format(url))
            for query_result in query:    
                url_count = query_result['url_count']
            if url_count == 0:
                return True
            elif url_count == 1:
                return False
        except Exception as e:
            print(e)
            raise HTTPException(status_code=404, detail="SHORT URL INPUT ERROR")

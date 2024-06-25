# LOC Authority Tools
A common issue with matching works from different sources / publishers is the integrity of the data. An author name
from one source may come in as 'Toni Morrison', while another has 'Morrison, Toni', or 'Morrison, Toni, 1931-2019',
or a myriad of other inputs. The goal of this project is to provide a simple proof of concept service to make resolving such
discrepancies easier. The final product of this is a webservice that lets you query by an author name that you have and returns
a set of potential matching 'established' names. The 'established' part of this is based on the Library of Congress [Name
Authority](https://id.loc.gov/authorities/names.html).

The general idea is as follows:

  1. Download the aforementioned named authority file
  2. Ingest each record from the file into a PostgreSQL DB
  3. Tokenize each name into a set of tokens representing (theoretically) each semantic part of the name
  4. Provide a webservice that uses these tokens as a quick filter before using fuzzy matching to provide a set of potentially
     matching names

Note, this is very much a proof-of-concept, and not a production-ready app. There are a number of obvious bugs here, and this
app misses out on some very basic things like connection pooling.  There is also some further learning to do in terms of
processing these authority files from the Library of Congress, and this is simply a first stab at that.

## Getting Started
This whole thing is a set of Python scripts and a very simple local webserver all running Python and managed by poetry.

### Setup / Installation


  1. Install poetry: https://python-poetry.org/docs/#installation
  2. Run `poetry install` to install dependencies.
  3. Run `docker compose up` to spin up the local database
  4. Run `poetry run python loc_authority_tools/seed_db.py` to create the DB tables
  5. Run `poetry run python loc_authority_tools/full_download.py` to download and unzip the LOC authority file
  6. Run `poetry run python loc_authority_tools/ingest_loc_names.py` to ingest the file into a local DB
  7. Run `poetry run python loc_authority_tools/tokenize_names.py` to ingest all author names and tokenize them
     for author matching
       - Note, this will take a long time (around 10 hours). A TODO is to add a `limit` param to the script
         OR to provide a dump of the data in S3
  8. Run `poetry run flask --app loc_authority_tools.app:app run` to start the webserver

## Endpoints

### GET '/authors-match?author={query}'
Returns a list of LOC author names potentially matching the search term, with confidence numbers

Example: `GET http://localhost:5000/author-match?author=morrison,toni`
```json
{
  "data": {
    "match": [
      {
        "confidence": 99,
        "label": "Morrison, Toni",
        "loc_url": "http://id.loc.gov/authorities/names/n80131379",
        "uuid": "0537a214-4050-4185-a206-12bb7edac0fb"
      },
      {
        "confidence": 92,
        "label": "Morrison, Voni",
        "loc_url": "http://id.loc.gov/authorities/names/no2018084424",
        "uuid": "361b2258-012d-4ead-b434-f98576ff7700"
      },
      {
        "confidence": 92,
        "label": "Morrison, Tony",
        "loc_url": "http://id.loc.gov/authorities/names/n79055204",
        "uuid": "8ea7df62-4ee9-4a9a-93b7-03139b8b15d6"
      },
      {
        "confidence": 88,
        "label": "Morrison, Tom",
        "loc_url": "http://id.loc.gov/authorities/names/n90716160",
        "uuid": "69a3d747-ef47-445e-b66f-120cb1cfe739"
      },
      {
        "confidence": 88,
        "label": "Morrison, Tim",
        "loc_url": "http://id.loc.gov/authorities/names/nb2010019150",
        "uuid": "b31d2dd5-7fbd-450d-8516-37d96b7bf33f"
      },
      {
        "confidence": 87,
        "label": "Morrison, T.",
        "loc_url": "http://id.loc.gov/authorities/names/n79025611",
        "uuid": "e5b2253f-6b7e-4cbf-a9f3-071dc836905f"
      }
    ]
  }
}
```
Note, there are duplicates here omitted for brevity, but that is a TODO to fix. There is also definitely some tuning required
for the fuzzy matching.


### GET '/authors/{uuid}'
Returns the corresponding author
```json
{
  "data": {
    "author": {
      "authoritative_label": "Morrison, Toni",
      "loc_url": "http://id.loc.gov/authorities/names/n80131379",
      "record_source": "84912d62-b264-4bf8-aaa9-7239c3b3be7b",
      "uuid": "0537a214-4050-4185-a206-12bb7edac0fb"
    }
  }
}
```

# LOC Authority Tools
A common issue with matching works from different sources / publishers is the integrity of the data. An author name
from one source may come in as 'Toni Morrison', while another has 'Morisson, Toni', or 'Morrison, Toni, 1931-2019',
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

# Getting Started
This whole thing is a set of Python scripts and a very simple local webserver all running Python and managed by poetry.

## Setup / Installation


  1. Install poetry: https://python-poetry.org/docs/#installation
  2. Run `poetry install` to install dependencies.
  3. Run `docker compose up` to spin up the local database
  4. Run `poetry run python loc_authority_tools/seed_db.py` to create the DB tables
  5. Run `poetry run python loc_authority_tools/full_download.py` to download and unzip the LOC authority file
  6. Run `poetry run python loc_authority_tools/tokenize_names.py` to ingest all author names and tokenize them
     for author matching
       - Note, this will take a long time (around 10 hours). A TODO is to add a `limit` param to the script
         OR to provide a dump of the data in S3
  7. Run `poetry run flask --app loc_authority_tools.app:app run` to start the webserver

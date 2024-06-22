import gzip
import io
import urllib.request


def main():
    print("Downloading authority file...")
    with urllib.request.urlopen("http://id.loc.gov/download/authorities/names.madsrdf.jsonld.gz") as zipfile_response:
        with gzip.GzipFile(fileobj=zipfile_response) as gzip_file:
            print("Unzipping authority file...")
            file_content = gzip_file.read()

    print("Writing unzipped file...")
    with open("names.madsrdf.jsonld", "wb") as f:
        f.write(file_content)


if __name__ == "__main__":
    main()

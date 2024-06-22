import dataclasses
import hashlib
import json

import psycopg


def main():
    print("Opening file and starting DB session...")
    with (
        open("names.madsrdf.jsonld", "r") as f,
        psycopg.connect("postgresql://postgres:postgres@localhost:5434/loc_authority_tools") as conn,
    ):
        print("Let's go")
        for line in f:
            try:
                print("Parsing person")
                person = parse_person(line)
                print("Hashing record")
                record_hash = hash_item(line)
            except Exception as e:
                print(f"Invalid line {str(e)}")
                continue

            try:
                record_uuid = conn.execute("""
                    INSERT INTO loc_authority_tools.mads_authority_record (record_hash, record)
                    VALUES (%s, %s)
                    RETURNING uuid
                    """,
                    (record_hash, line),
                ).fetchone()[0]

                conn.execute("""
                    INSERT INTO loc_authority_tools.loc_person_authority (record_source, loc_url, authoritative_label)
                    VALUES (%s, %s, %s)
                    """,
                    (record_uuid, person.loc_url, person.authoritative_label),
                )
            except Exception as e:
                print(f"Exception when writing to DB: {str(e)}")
                conn.rollback()
            else:
                conn.commit()
                print("Successfully wrote to DB")


@dataclasses.dataclass
class LOCPerson:
    loc_url: str
    authoritative_label: str


def parse_person(json_ld_item: str) -> LOCPerson:
    parsed = json.loads(json_ld_item)
    for item in parsed["@graph"]:
        type_ = item["@type"]
        if type_[0] != "madsrdf:Authority" or type_[1] != "madsrdf:PersonalName":
            continue

        if not item["@id"].startswith("http://id.loc.gov/authorities"):
            # Probably a better way to do this
            continue

        return LOCPerson(
            loc_url=item["@id"],
            authoritative_label=item["madsrdf:authoritativeLabel"],
        )

    raise ValueError()


def hash_item(json_ld_item: str) -> str:
    h = hashlib.sha3_512()
    h.update(json_ld_item.encode())
    return h.hexdigest()


if __name__ == "__main__":
    main()

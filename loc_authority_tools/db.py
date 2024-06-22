import typing

import psycopg


def conn():
    # TODO: environment variables
    return psycopg.connect("postgresql://postgres:postgres@localhost:5434/loc_authority_tools")


def fetch_all_authorities(conn, batch_size: int) -> typing.Iterator[tuple[str, str]]:
    with conn.cursor(name="name_cursor", withhold=True) as cursor:
        cursor.execute(
            """
            SELECT uuid, authoritative_label
            FROM loc_authority_tools.loc_person_authority
            """,
        )
        while True:
            rows = cursor.fetchmany(batch_size)
            if not rows:
                break
            yield from rows

        return
        yield

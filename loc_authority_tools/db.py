import typing

import psycopg
import psycopg.sql as sql


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


def save_authority_tokens(conn, authority_uuid: str, tokens: list[str]) -> None:
    placeholders = sql.SQL(', ').join(sql.Placeholder() * 2)
    query = sql.SQL(
        """
        INSERT INTO loc_authority_tools.loc_person_authority_label_token (authority_uuid, token)
        VALUES ({placeholders})
        ON CONFLICT (authority_uuid, token) DO NOTHING;
        """,
    ).format(placeholders=placeholders)
    with conn.cursor() as cursor:
        cursor.executemany(query, [(authority_uuid, token) for token in tokens])

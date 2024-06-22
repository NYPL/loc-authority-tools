import flask
import thefuzz.fuzz
import thefuzz.process

import loc_authority_tools.db as db
import loc_authority_tools.tokenizer as tokenizer


app = flask.Flask(__name__)


@app.route("/author-match", methods=['GET'])
def author_match():
    author_to_match = flask.request.args.get("author")
    if not author:
        return (400, {"error": {"msg": "Must supply author parameter"}})

    best_match = find_match(author_to_match)
    if not best_match:
        return {"data": {"msg": "No matching author found"}}

    return {"data": {"match": best_match}}


def find_match(name: str) -> str | None:
    name_tokens = tokenizer.tokenize_name(name)
    with db.conn() as conn:
        choices = conn.execute(
            """
            SELECT p.authoritative_label, ARRAY_AGG(t.token) AS tokens
            FROM loc_authority_tools.loc_person_authority_label_token AS t
            JOIN loc_authority_tools.loc_person_authority AS p
            ON t.authority_uuid = p.uuid
            WHERE
              t.token IN (%s)
            GROUP BY 1
            """,
            name_tokens,
        ).fetchall()

    name_tokens = set(name_tokens)
    choices = []
    for loc_name, loc_tokens in choices:
        if loc_name == name:
            return loc_name
        loc_tokens = set(loc_tokens)
        if loc_tokens == name_tokens:
            return loc_name

        choices.append(loc_name)

    if not choices:
        return None
    results = thefuzz.process.extract(name, choices, scorer=thefuzz.fuzz.token_sort_ratio)
    return sorted(results, key=lambda tup: tup[1], reverse=True)[0]

import flask
import thefuzz.fuzz
import thefuzz.process

import loc_authority_tools.db as db
import loc_authority_tools.tokenizer as tokenizer
import loc_authority_tools.works_lookup as works_lookup


app = flask.Flask(__name__)


@app.route("/authors/<uuid>", methods=['GET'])
def get_author(uuid: str):
    with db.conn() as conn:
        try:
            author = db.get_authority_by_uuid(conn, uuid)
        except ValueError:
            return (404, {"data": {"error": {"msg": "Not Found"}}})

    return {"data": {"author": author.json()}}


@app.route("/authors/<uuid>/title-match", methods=['GET'])
def match_title_for_author(uuid: str):
    title_to_match = flask.request.args.get("title")
    if not title_to_match:
        return (400, {"error": {"msg": "Must supply title parameter"}})
    with db.conn() as conn:
        try:
            author = db.get_authority_by_uuid(conn, uuid)
        except ValueError:
            return (404, {"data": {"error": {"msg": "Not Found"}}})

    session = works_lookup.new_session()
    contributed_works = works_lookup.fetch_works_contributed_to(session, author.loc_url)
    title_choices = {
        works_lookup.fetch_work_bibframe_title(session, work.uri)
        for work in contributed_works
    }
    if None in title_choices:
        title_choices.remove(None)

    if title_to_match in title_choices:
        return {"data": {"match": [_title_match(title_to_match, 100)]}}

    match_results = thefuzz.process.extract(title_to_match, title_choices, scorer=thefuzz.fuzz.token_sort_ratio)
    results = []
    for match_name, score in match_results:
        if score < 75:
            continue
        results.append(_title_match(match_name, score))

    return {"data": {"match": results}}


def _title_match(title: str, confidence: int) -> dict:
    return {
        "title": title,
        "confidence": confidence,
    }


@app.route("/author-match", methods=['GET'])
def author_match():
    author_to_match = flask.request.args.get("author")
    if not author_to_match:
        return (400, {"error": {"msg": "Must supply author parameter"}})

    matches = find_match(author_to_match)

    return {"data": {"match": matches}}


def find_match(name: str) -> list[dict]:
    name_tokens = tokenizer.tokenize_name(name)
    with db.conn() as conn:
        choices = db.match_authorities_by_tokens(conn, name_tokens)

    name_tokens = set(name_tokens)
    exact = []
    fuzzy_candidates = []
    for authority, loc_tokens in choices:
        if authority.authoritative_label == name:
            exact.append(_match(authority, 100))
        else:
            fuzzy_candidates.append(authority)

    fuzzy_matches = []
    if fuzzy_candidates:
        fuzzy_matches = do_fuzzy_match(name, fuzzy_candidates)

    # TODO: Figure out why we have duplicates
    return [*exact, *fuzzy_matches]


def do_fuzzy_match(name: str, authorities: list[db.LOCPersonAuthority]) -> list[dict]:
    authorities_by_label = {}
    choices = []
    for a in authorities:
        authorities_by_label[a.authoritative_label] = a
        choices.append(a.authoritative_label)

    match_results = thefuzz.process.extract(name, choices, scorer=thefuzz.fuzz.token_sort_ratio)
    results = []
    for match_name, score in match_results:
        if score < 75:
            continue
        results.append(_match(authorities_by_label[match_name], score))

    return results


def _match(authority: db.LOCPersonAuthority, confidence: int) -> dict:
    return {
        "uuid": authority.uuid,
        "label": authority.authoritative_label,
        "loc_url": authority.loc_url,
        "confidence": confidence,
    }

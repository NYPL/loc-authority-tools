import flask
import thefuzz.fuzz
import thefuzz.process

import loc_authority_tools.db as db
import loc_authority_tools.tokenizer as tokenizer


app = flask.Flask(__name__)


@app.route("/author-match", methods=['GET'])
def author_match():
    author_to_match = flask.request.args.get("author")
    if not author_to_match:
        return (400, {"error": {"msg": "Must supply author parameter"}})

    best_match = find_match(author_to_match)
    if not best_match:
        return {"data": {"msg": "No matching author found"}}

    return {"data": {"match": best_match}}


def find_match(name: str) -> str | None:
    name_tokens = tokenizer.tokenize_name(name)
    with db.conn() as conn:
        choices = db.match_authorities_by_tokens(conn, name_tokens)

    name_tokens = set(name_tokens)
    exact = []
    fuzzy_candidates = []
    for authority, loc_tokens in choices:
        loc_tokens = set(loc_tokens)
        if authority.authoritative_label == name:
            exact.append(_match(authority, 100))
        elif loc_tokens == name_tokens and len(loc_tokens) > 1:
            exact.append(_match(authority, 99))
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

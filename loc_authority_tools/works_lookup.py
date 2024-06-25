import dataclasses

import requests


def new_session() -> requests.Session:
    return requests.Session()


@dataclasses.dataclass
class ContributedWork:
    uri: str
    label: str


def fetch_works_contributed_to(session: requests.Session, contributor_url: str) -> list[ContributedWork]:
    response = session.get(
        "https://id.loc.gov/resources/works/relationships/contributorto",
        params={"label": contributor_url},
    )
    response.raise_for_status()
    return [ContributedWork(**item) for item in response.json()["results"]]


def fetch_work_bibframe_title(session: requests.Session, work_uri: str) -> str | None:
    response = session.get(f"{work_uri}.bibframe.json")
    response.raise_for_status()
    title_entry = next(
        (
            item for item in response.json()
            if "http://id.loc.gov/ontologies/bibframe/Title" in item.get("@type", [])
        ),
        None,
    )
    if not title_entry:
        return None

    return next(
        (
            title_item["@value"]
            for title_item
            in title_entry.get("http://id.loc.gov/ontologies/bibframe/mainTitle", [])
        ),
        None,
    )

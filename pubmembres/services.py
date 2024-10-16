import requests

BASE_URL = "https://orcid.org/"
BASE_PUBLIC_API_URL = "https://pub.orcid.org/v3.0/"


def get_access_token(client_id, client_secret):
    response = requests.post(
        f"{BASE_URL}oauth/token",
        data={
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "client_credentials",
            "scope": "/read-public",
            "redirect_uri": "https://crdm.ulaval.ca",
        },
        headers={"Accept": "application/json"},
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to get access token, error code was {response.status_code}"
        )

    return response.json()["access_token"]


def get_orcid_name(orcid_id, access_token):
    response = requests.get(
        f"{BASE_PUBLIC_API_URL}{orcid_id}/person",
        headers={
            "Accept": "application/orcid+json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to get ORCID name, error code was {response.status_code}"
        )

    return (
        response.json()["name"]["given-names"]["value"]
        + " "
        + response.json()["name"]["family-name"]["value"]
    )


def get_orcid_works(orcid_id, access_token):
    response = requests.get(
        f"{BASE_PUBLIC_API_URL}{orcid_id}/works",
        headers={
            "Accept": "application/orcid+json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to get ORCID works, error code was {response.status_code}"
        )

    result = []
    for work in response.json()["group"]:
        try:
            result.append(
                {
                    "put_code": work["work-summary"][0]["put-code"],
                    "year": work["work-summary"][0]["publication-date"]["year"][
                        "value"
                    ],
                }
            )
        except TypeError:
            pass

    return result


def _extract_raw_work_data(put_code, orcid_id, access_token):
    response = requests.get(
        f"{BASE_PUBLIC_API_URL}{orcid_id}/work/{put_code}",
        headers={
            "Accept": "application/orcid+json",
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code != 200:
        raise Exception(
            f"Failed to get ORCID work, error code was {response.status_code}"
        )

    return response


def extract_work_data(put_code, orcid_id, access_token):

    response = _extract_raw_work_data(put_code, orcid_id, access_token)

    contributors = []
    try:
        for contributor in response.json()["contributors"]["contributor"]:
            contributors.append(contributor["credit-name"]["value"])

    except TypeError:
        pass

    try:
        url = response.json()["url"]["value"]
    except TypeError:
        url = ""

    try:
        journal = response.json()["journal-title"]["value"]
    except TypeError:
        journal = ""

    result = {
        "title": response.json()["title"]["title"]["value"],
        "type": response.json()["type"],
        "publication_date": response.json()["publication-date"]["year"]["value"],
        "contributors": contributors,
        "url": url,
        "journal": journal,
    }

    return result


def simplify_orcid_txt():
    with open("orcids.txt", "r") as file:
        orcids = []
        for line in file:
            if line.strip() in orcids:
                continue
            orcids.append(line.strip())

    with open("orcids.txt", "w") as file:
        for orcid in orcids:
            file.write(orcid + "\n")

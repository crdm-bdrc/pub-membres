import requests
import os
from pubmembres import services
from dotenv import load_dotenv
import csv

load_dotenv()

ORCID_CLIENT_ID = os.getenv("ORCID_CLIENT_ID")
ORCID_CLIENT_SECRET = os.getenv("ORCID_CLIENT_SECRET")

YEARS = ["2021", "2022", "2023"]

records_api_url = "https://zenodo.org/api/records"

orcids = []
with open("orcids.txt", "r") as file:
    for line in file:
        orcids.append(line.strip())


with open("zenodo_output.csv", mode="w") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "ORCID",
            "Name",
            "Title",
            "Doi",
            "Publication Date",
            "Contributors",
            "Type",
            "Journal",
        ]
    )
    access_token = services.get_access_token(ORCID_CLIENT_ID, ORCID_CLIENT_SECRET)
    for orcid_id in orcids:
        name = services.get_orcid_name(orcid_id, access_token)
        print(
            "fetching works for",
            orcid_id,
            name,
        )

        search_query = f"creators.orcid:{orcid_id}"
        res = requests.get(
            records_api_url, params={"q": search_query, "size": 100, "page": 1}
        )
        print(res.status_code)

        data = res.json()
        results = data["hits"]["hits"]
        cleaned_results = []

        result_count = 0
        for result in results:

            title = result["metadata"]["title"]
            doi = result["metadata"]["doi"]
            publication_date = result["metadata"]["publication_date"]
            if publication_date[:4] not in YEARS:
                continue

            creators = ", ".join(
                [creator["name"] for creator in result["metadata"]["creators"]]
            )
            resource_type = result["metadata"]["resource_type"]["type"]
            meeting = result["metadata"].get("meeting", {}).get("title", "")
            result_count += 1
            writer.writerow(
                [
                    orcid_id,
                    name,
                    title,
                    doi,
                    publication_date,
                    creators,
                    resource_type,
                    meeting,
                ]
            )
        print(result_count)


with open("zenodo_records_raw.json", "w") as f:
    f.write(res.text)

import requests
import os
from pubmembres import services
from dotenv import load_dotenv
import csv
from bs4 import BeautifulSoup

load_dotenv()

ORCID_CLIENT_ID = os.getenv("ORCID_CLIENT_ID")
ORCID_CLIENT_SECRET = os.getenv("ORCID_CLIENT_SECRET")

YEARS = ["2021", "2022", "2023"]

arxiv_api_url = "http://export.arxiv.org/api/query?"

orcids = []
with open("orcids.txt", "r") as file:
    for line in file:
        orcids.append(line.strip())


with open("arxiv_output.csv", mode="w") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "ORCID",
            "Name",
            "Title",
            "Arxiv ID",
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
        res = requests.get(
            arxiv_api_url,
            params={
                "search_query": f'"{name}"',
                "searchtype": "author",
                "max_results": 100,
            },
        )
        print(res.status_code)

        data = res.text
        soup = BeautifulSoup(data, "html.parser")

        # get entry.find("arxiv:doi"), store .text if it is not null

        # results = []
        result_count = 0
        for entry in soup.find_all("entry"):
            result_count += 1
            result = {}
            title = entry.find("title").text
            arxiv_id = entry.find("id").text
            doi = entry.find("arxiv:doi").text if entry.find("arxiv:doi") else None
            publication_date = entry.find("published").text
            creators = [{"name": creator.text} for creator in entry.find_all("author")]
            resource_type = (
                {"type": entry.find("arxiv:primary_category")["term"]}
                if entry.find("arxiv:primary_category")
                else None
            )
            journal = (
                {"title": entry.find("arxiv:journal_ref").text}
                if entry.find("arxiv:journal_ref")
                else None
            )
            # results.append(result)

            writer.writerow(
                [
                    orcid_id,
                    name,
                    title,
                    arxiv_id,
                    doi,
                    publication_date,
                    creators,
                    resource_type,
                    journal,
                ]
            )
        print(result_count)


with open("arxiv_records_raw.json", "w") as f:
    f.write(res.text)

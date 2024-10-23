import os
from pubmembres import services
from dotenv import load_dotenv
import csv

load_dotenv()

ORCID_CLIENT_ID = os.getenv("ORCID_CLIENT_ID")
ORCID_CLIENT_SECRET = os.getenv("ORCID_CLIENT_SECRET")

YEARS = ["2021", "2022", "2023"]


orcids = []
with open("orcids.txt", "r") as file:
    for line in file:
        orcids.append(line.strip())


with open("output.csv", mode="w") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "ORCID",
            "Name",
            "Title",
            "Type",
            "Publication Date",
            "Contributors",
            "URL",
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
        works = services.get_orcid_works(orcid_id, access_token)
        work_count = 0
        out_of_range_work_count = 0
        for work in works:
            if work["year"] in YEARS:
                work_count += 1
                work_data = services.extract_work_data(
                    work["put_code"], orcid_id, access_token
                )
                if work_data["contributors"] is not None:
                    work_data["contributors"] = ", ".join(work_data["contributors"])
                writer.writerow(
                    [
                        orcid_id,
                        name,
                        work_data["title"],
                        work_data["type"],
                        work_data["publication_date"],
                        work_data["contributors"],
                        work_data["url"],
                        work_data["journal"],
                    ]
                )
            else:
                out_of_range_work_count += 1
        print("work count", work_count)
        print("out of range work count", out_of_range_work_count)

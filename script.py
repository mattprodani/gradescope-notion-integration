from notion.notion import NotionConnector
from gradescope.scope import GSConnector
import os
import json

def main():
    get_var = lambda x: os.environ.get(x)
    if os.getenv("NOTION_API_KEY") is None:
        secrets = json.load(open("secrets.json"))
        get_var = lambda x: secrets[x]
    API_KEY = get_var("NOTION_API_KEY")
    DB_ID = get_var("NOTION_DB_ID")
    GS_EMAIL = get_var("GS_EMAIL")
    GS_PASSWORD = get_var("GS_PASSWORD")

    if API_KEY is None or DB_ID is None or GS_EMAIL is None or GS_PASSWORD is None:
        raise ValueError(str(["Missing environment variable: \n" + x for x in ["NOTION_API_KEY", "NOTION_DB_ID", "GS_EMAIL", "GS_PASSWORD"] if get_var(x) is None]))

    notion = NotionConnector(API_KEY, DB_ID)
    print("Successfully connected to Notion")

    notion.update_schema()

    gs = GSConnector(GS_EMAIL, GS_PASSWORD)
    print("Successfully connected to Gradescope")

    assignments = gs.get_all_assignments()
    print(f"Successfully retrieved {len(assignments)} assignments from Gradescope")

    

    for assignment in assignments:
        if assignment.aid == "0000000": print(f"No AID, skipping {assignment}"); continue
        request = notion.add_assignment(assignment)
        if request == 100: continue
        elif request.status_code == 200:
            print(f"Successfully added assignment {assignment.name}")
        else:
            print(f"Failed to add assignment {assignment.name}")
            print(request.text)

if __name__ == "__main__":
    main()
    




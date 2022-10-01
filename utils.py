import json
import requests



def create_row_obj(assignment):
    return {
        "Assignment": _title_obj(assignment["name"]),
        "Course": _RTO(assignment["course"]),
        "Status": _RTO(assignment["status"]),
        "Open Date": _RTO(assignment["open_date"]),
        "Due Date": _RTO(assignment["close_date"]),
        "Points Earned": _RTO(assignment["points"][0]),
        "Total Points": _RTO(assignment["points"][1])
    }

def create_update_request(api_key, db_id, assignment):

    url = "https://api.notion.com/v1/pages/"

    body = json.dumps({"parent": {"database_id": db_id}, "properties": create_row_obj(assignment)})
    headers = {
    'Content-Type': 'application/json',
    'Notion-Version': '2022-02-22',
    'Authorization': f'Bearer {api_key}'
    }

    return requests.request("POST", url, headers=headers, data=body)



def _title_obj(x):
    return {"title":[{"text":{"content":str(x)}}]}

def _RTO(x):
    return {"rich_text":[{"text":{"content":str(x)}}]}
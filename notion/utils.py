import json
import requests
from datetime import datetime 

class Queries:
    def __init__(self):
        self.update_schema = json.loads(open("schema.json", "r").read())

    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __iter__(self):
        return iter(self.__dict__)

        
class Endpoints:
    def __init__(self):
        self.pages = "https://api.notion.com/v1/pages/"
        self.databases = "https://api.notion.com/v1/databases/"
        self.search = "https://api.notion.com/v1/search/"
        self.users = "https://api.notion.com/v1/users/"
        self.blocks = "https://api.notion.com/v1/blocks/"
    
    def __str__(self):
        return "Endpoints"
    
    def __repr__(self):
        return "Endpoints"
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __iter__(self):
        return iter(self.__dict__)



def compare_to_props(assignment, props):
    """ Compares assignment to properties of a notion row """
    # returns key of first mismatched property
    for key, val in props.items():
        if key == "ID": continue
        if key == "Assignment" and val != assignment["name"]: return key
        elif key == "Course" and val != assignment["course"]: return key
        elif key == "Status" and val != assignment["status"]: return key
        elif key == "Open Date" and datetime.fromisoformat(val) != assignment["open_date"]: 
            print("Open Date mismatch")
            print(datetime.fromisoformat(val))
            print(assignment["open_date"])
            return key
        elif key == "Due Date" and datetime.fromisoformat(val) != assignment["close_date"]: return key
        elif key == "Points Earned" and val != assignment["points"][0]: return key
        elif key == "Total Points" and val != assignment["points"][1]: return key
    return True

def process_db_qry(data):
    """ Processes data from notion database query """

    ALL_PROPS = ["Assignment", "Course", "Status", "Open Date", "Due Date", "Points Earned", "Total Points", "ID"]
    next_cursor = data["next_cursor"]
    results = data["results"]
    processed = {}
    for result in results:
        row = {}
        row["page_id"] = result["id"]
        properties = result["properties"]
        new_props = {}
        for key, val in properties.items():
            if key not in ALL_PROPS: continue
            new_props[key] = property_to_dict(val)
        row["properties"] = new_props
        processed[new_props["ID"]] = row
    return processed, next_cursor
    

def property_to_dict(prop):
    if "title" in prop:
        return prop["title"][0]["text"]["content"]
    elif "rich_text" in prop:
        return prop["rich_text"][0]["text"]["content"]
    elif "number" in prop:
        return prop["number"]
    elif "date" in prop:
        return prop["date"]["start"]


def create_row_obj(assignment):
    return {
        "Assignment": _title_obj(assignment["name"]),
        "Course": _RTO(assignment["course"]),
        "Status": _RTO(assignment["status"]),
        "Open Date": _date_obj(assignment["open_date"]),
        "Due Date": _date_obj(assignment["close_date"]),
        "Points Earned": _num_obj(assignment["points"][0]),
        "Total Points": _num_obj(assignment["points"][1]),
        "ID": _RTO(assignment["aid"])
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

def _num_obj(x):
    return {"number": x}

def _date_obj(x):
    return {"date": {"start": x.isoformat()}}

def _title_obj(x):
    return {"title":[{"text":{"content":str(x)}}]}

def _RTO(x):
    return {"rich_text":[{"text":{"content":str(x)}}]}
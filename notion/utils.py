import json
import requests

class Queries:
    def __init__(self):
        self.update_schema_qry = """{"title":[{"text":{"content":"Gradescope Assignments"}}],"properties":{"Assignment":{"title":{}},"Course":{"rich_text":{}},"Status":{"rich_text":{}},"Open Date":{"date":{}},"Due Date":{"date":{}},"Points Earned":{"type":"number","number":{"format":"number"}},"Total Points":{"type":"number","number":{"format":"number"}},"Percent Score":{"name":"Percent Score","type":"formula","formula":{"expression":"prop(\"Points Earned\")/prop(\"Total Points\")"}}}}"""

    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __iter__(self):
        return iter(self.__dict__)

        
class Endpoints:
    def __init__(self):
        self.pages = "https://api.notion.com/v1/pages"
        self.databases = "https://api.notion.com/v1/databases"
        self.search = "https://api.notion.com/v1/search"
        self.users = "https://api.notion.com/v1/users"
        self.blocks = "https://api.notion.com/v1/blocks"
        self.block_children = "https://api.notion.com/v1/blocks/{}/children"
    
    def __str__(self):
        return "Endpoints"
    
    def __repr__(self):
        return "Endpoints"
    
    def __getitem__(self, key):
        return self.__dict__[key]
    
    def __iter__(self):
        return iter(self.__dict__)


def create_row_obj(assignment):
    return {
        "Assignment": _title_obj(assignment["name"]),
        "Course": _RTO(assignment["course"]),
        "Status": _RTO(assignment["status"]),
        "Open Date": _date_obj(assignment["open_date"]),
        "Due Date": _date_obj(assignment["close_date"]),
        "Points Earned": _num_obj(assignment["points"][0]),
        "Total Points": _num_obj(assignment["points"][1])
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
import requests
from notion.utils import create_row_obj, Endpoints, Queries
import json
from gradescope.assignment import GSAssignment

class Notion:
    def __init__(self, API_KEY: str, DB_ID: str):
        self.Endpoints = Endpoints()
        self.Queries = Queries()
        self.API_KEY = API_KEY
        self.DB_ID = DB_ID
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.API_KEY}"})
        self.session.headers.update({"Notion-Version": "2022-02-22"})
        self.session.headers.update({"Content-Type": "application/json"})

    def __str__(self):
        return f"Notion Session: DB_ID: {self.DB_ID}"

    def add_assignment(self, assignment: GSAssignment):
        try:
            if self.assignment_exists(assignment):
                pass
            else:
                return self.add_assignment_request(assignment)
        except Exception as e:
            return "API Error", 400
        
    def update_schema(self):
        url = self.Endpoints.databases + self.DB_ID
        body = self.Queries["update_schema"]
        return self.session.patch(url, data=body)

    def update_assignment(self, assignment: GSAssignment):
        pass

    def assignment_exists(self, assignment: GSAssignment):
        return False
        # TODO 
        # DEBUG PLACEHOLDER

    def does_exist_request(self, assignment: GSAssignment):
        pass

    def add_assignment_request(self, assignment: GSAssignment):

        url = self.Endpoints.pages

        body = json.dumps({"parent": {"database_id": self.DB_ID}, "properties": create_row_obj(assignment)})

        return self.session.post(url, data=body)

    def update_assignment_request(self, assignment: GSAssignment):
        pass

    def compare_assignment(self, assignment: GSAssignment):
        pass
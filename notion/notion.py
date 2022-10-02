import requests
import json
from gradescope.assignment import GSAssignment
from notion.utils import create_row_obj, Endpoints, Queries

class NotionConnector:
    """
        Notion Connector Class
        - Handles requests to Notion API for adding/updating assignments
    """

    def __init__(self, API_KEY: str, DB_ID: str):
        """
            Notion Connector Class
            params:
                API_KEY: str
                DB_ID: str
        """

        self.Endpoints = Endpoints()
        self.Queries = Queries()
        self.API_KEY = API_KEY
        self.DB_ID = DB_ID
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.API_KEY}"})
        self.session.headers.update({"Notion-Version": "2022-02-22"})
        self.session.headers.update({"Content-Type": "application/json"})

    def add_assignment(self, assignment: GSAssignment):
        """ Attempts adding assignment to notion, checks if assignment already exists """
        return self._add_assignment_request(assignment)
        # try:
        #     if self.assignment_exists(assignment):
        #         pass
        #     else:
        #         return self._add_assignment_request(assignment)
        # except Exception as e:
        #     print(e)
        #     return e
        
    def update_schema(self):
        url = self.Endpoints.databases + self.DB_ID
        body = self.Queries["update_schema"]
        return self.session.patch(url, data=body)

    def update_assignment(self, assignment: GSAssignment):
        raise NotImplementedError

    def assignment_exists(self, assignment: GSAssignment):
        return False
        # TODO 
        # DEBUG PLACEHOLDER

    def does_exist_request(self, assignment: GSAssignment):
        """ Not Implemented! Checks if assignment exists in notion 
            returns -1 if not found, else returns page_id
        """
        raise NotImplementedError

    def _add_assignment_request(self, assignment: GSAssignment):
        """ Sends request to create a new assignment page in notion"""
        url = self.Endpoints.pages
        body = json.dumps({"parent": {"database_id": self.DB_ID}, "properties": create_row_obj(assignment)})
        return self.session.post(url, data=body)

    def _update_assignment_request(self, assignment: GSAssignment):
        raise NotImplementedError

    def compare_assignment(self, assignment: GSAssignment):
        raise NotImplementedError

    def __str__(self):
        return f"Notion Session: DB_ID: {self.DB_ID}"
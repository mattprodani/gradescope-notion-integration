import requests
import json
from gradescope.assignment import GSAssignment
from notion.utils import create_row_obj, Endpoints, Queries, process_db_qry, compare_to_props

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
        self.notion_db = {}
        self.load_notion_db()

    def load_notion_db(self, next_cursor = None):
        url = f"https://api.notion.com/v1/databases/{self.DB_ID}/query"
        if next_cursor:
            body = json.dumps({"start_cursor": next_cursor, "filter": {"property": "ID", "rich_text": {"is_not_empty": True}}})
        else:
            body = json.dumps({"filter": {"property": "ID", "rich_text": {"is_not_empty": True}}})

        response = self.session.post(url, data=body)
        data = json.loads(response.text)
        db, next_cursor = process_db_qry(data)
        self.notion_db.update(db)

        if next_cursor:
            self.load_notion_db(next_cursor)


    def add_assignment(self, assignment: GSAssignment):
        """ Attempts adding assignment to notion, checks if assignment already exists """
        if assignment.aid in self.notion_db:
            return self.update_assignment(assignment)
        else:
            return self._add_assignment_request(assignment)
    def update_schema(self):
        url = self.Endpoints.databases + self.DB_ID
        body = self.Queries["update_schema"]
        return self.session.patch(url, data=body)

    def update_assignment(self, assignment: GSAssignment):
        print(assignment.aid)
        if compare_to_props(assignment, self.notion_db[assignment.aid]["properties"]) == True:
            return 100
        else:
            return self._update_assignment_request(assignment)

    def _add_assignment_request(self, assignment: GSAssignment):
        """ Sends request to create a new assignment page in notion"""
        url = self.Endpoints.pages
        body = json.dumps({"parent": {"database_id": self.DB_ID}, "properties": create_row_obj(assignment)})
        return self.session.post(url, data=body)

    def _update_assignment_request(self, assignment: GSAssignment):
        """ Sends request to update an assignment page in notion"""
        url = self.Endpoints.pages + self.notion_db[assignment.aid]["page_id"]
        body = json.dumps({"properties": create_row_obj(assignment)})
        return self.session.patch(url, data=body)

    def __str__(self):
        return f"Notion Session: DB_ID: {self.DB_ID}"
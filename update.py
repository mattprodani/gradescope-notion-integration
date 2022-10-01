
import json
import json
from gradescope.scope import GSConnection
from utils import create_update_request

EMAIL = json.load(open("secrets.json"))["email"]
PASSWORD = json.load(open("secrets.json"))["password"]
DB_ID = json.load(open("secrets.json"))["db_id"]
API_KEY = json.load(open("secrets.json"))["api_key"]
gs = GSConnection(EMAIL, PASSWORD)
acc = gs.account
acc.add_courses_in_account()
courses = acc.courses
ASSIGNMENTS = {}
for cid in courses:
    course = courses[cid]
    course._load_assignments()
    for assignment in course.assignments.values():
        print(assignment.name)
        print(assignment.status)
        print(assignment.open_date)
        print(assignment.close_date)

        ASSIGNMENTS[assignment.name] = {
            "name": assignment.name,
            "course": course.name,
            "status": assignment.status,
            "open_date": assignment.open_date.strftime("%m/%d/%Y, %H:%M:%S"),
            "close_date": assignment.close_date.strftime("%m/%d/%Y, %H:%M:%S"),
            "points": assignment.points
        }
json.dump(ASSIGNMENTS, open("assignments.json", "w"), indent=4)

for assignment in ASSIGNMENTS.values():
    response = create_update_request(API_KEY, DB_ID, assignment)
    print(response.text)


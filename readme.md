# Gradescope - Notion Connector

## What is this?

This is a package that allows you to automatically upload your gradescope assigments, due dates, grades, and more to a notion database.

## Usage

**Requires:** Python >= 3.6; Packages: [bs4 (BeautifulSoup), requests]. Install with `pip install -r requirements.txt`

### Environment Variables
You can either set enviorment variables in your system or through a secrets.json file (example file provided) for the following variables:
### Notion API

First, you need to get your notion API key. To do this, go to [Notion.so](https://notion.so) and log in. Then, go to [this page](https://www.notion.so/my-integrations) and click "New Integration". Then, click "Copy Token" and paste it into the `NOTION_API_KEY` environment variable.
Then, you need to link a database to the integration, and get the database ID. To do this, go to the database you want to link, and click "Share" in the top right. Then, click "Copy Link". Use the part of the link after '/' and before '?' as the `NOTION_DB_ID` environment variable.

### Gradescope Connection

Set the `GS_USERNAME` and `GS_PASSWORD` environment variables to your gradescope username and password.

### Running
To run the program, run `python script.py` in the root directory of the project. 

## Using the NotionConnector Class

Instantiate the class with the following parameters:
- `api_key`: The API key for your notion integration
- `db_id`: The ID of the database you want to link to

To change the schema and how the data is stored, change the schema.json file according to Notion API documentation. Then, Notion.update_schema() sends a PATCH request to the API to update the schema.
To change the data parsing, change the row object formatter in notion/utils.py.

## TODO

- [x] Existing assignment detection
- [x] URL hyperlinking
- [ ] Dockerize
- [ ] Add support for multiple databases
- [ ] Automatic database creation
- [ ] Relation support for 'course id'
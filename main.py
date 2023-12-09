import requests
import os
from datetime import datetime, timezone

NOTION_TOKEN = os.environ.get('NOTION_API_SECRET')
DATABASE_ID = "eb09715cf7a84d68957308dc9b47f94e" # test database

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    print(data)

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    # results = data["results"]
    # while data["has_more"] and get_all:
    #     payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
    #     url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    #     response = requests.post(url, json=payload, headers=headers)
    #     data = response.json()
    #     results.extend(data["results"])

    return data

def create_date(start_day=None, end_day=None, start_hour=None, end_hour=None):
    start = "2023-12-10T" + str(start_hour).zfill(2) + ":00:00.000+01:00"
    end = "2023-12-10T" + str(end_hour).zfill(2) + ":00:00.000+01:00"
    date = {
        "start": start,
        "end": end,
        "time_zone": None
    }
    print(date)
    return date

def create_data():
    title = "Test Title"
    description = "Test Description"
    published_date = datetime.now().astimezone(timezone.utc).isoformat()
    data = {
        "URL": {"title": [{"text": {"content": description}}]},
        "Title": {"rich_text": [{"text": {"content": title}}]},
        "Published": {"date": {"start": published_date, "end": None}}
    }
    data = {
                "Date": {
                    # "id": "Xtp%3C",
                    "type": "date",
                    "date": create_date(1,2,3,4)
                },
                "Tags": {
                    "id": "lipg",
                    "type": "multi_select",
                    "multi_select": [
                        {
                            "id": "2781549d-6ad5-468e-a0eb-c3f815ae6cc3",
                            "name": "new",
                            "color": "blue"
                        }
                    ]
                },
                "Name": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": "AN2",
                                "link": None
                            },
                            "annotations": {
                                "bold": False,
                                "italic": True,
                                "strikethrough": True,
                                "underline": False,
                                "code": False,
                                "color": "default"
                            },
                            "plain_text": "Test2",
                            "href": None
                        }
                    ]
                }
            }
    return data

def create_page(data: dict):
    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)
    # print(res.status_code)
    return res

def main():
    print("okkkk lets go")
    data = create_data()
    create_page(data)
    # pages = get_pages()

main()
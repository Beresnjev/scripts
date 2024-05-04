from googletrans import Translator
import requests
import json
import re
import os


def translate_text(text):
    translator = Translator()
    result = translator.translate(text, src='ru', dest='et')
    return result.text


def send_request(url, data=None, post=True, dump=False):
    session = requests.Session()
    cookies = {
        "__utma": "232968074.602270297.1714154376.1714154376.1714154376.1",
        "__utmc": "232968074",
        "__utmz": "232968074.1714154376.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)",
        "_hjSession_2412119": "eyJpZCI6ImY4NzJiOWJjLTMyMTQtNDYzMC1iZTY3LWQ4NDEzNTRiNDAxOCIsImMiOjE3MTQxNTQzNzYzNDEsInMiOjAsInIiOjAsInNiIjowLCJzciI6MCwic2UiOjAsImZzIjoxLCJzcCI6MH0=",
        "_ga": "GA1.1.139261564.1714154376",
        "EKOOLSESSION": "1d0735ec-1e9f-47f1-ae5f-9045f52d47b4",
        "SESSION": "de15e5aa-f7f5-4031-ad6d-2ac962ec42e4",
        "X-AUTH": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjExNTQyMzQwOTksImZ1bGxOYW1lIjoiSW5nZStWZWluZXIiLCJ2aWV3ZWRQZXJzb25JZCI6MTE1NDIzNDA5OSwiaW5zdElkIjoyNjMsInJvbGVJZCI6MTc3MDA2MjAyNzAsImxvY2FsZSI6InJ1IiwiaWF0IjoxNzE0MjIwNjU0LCJleHAiOjE3MTQzMDcwNTQsImp0aSI6IjE3MTQyMjA2NTQifQ.XtQBaLh-Wg4ZvdZh74KdsrM7uGce3Vy4k8yLvrnRTL6Utzy-zwHitPiXFt2Dth3JAVxnTgAokVTqYiDrDcEmQpbMLGK03tTNA96wbLjA6LVLFnP5zL6olCcgwszin0MuWiMZQU9qkhla2aYnZz2siFkbNR8Bcn_P_d8NNgp9CN0",
        "DWRSESSIONID": "BKNZqnQ3qTzs9gImwIzafZT9~uD8bYBqvYo",
        "tmp_show_mobile_version": "0",
        "logged_in": "true",
        "AUTH": "B0bssySzJTG7npGQYH2x4O1MeB4uwHOk%2Bq99uu56FWDzxkyxWq%2B%2FgUqriyPc7u6UmIvj%2F%2BSy%2F0xkw2rUgaPTSj2AOUPbC28ngw%2FOTb2txsTKALy7iJhQvS6%2FwjE4M48elQIIIo%2FWich54c%2F2ZRYHFR%2Fk4xcN4oeobjoTG5g6YB%2BJmJhnYNYCe7i3uptavH9SpLRgYrshDYosuaF%2BRYrotobmhuC135HrWGUA2F7yekHKPZHGcWdVjxCG9ADLRC88oGysbW8FHglE1RpnmbJlc7aJhdrp21dEdldv49pIkoHtXkYRfF7Z%2FL3UD6q13aiEcnMb%2FeHFOKOIs6cw41%2BfSEIzq%2BVCjgCTULBSzfSlZLGugDE5ZUrpN2a%2Fh273EnmTY7qQHAndQxaYymbIVPDKKjPLR9aP99D%2FrLy4hzjVGdPvSUsg3jBL8EV%2B2DFcjonG1rUtTxEfegvtnCIOEprnwoQRJNztBs06roCuWG%2FZjSrMxFk0%2Bf3a0lb0jL7Xe2Y9lVhBO%2BmxOF%2BxSl85McA%2FMLrvzXtfZoRsqy57n44%2FKFtH%2BGa7kIX685zU8MEAgVq3LZS%2FsPKHn4ppKljrrFgAo9igUCdjJsm%2BPIQdfJosZDSlmPB6R7Re%2FYoY%2BqUVNKILGAc43%2B2wwO1Rlj1Qnef8Yw%3D%3D",
        "XSRF-TOKEN": "eyJpdiI6IlgrK1orRVhkd2FZZFZXQjhydUZSVVE9PSIsInZhbHVlIjoicTltSGZ3OER2aWt3MWxnaUQyN0M4ZkVHQjJudXBIQlErQkUvMGgwYWlLSFMwMTJRRlYvdkZ0VDBnNUlEN0VMdSIsIm1hYyI6IjYyZDc4ZGYzZDMxZDE1OWJjYjkwOWY0M2Y4N2QyNWY2MjQzNzQzMGYxMzA3ZmYxZGViZDZhZDE0YzU0ZTFmMzIiLCJ0YWciOiIifQ%3D%3D",
        "ekool_login_session": "eyJpdiI6IkQ5QXhNVlJNNElZN240MVlobkNWbVE9PSIsInZhbHVlIjoiMDJTNnc2NW82aDU4cnJLRDNTY0tIeExVbjVNVmtKeXhhMXRZWVNqeHVKVG9kaTZQdFRzN1IzZFNNajJQdVZGQUJqVXhsRWZwZXBHSE9DVDZmWk02dDhGWkNmS2JhWU02eFJHYllhUnJhVEN2eFFEOHhHaEU4NEpwbkE1S1JnZ0IiLCJtYWMiOiIyMTI0OTYxYjRjM2ZiYWY2OTAyNTAzZGYwMjAzYTE4YmY2MDY5YmRjZjNmZWM2MWNmZTUzODY4ZWIxZDJlYWQyIiwidGFnIjoiIn0%3D"
    }

    if post:
        if not dump:
            response = session.post(url, data=data, cookies=cookies)
        else:
            response = session.post(url, json=data, cookies=cookies)

    else:
        response = session.get(url, cookies=cookies)

    if 300 > response.status_code >= 200:
        return response.text
    else:
        print("Error:", response.status_code, response.text)


def extract_json_from_response(response_text):
    first_start_index = response_text.find("dwr.engine.remote.handleCallback")
    end_index = response_text.find(";\n})();\n//#DWR-END#")
    if first_start_index != -1:
        # Extract the JSON substring between the second '{' and the last '}'
        json_text = response_text[first_start_index:end_index - len(";})();//#DWR-END#") - 3]
        json_text = json_text[json_text.find("{"):]
        json_text = json_text.replace("'", '"')
        json_patched = re.sub(r'([{,:])(\s*)(\w+)(\s*):', r'\1\2"\3"\4:', json_text)

        pattern = re.compile(r'"rootEvents":(\[.*?\])', re.DOTALL)
        match = pattern.search(json_patched)

        if match:
            root_events_text = match.group(1)
            root_events_text = root_events_text.replace(':"http"', ':\\"http\\"')

        else:
            print("No rootEvents found.")
            return None

        return json.loads(root_events_text)
    return None


def contains_cyrillic(text):
    if text is None:
        return False
    # Cyrillic character ranges in Unicode
    cyrillic_ranges = [
        (0x0400, 0x04FF),  # Cyrillic
        (0x0500, 0x052F),  # Cyrillic Supplement
        (0x2DE0, 0x2DFF),  # Cyrillic Extended-A
        (0xA640, 0xA69F),  # Cyrillic Extended-B
    ]

    for char in text:
        if any(start <= ord(char) <= end for start, end in cyrillic_ranges):
            return True
    return False


def read_files_in_directory(directory_path):
    data_dict = {}

    # Get the absolute path of the directory
    abs_directory_path = os.path.abspath(directory_path)

    # Check if the directory exists
    if not os.path.isdir(abs_directory_path):
        print("Directory does not exist.")
        return data_dict

    # Iterate over files in the directory
    for filename in os.listdir(abs_directory_path):
        file_path = os.path.join(abs_directory_path, filename)
        # Check if the item is a file
        if os.path.isfile(file_path):
            # Read the content of the file
            with open(file_path, 'r') as file:
                content = json.load(file)
                # Add content to the dictionary with filename as key
                data_dict[filename[:-5]] = content

    return data_dict

journal_ids = [
    # "17707443207",  # 1.el Inimese\\u00F5petus
    # "17707441537",  # 1.el K\\u00E4eline tegevus
    # "17810405040",  # 1.el Klassijuhataja tund
    # "17810139082",  # 1.el Kunst
    # "17707441892",  # 1.el Liikumine
    # "17707429642",  # 1.el Matemaatika
    #
    # "17709632322",  # 3.d Matemaatika
    # "17709639880",  # 3.el Inimese\\u00F5petus
    # "17709640348",  # 3.el K\\u00E4eline tegevus
    # "17721242835",  # 3.el Klassijuhataja tund
    #
    # "17810140756",  # 3.el Kunst
    # "17709640743",  # 3.el Liikumine
    # "17709639584",  # 3.el Matemaatika
    "17709641468",  # 3.el\\u00D5uetund

    # "17700225147",  # 5.h Informaatika
    # "17700226101",  # 5.h Klassijuhataja tund
    # "17700226139",  # 5.h Kunst
]

for journal_id in journal_ids:
    # current_directory = os.path.dirname(os.path.abspath(__file__))
    # relative_directory = os.path.join(current_directory, "backup/", journal_id)
    # os.makedirs(relative_directory)
    #
    # getLessonsEndpoint = "https://ekool.eu/dwr/call/plaincall/courseJournalManager.getJournalDataForTeacher.dwr"
    #
    # lessonsData = {
    #     "callCount": "1",
    #     "nextReverseAjaxIndex": "0",
    #     "c0-scriptName": "courseJournalManager",
    #     "c0-methodName": "getJournalDataForTeacher",
    #     "c0-id": "0",
    #     "instanceId": "0",
    #
    #     "c0-param0": "number:" + journal_id,
    #     "batchId": "23",
    #     "page": "%2Findex_ru.html%3Fa%3D1714220598010",
    #     "scriptSessionId": "BKNZqnQ3qTzs9gImwIzafZT9~uD8bYBqvYo/VmZGHXl-*4zGFcRyl",
    # }
    #
    getLessonDataEndpoint = f"https://api-v2.ekool.eu/journal/{journal_id}/event/"
    #
    # request_response = send_request(getLessonsEndpoint, data=lessonsData)
    # print(request_response)
    # # json_text = extract_json_from_response(request_response)
    #
    # try:
    #     with open("json.json", 'r') as file:
    #         json_data = json.load(file)
    # except FileNotFoundError:
    #     print("File not found.")
    # except json.JSONDecodeError:
    #     print("Invalid JSON format in the file.")
    #
    # if json_data is None:
    #     Exception("No JSON data found.")
    #
    # event_translations = {}
    # for event in json_data:
    #     response = send_request(getLessonDataEndpoint + str(event["id"]), post=False)
    #     if response is None:
    #         continue
    #     json_response = json.loads(response)
    #     # print(json_response)
    #     # if "data" not in json_response:
    #     #     print(json_response)
    #     #     continue
    #     data = json_response["data"]
    #     title = data["title"]
    #     description = data["description"]
    #
    #     title_cyrillic = contains_cyrillic(title)
    #     description_cyrillic = contains_cyrillic(description)
    #
    #     if title_cyrillic or description_cyrillic:
    #
    #         if title is not None and title_cyrillic:
    #             translated_title = translate_text(title)
    #         elif title is None:
    #             translated_title = None
    #         else:
    #             translated_title = title
    #
    #         if description is not None and description_cyrillic:
    #             translated_description = translate_text(description)
    #         elif description is None:
    #             translated_description = None
    #         else:
    #             translated_description = description
    #
    #         event_translations[event["id"]] = {
    #             "title": translated_title,
    #             "description": translated_description,
    #             "original_body": data
    #         }

    event_translations = read_files_in_directory(f"backup/{journal_id}")
    print(len(event_translations))

    # for event_id, body in event_translations.items():
    #     print(f"Event ID: {event_id}")
    #     print(f"{body}")
    #     response = send_request(getLessonDataEndpoint + str(event_id), post=True, data=body, dump=True)
    #     print(response)

    # for event_id, translation in event_translations.items():
    #     print(f"Event ID: {event_id}")
    #     print(f"Title: {translation['title']}")
    #     print(f"Description: {translation['description']}")
    #     print(f"Original body: {translation['original_body']}")
    #     print()
    #
    #     body = translation['original_body']
    #
    #     with open(f'backup/{journal_id}/{event_id}.json', 'w') as json_file:
    #         json.dump(body, json_file)
    #
    #     body['title'] = translation['title']
    #     body['description'] = translation['description']
    #     # print(f"Updated body:\n{body}")
    #
    #     response = send_request(getLessonDataEndpoint + str(event_id), post=True, data=body, dump=True)
    #     # print(response)

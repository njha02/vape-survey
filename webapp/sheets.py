from google.cloud import storage
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.auth.transport.requests import Request

import json
from cryptography.fernet import Fernet
from typing import List


def init_sheets_service():
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "../secret.json", scopes=SCOPES
    )
    service = build("sheets", "v4", credentials=credentials)

    return service.spreadsheets()


sheets = init_sheets_service()
SPREADSHEET_ID = "144Gb6lhsflflL6MfCQcMSEsQDK819A_5EuZa6_rFtHk"
HEADERS = [
    "School",
    "Name",
    "Email",
    "Age",
    "Grade",
    "Gender",
    "Friend1",
    "Friend2",
    "Friend3",
    "Influence",
    "Vape",
]


def get_all_sheet_titles():
    return [
        x["properties"]["title"]
        for x in sheets.get(spreadsheetId=SPREADSHEET_ID).execute().get("sheets")
    ]


def create_tab(tab_name):
    body = {
        "requests": [
            {
                "addSheet": {
                    "properties": {
                        "title": tab_name,
                    }
                }
            }
        ]
    }
    result = sheets.batchUpdate(spreadsheetId=SPREADSHEET_ID, body=body).execute()
    write_to_sheet(tab_name, HEADERS)


def write_to_sheet(tab_name: str, values: List[str]):
    if tab_name not in get_all_sheet_titles():
        create_tab(tab_name)
    value_range_body = {"values": [values]}
    request = sheets.values().append(
        range=f"{tab_name}",
        spreadsheetId=SPREADSHEET_ID,
        body=value_range_body,
        valueInputOption="RAW",
    )
    response = request.execute()


# def write_to_storage(data):
#     client = storage.Client.from_service_account_json("../secret.json")
#     bucket = client.bucket("vape-survey-results")

#     def encrypt_data(data):
#         def encrypt_string(s):
#             return (
#                 Fernet(current_app.config["ENCRYPTION_KEY"])
#                 .encrypt(str.encode(s))
#                 .decode()
#             )

#         data["name"] = encrypt_string(data["name"].strip().lower())
#         data["friend1"] = encrypt_string(data["friend1"].strip().lower())
#         data["friend2"] = encrypt_string(data["friend2"].strip().lower())
#         data["friend3"] = encrypt_string(data["friend3"].strip().lower())
#         return data

#     data = encrypt_data(data)
#     print("Encrypted data", data)

#     filename = f'{data["name"]}.json'
#     blob = bucket.blob(filename)
#     blob.upload_from_string(json.dumps(data))
#     print("Data {} uploaded to {}.".format(data, filename))

#     destination = bucket.blob("data.json")
#     destination.content_type = "text/plain"
#     destination.compose([blob, destination])
#     print("Composed new object {} in the bucket {}".format("data.json", bucket.name))

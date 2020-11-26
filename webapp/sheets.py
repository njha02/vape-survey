from google.cloud import storage
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from google.auth.transport.requests import Request

import json
from cryptography.fernet import Fernet
from typing import List


SPREADSHEET_ID = "144Gb6lhsflflL6MfCQcMSEsQDK819A_5EuZa6_rFtHk"
# TODO: define all questions in file and generate form/headers/etc from that yaml file
HEADERS = [
    "School",
    "Name",
    "Age",
    "Grade",
    "Gender",
    "Friend1",
    "Friend2",
    "Friend3",
    "Influence",
    "Vape",
]

sheets_service = None


def init_sheets_service():
    global sheets_service
    if sheets_service:
        return sheets_service
    else:
        SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "./secret.json", scopes=SCOPES
        )
        service = build("sheets", "v4", credentials=credentials)
        sheets_service = service.spreadsheets()
        return sheets_service


def get_all_sheet_titles():
    sheets_service = init_sheets_service()
    return [
        x["properties"]["title"]
        for x in sheets_service.get(spreadsheetId=SPREADSHEET_ID)
        .execute()
        .get("sheets")
    ]


def create_tab(tab_name):
    sheets_service = init_sheets_service()
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
    result = sheets_service.batchUpdate(
        spreadsheetId=SPREADSHEET_ID, body=body
    ).execute()
    print(result)
    write_to_sheet(tab_name, HEADERS)


def write_to_sheet(tab_name: str, values: List[str]):
    sheets_service = init_sheets_service()
    if tab_name not in get_all_sheet_titles():
        create_tab(tab_name)
    value_range_body = {"values": [values]}
    request = sheets_service.values().append(
        range=f"{tab_name}",
        spreadsheetId=SPREADSHEET_ID,
        body=value_range_body,
        valueInputOption="RAW",
    )
    response = request.execute()
    print(response)

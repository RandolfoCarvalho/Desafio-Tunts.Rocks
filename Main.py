import os.path
from Student import Student
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1ABVotm_lBiKCWNARHBPz9lIeU4OfeTBXMiTURfHVfw8"
SAMPLE_RANGE_NAME = "A1:F27"


def main():
  creds = None

  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("sheets", "v4", credentials=creds)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = (
        sheet.values()
        .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])
    lista_de_students = []
    if not values:
        print("No data found.")
    else:
        headers = values[3]
        for row in values[3:]:
            student_data = dict(zip(headers, row))
            keys_list = list(student_data.values())
            registration = keys_list[0]
            name = keys_list[1]
            absences = keys_list[2]
            p1 = keys_list[3]
            p2 = keys_list[4]
            p3 = keys_list[5]
            student = Student(registration, name, float(absences), int(p1), int(p2), int(p3))
            student.calculate_situation()
            student.verify_situation()
            lista_de_students.append(student)

    for obj in lista_de_students:
      print(obj.Name + " - Mean: " + str(obj.Mean) + "-Nota para aprovação: " + str(obj.NAF))
  except HttpError as err:
    print(err)  


if __name__ == "__main__":
  main()
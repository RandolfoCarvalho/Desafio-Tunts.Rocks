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
SAMPLE_SPREADSHEET_ID = "12bQm4Hr6ygjO8nlVTFjVkwWc775CPNX9fT8RlO3k5Vs"
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
    list_of_students = []
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
            list_of_students.append(student)

  #Add info to Google Sheets
    addValues_G = [] 
    addValues_H = [] 
    for obj in list_of_students:
        addValues_G.append([obj.Situation.name]) 
        addValues_H.append([obj.NAF])
    result_G = (
        sheet.values()
        .update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="G4:G",
            valueInputOption="USER_ENTERED",
            body={"values": addValues_G}
        )
        .execute()
    )
    result_H = (
        sheet.values()
        .update(
            spreadsheetId=SAMPLE_SPREADSHEET_ID,
            range="H4:H",
            valueInputOption="USER_ENTERED",
            body={"values": addValues_H}
        )
        .execute()
    )

  except HttpError as err:
    print(err)  
if __name__ == "__main__":
  main()
import httplib2 
import googleapiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	
import json

CREDENTIALS_FILE = 'credits.json'  

credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])

httpAuth = credentials.authorize(httplib2.Http()) 
service = googleapiclient.discovery.build('sheets', 'v4', http = httpAuth)

def parse_data(field):
    file = open("config.json")
    data = json.load(file)[field]

    return data

def parse_csv():
  #try:
    ranges = [f"{parse_data('teachers_sheet')}!{parse_data('teachers_range')}", f"{parse_data('pipls_sheet')}!{parse_data('pipls_range')}"] 
              
    results = service.spreadsheets().values().batchGet(spreadsheetId = parse_data('google_id'), 
                                        ranges = ranges, 
                                        valueRenderOption = 'FORMATTED_VALUE',  
                                        dateTimeRenderOption = 'FORMATTED_STRING').execute() 
    ans = results['valueRanges']
    emails = list(ans[0]['values']) + list(ans[1]['values'])
    print(emails)
    while emails.count([]) != 0:
        del emails[emails.index([])] 
    for i in range(len(emails)):
        try:
            emails[i] = str(emails[i][0]).lower()
            #print(emails[i])
        except:
            break
    print(emails)
    return emails 
  #except:
   # return False

if __name__ == "__main__":
    parse_csv()
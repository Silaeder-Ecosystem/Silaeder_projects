import os
import sys
file_path = os.path.dirname(__file__)
module_path = os.path.join(file_path, "lib")
sys.path.append(module_path)

import httplib2
import googleapiclient.discovery as googleapiclient
from oauth2client.service_account import ServiceAccountCredentials
import json
CREDENTIALS_FILE = 'creditans.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.build('sheets', 'v4', httpAuth)

def parse_data(field):
    file = open('config.json')
    data = json.load(file)[field]
    return data


def parse_csv():
    ranges = [
        f'''{parse_data('teachers_sheet')}!{parse_data('teachers_range')}''',
        f'''{parse_data('pipls_sheet')}!{parse_data('pipls_range')}''']
    results = service.spreadsheets().values().batchGet(spreadsheetId=parse_data('google_id'), ranges=ranges, valueRenderOption='FORMATTED_VALUE', dateTimeRenderOption='FORMATTED_STRING').execute()
    ans = results['valueRanges']
    print(ans)
    emails = list(ans[0]['values']) + list(ans[1]['values'])
    print(emails)
    res = ['e265.lunev@yandex.ru']
    for i in emails:
        if i != []:
            if i[0].find('@') != -1:
                res.append(i[0].lower())
    print(res)
    return res


if __name__ == '__main__':
    parse_csv()

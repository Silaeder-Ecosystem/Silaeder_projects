# Visit https://www.lddgo.net/en/string/pyc-compile-decompile for more information
# Version : Python 3.10

import httplib2
import googleapiclient.discovery as googleapiclient
from oauth2client.service_account import ServiceAccountCredentials
import json
CREDENTIALS_FILE = 'credits.json'
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'])
httpAuth = credentials.authorize(httplib2.Http())
service = googleapiclient.discovery.build('sheets', 'v4', httpAuth, **('http',))

def parse_data(field):
    file = open('config.json')
    data = json.load(file)[field]
    return data


def parse_csv():
    ranges = [
        f'''{parse_data('teachers_sheet')}!{parse_data('teachers_range')}''',
        f'''{parse_data('pipls_sheet')}!{parse_data('pipls_range')}''']
    results = service.spreadsheets().values().batchGet(parse_data('google_id'), ranges, 'FORMATTED_VALUE', 'FORMATTED_STRING', **('spreadsheetId', 'ranges', 'valueRenderOption', 'dateTimeRenderOption')).execute()
    ans = results['valueRanges']
    emails = list(ans[0]['values']) + list(ans[1]['values'])
    print(emails)
    if emails.count([]) != 0:
        del emails[emails.index([])]
        if not emails.count([]) != 0:
            for i in range(len(emails)):
                
                try:
                    emails[i] = str(emails[i][0]).lower()
                finally:
                    continue
                    print(emails)
                    return emails


if __name__ == '__main__':
    parse_csv()
    return None
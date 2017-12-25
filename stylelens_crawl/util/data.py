import os
import re
from stylelens_crawl import BASE_DIR, PKG_DIR
from googleapiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

RANGE_RE = re.compile(r'^[$]?([A-Z]+)[$]?(\d+)$')


class CsvToDict(object):
    def __init__(self, headers, ranges=None):
        self.headers = headers
        self.ranges = ranges

    def make_a_header_with_ranges(self):
        assert self.headers, 'The headers value is None'
        assert self.ranges, 'The ranges values is None'

        mat = RANGE_RE.match(self.ranges.split(sep='!')[-1].split(sep=':')[0])

        assert mat, 'The range format is wrong'

        column, _ = mat.groups()

        converted_header = {}
        for header in self.headers:
            converted_header[header] = column
            column = chr(ord(column) + 1)

        return converted_header

    def convert_csv_to_dict(self, rows):
        output = []
        for row in rows:
            converted_row = {}
            for idx, header in enumerate(self.headers):
                if idx == len(row):
                    break
                converted_row[header] = row[idx]

            output.append(converted_row)

        return output


class SpreadSheets(object):
    def __init__(self, sheet_id, scope=None, key_path=None):
        if sheet_id is None:
            raise RuntimeError('The sheetid value is None.')

        if not scope:
            scope = ['https://www.googleapis.com/auth/spreadsheets.readonly']

        if not key_path:
            if os.path.exists('/tmp/gdoc_certi.json'):
                key_path = '/tmp/gdoc_certi.json'
            elif os.path.exists(os.path.join(PKG_DIR, 'cred/f3c4bf11ae96.json')):
                key_path = os.path.join(PKG_DIR, 'cred/f3c4bf11ae96.json')

        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_path, scope)
        self.service = discovery.build('sheets', 'v4', credentials=credentials)
        self.sheet_id = sheet_id

    def get_rows(self, ranges):
        return self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=ranges).execute().get(
            'values', [])

    def get_rows_with_header(self, ranges):
        result = self.service.spreadsheets().values().get(spreadsheetId=self.sheet_id, range=ranges).execute().get(
            'values', [])
        return CsvToDict(headers=result.pop(0)).convert_csv_to_dict(result)

    def update_item_with_column_key(self, ranges, item, value_input_option='USER_ENTERED'):
        return self.service.spreadsheets().values().update(spreadsheetId=self.sheet_id, range=ranges,
                                                        valueInputOption=value_input_option, body={
                                                            'values': item
                                                        }).execute()

import json
from stylelens_crawl.util.data import SpreadSheets

print(json.dumps(SpreadSheets(sheet_id='1In9_1IbEyzU-nU57WxF1JbjXTki2yHkwIJfXZRY7ZjQ').get_rows_with_header("'크롤링'!A9:AD3000"), ensure_ascii=False))

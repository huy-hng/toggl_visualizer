import json
import os
import time

import requests

from dotenv import load_dotenv
load_dotenv()

base_url = 'https://api.track.toggl.com/reports/api/v2'
WORKSPACE_ID = '3863836'

def date_builder(year: int, month: int, day: int):
	def padder(num):
		return str(num).rjust(2, '0')
	return f'{padder(year)}-{padder(month)}-{padder(day)}'

def request(payload):
	while True:
		time.sleep(0.1)

		res = requests.get(f'{base_url}/details',
						params=payload,
						auth=(os.getenv('API_TOKEN'), 'api_token'))

		if res.status_code == 200:
			break
		elif res.status_code == 429:
			time.sleep(1)
			continue
		else:
			raise Exception('unknown status code Exception', res.status_code)


	return res

def get_report_since(since: str):
	params = {
		'user_agent': 'asdf',
		'workspace_id': WORKSPACE_ID,
		'since': since,
	}

	page = 1
	combined_data = []
	while True:
		params['page'] = page
		res = request(params)
		data = json.loads(res.text)

		if not data['data']:
			break

		combined_data += data['data']
		page += 1

	with open(f'./data/{since}.json', 'w') as f:
		f.write(json.dumps(combined_data, indent=2))
	return combined_data



if __name__ == '__main__':
	get_report_since(date_builder(2022, 2, 1))
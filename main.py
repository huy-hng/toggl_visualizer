import datetime
import json
from dataclasses import dataclass

import pandas as pd

from helpers import parse_time

@dataclass
class TogglEntry:
	description: str
	start: datetime
	end: datetime
	dur: int
	client: str
	project: str

	def __init__(self, entry: dict):
		self.description = entry['description']
		self.start = parse_time(entry['start'])
		self.end = parse_time(entry['end'])
		self.dur = int(entry['dur'] / 1000)
		self.client = entry['client']
		self.project = entry['project']

def duration_report(data: list[TogglEntry]):
	report = {}
	for d in data:
		if d.client not in report:
			report[d.client] = 0

		report[d.client] += d.dur
		
	report = {k: round(v/3600, 2) for k,v in report.items()}

	return report

# def filter_by_day(data: list[TogglEntry], day: datetime.date):
# 	for 

def sum_duration(data: list[TogglEntry]):
	duration = 0
	for d in data:
		duration += d.dur
	return duration

def weekly_report(data: list[TogglEntry]):
	end_date = datetime.datetime.now().date()
	num_days = datetime.timedelta(days=7)
	current_day = end_date - num_days
	one_day = datetime.timedelta(days=1)
	report = {
		'dur': 0,
		'clients': {
			'dur': 0,
			'projects': {
				'dur': 0,
				'descriptions': []
			}
		}
	}
	for d in data:
		while d.end != current_day:
			current_day += one_day

		clients = report['clients']
		if d.client not in report:
			clients[d.client] = {
				'duration': 0,
				'projects': {}
			}

		projects = clients[d.client]['projects']
		if d.project not in clients[d.client]['projects']:
			clients[d.client][d.project] = {}
		if d.description not in report[d.client][d.project]:
			clients[d.client][d.project]

		if d.end.date() == current_day:
			report





def main():
	with open('./data/2022-02-01.json') as f:
		data = json.load(f)

	parsed_data: list[TogglEntry] = []
	for entry in data:
		parsed_data.append(TogglEntry(entry))

	duration = sum_duration(parsed_data)
	print(duration)
	# report = duration_report(parsed_data)
	# print(report)


if __name__ == '__main__':
	main()
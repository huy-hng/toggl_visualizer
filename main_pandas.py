# %%
import datetime
import json
from dataclasses import dataclass

import pandas as pd
pd.options.display.width = 0

from helpers import parse_time


def get_last_week(df: pd.DataFrame):
	df['start_date'] = df['start'].apply(lambda x: x.date())
	df['end_date'] = df['end'].apply(lambda x: x.date())

	end_date = datetime.datetime.now().date()
	start_date = end_date - datetime.timedelta(days=7)

	mask = (df['start_date'] >= start_date) & (df['end_date'] < end_date)
	filtered = df.loc[mask]
	return filtered


def get_group_durations(df: pd.DataFrame, group_name: str):
	# mi = pd.MultiIndex.from_frame(df, column=['client', 'project'])
	column_values = df[['client', 'project', 'description']]
	# unique_values = pd.unique(column_values)
	# print(column_values)

	index = pd.MultiIndex.from_frame(column_values)
	s = pd.Series(0, index=index)
	print(s)

	# for e in index:
	# 	print(e)

	# grouped = df.groupby(['end_date', group_name])
	date_group = df.groupby('start_date')
	week = pd.DataFrame()
	week['day_total'] = 0

	for date in date_group.groups:
		day = date_group.get_group(date)
		grouped = day.groupby(group_name)

		total_day_dur = 0
		for group in grouped.groups:
			dur = sum(grouped.get_group(group)['dur'])
			total_day_dur += dur
			week.loc[date, group] = dur

		week.loc[date, 'day_total'] = total_day_dur

	week.fillna(0, inplace=True)

	# add total column
	week.loc['total'] = 0
	for col in week.columns:
		week.loc['total', col] = sum(week[col])

	# create df with percentages
	# week_percentages = week.copy()
	# week_percentages.drop('day_total', axis=1, inplace=True)
	# for col in week_percentages.columns:
	# 	week_percentages[col] = round(week[col] / week["day_total"] * 100, 2)

	return week#, week_percentages


def main():
	df = pd.read_json('./data/2022-02-01.json')
	rows_to_delete = ['id', 'pid', 'tid', 'uid', 'billable', 'is_billable', 'cur',
										'tags', 'task', 'project_color']
	df.drop(rows_to_delete, axis=1, inplace=True)
	df['start'] = df['start'].apply(parse_time)
	df['end'] = df['end'].apply(parse_time)
	df['dur'] = df['dur'].apply(lambda x: int(x/1000))

	last_week = get_last_week(df)

	week, week_percentages = get_group_durations(last_week, 'client')
	week_hours = week.applymap(lambda x: round(x/3600, 2))
	print(week_hours.head(10))
	print()
	print(week_percentages.head(10))


if __name__ == '__main__':
	main()
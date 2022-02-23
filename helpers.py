import datetime

def parse_time(time: str):
	time = time.split('+')[0]
	return datetime.datetime.strptime(time, '%Y-%m-%dT%H:%M:%S')

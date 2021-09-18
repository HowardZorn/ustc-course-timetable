import json
import argparse
from icalendar import Calendar, Event
from datetime import datetime

argp = argparse.ArgumentParser()
argp.add_argument('json_file')
args = argp.parse_args()


cal = Calendar()
cal.add('prodid', '-//ustc timetable//timetable//CN')
cal.add('version', '2.0')
cal.add('TZID', 'Asia/Shanghai')
cal.add('X-WR-TIMEZONE', 'Asia/Shanghai')

j = str(open(args.json_file, 'r', encoding='utf-8').read())
j = json.loads(j)

lesson = {}

for l in j["result"]["lessonList"]:
    id = l["id"]
    lesson[id] = l

print("你选了：")
for id in lesson:
    print(lesson[id]['courseName'])

course_dict = {}

for s in j['result']['scheduleList']:
    summary = lesson[s['lessonId']]['courseName']
    location = s['room']['nameZh']
    description = s['personName']
    startTime = '%.4d' % s['startTime']
    endTime = '%.4d' % s['endTime']
    dtstart = datetime.strptime(s['date'] + ' ' + startTime, '%Y-%m-%d %H%M')
    dtend = datetime.strptime(s['date'] + ' ' + endTime, '%Y-%m-%d %H%M')
    key = (summary, location, dtstart, dtend)
    if key in course_dict:
        course_dict[key].append(description)
    else:
        course_dict[key] = [description]

for key, value in course_dict.items():
    summary, location, dtstart, dtend = key
    description = '，'.join(value)
    event = Event()
    event.add('summary', summary)
    event.add('location', location)
    event.add('description', description)
    event.add('dtstart', dtstart)
    event.add('dtend', dtend)
    event.add('dtstamp', datetime.utcnow())
    cal.add_component(event)

f = open('courses.ics', 'wb')
f.write(cal.to_ical())
f.close()

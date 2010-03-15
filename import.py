import apachelog     # for parsing log
import sys           # for sterr
import riak
import re
import json

import time
import datetime
import pytz

# import pdb
# pdb.set_trace()

HOST = 'localhost'
PORT = 8098
BUCKET = 'test4'
FILE = '/home/vishvananda/nasa/tbllog/access.log'
FORMAT = apachelog.formats['extended']
IGNORE = (
    ur"\.gif$",
    ur"\.jpg$",
    ur"\.js$",
    ur"\.css$",
    ur"\.ico$",
    ur"^/flickr/",
    ur"^/feed/",
)

ignore_compiled = []
for s in IGNORE:
    ignore_compiled.append(re.compile(s))

class Timezone(datetime.tzinfo):

    def __init__(self, name="+0000"):
        self.name = name
        seconds = int(name[:-2])*3600+int(name[-2:])*60
        self.offset = datetime.timedelta(seconds=seconds)

    def utcoffset(self, dt):
        return self.offset

    def dst(self, dt):
        return datetime.timedelta(0)

    def tzname(self, dt):
        return self.name

def parse_apache_date(date_str, tz_str):
    tt = time.strptime(date_str, "%d/%b/%Y:%H:%M:%S")
    tt = tt[:6] + (0, Timezone(tz_str))
    return datetime.datetime(*tt).astimezone(pytz.utc)

def httpdate(dt):
    weekday = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"][dt.weekday()]
    month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep",
             "Oct", "Nov", "Dec"][dt.month - 1]
    return "%s, %02d %s %04d %02d:%02d:%02d GMT%s" % (weekday, dt.day, month,
        dt.year, dt.hour, dt.minute, dt.second, dt.tzinfo.name)

def ignored(url):
    for exp in ignore_compiled:
        result = exp.search(url)
        if result != None:
            return True
    return False

client = riak.RiakClient(HOST, PORT)
bucket = client.bucket(BUCKET)

p = apachelog.parser(FORMAT)


id = 0
for line in open(FILE):
    try:
        data = p.parse(line)
        request_parts = data["%r"].split(" ")
        url_parts = request_parts[1].partition("?")
        if not ignored(url_parts[0]):
            id += 1
            hit = {}
            hit['host'] = data["%h"]
            hit['url'] = url_parts[0];
            hit['query'] = url_parts[2];
            hit['referrer'] = data["%{Referer}i"]
            hit['agent'] = data["%{User-agent}i"]
            hit['status'] = data["%>s"]
            dt = parse_apache_date(data["%t"][1:21], data["%t"][-6:-1])
            # date is in UTC
            hit['date'] = dt.strftime('%Y-%m-%d')
            # javascript friendly date
            hit['timestamp'] = dt.strftime('%s')
            # hit['longdate'] = httpdate(dt)
            # print json.dumps(hit)
            if id % 1000 == 0: print id, hit['date']
            if hit['date'] == '2010-02-08': break;
#            if id == 5001: break;
            obj = bucket.new(str(id), hit).store()
    except apachelog.ApacheLogParserError:
        sys.stderr.write("Unable to parse %s" % line)

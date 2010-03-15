from logs import riak
from lib.decorators import render_to
from django.conf import settings

@render_to('logs/index.html')
def index(request):
    return {}

@render_to('logs/top_pages_day.html')
def top_pages_day(request, year, month, day):
    client = riak.RiakClient(settings.RIAK_HOST, settings.RIAK_PORT)
    date = year + u'-' + month + u'-' + day
    pages = client \
    .add(settings.RIAK_BUCKET) \
    .map("function (value) {"
      +  "    var hit = JSON.parse(value.values[0].data);"
      +  "    if (hit.date == '" + date.encode('ascii') + "') {"
      +  "        return [{url: hit.url, hits: 1}];"
      +  "    } else {"
      +  "        return []"
      +  "    }"
      +  "}") \
    .reduce("function (values) {"
      +  "    var result = [];"
      +  "    for (var i in values) {"
      +  "        var found = false;"
      +  "        for (var j in result) {"
      +  "            if (result[j].url == values[i].url) {"
      +  "                result[j].hits += values[i].hits;"
      +  "                found = true;"
      +  "            }"
      +  "        }"
      +  "        if(!found) result.push(values[i]);"
      +  "    }"
      +  "    return result;"
      +  "}") \
    .reduce("Riak.reduceSort", {'arg': "function (a, b) {"
      +  "    return a.hits < b.hits;"
      +  "}"}) \
    .reduce("Riak.reduceLimit", {'arg': 10}) \
    .run()
    return { 'date': date, 'pages': pages }

@render_to('logs/view_depth_day.html')
def view_depth_day(request, year, month, day):
    client = riak.RiakClient(settings.RIAK_HOST, settings.RIAK_PORT)
    date = year + u'-' + month + u'-' + day
    pages = client \
    .add(settings.RIAK_BUCKET) \
    .map("function (value) {"
      +  "    var hit = JSON.parse(value.values[0].data);"
      +  "    if (hit.date == '" + date.encode('ascii') + "') {"
      +  "        return [{url: hit.url, hits: 1}];"
      +  "    } else {"
      +  "        return []"
      +  "    }"
      +  "}", {'timeout': 180000}) \
    .reduce("function (values) {"
      +  "    var result = [];"
      +  "    for (var i in values) {"
      +  "        var found = false;"
      +  "        for (var j in result) {"
      +  "            if (result[j].url == values[i].url) {"
      +  "                result[j].hits += values[i].hits;"
      +  "                found = true;"
      +  "            }"
      +  "        }"
      +  "        if(!found) result.push(values[i]);"
      +  "    }"
      +  "    return result;"
      +  "}", {'timeout': 180000}) \
    .reduce("Riak.reduceSort", {'arg': "function (a, b) {"
      +  "    return a.hits < b.hits;"
      +  "}"}) \
    .reduce("Riak.reduceLimit", {'arg': 10}) \
    .run()
    return { 'date': date, 'pages': pages }


@render_to('logs/page_views_month.html')
def page_views_month(request, year, month):
    client = riak.RiakClient(settings.RIAK_HOST, settings.RIAK_PORT)
    date = year + u'-' + month
    days = client \
    .add(settings.RIAK_BUCKET) \
    .map("function (value) {"
      +  "    var hit = JSON.parse(value.values[0].data);"
      +  "    if (hit.date.substring(0,7) == '2010-02') {"
      +  "        return [{day: parseInt(hit.date.substring(8), 10), hits: 1}];"
      +  "    } else {"
      +  "        return [];"
      +  "    }"
      +  "}", {'timeout': 120000}) \
    .reduce("function (values) {"
      +  "    var result = [];"
      +  "    for (var i in values) {"
      +  "        var found = false;"
      +  "        for (var j in result) {"
      +  "            if (result[j].day == values[i].day) {"
      +  "                result[j].hits += values[i].hits;"
      +  "                found = true;"
      +  "            }"
      +  "        }"
      +  "        if(!found) result.push(values[i]);"
      +  "    }"
      +  "    return result;"
      +  "}", {'timeout': 120000}) \
    .reduce("Riak.reduceSort", {'arg': "function (a, b) {"
      +  "    return a.day > b.day;"
      +  "}"}) \
    .run()
    return { 'date': date, 'days': days }

@render_to('logs/unique_ips_month.html')
def unique_ips_month(request, year, month):
    client = riak.RiakClient(settings.RIAK_HOST, settings.RIAK_PORT)
    date = year + u'-' + month
    days = client \
    .add(settings.RIAK_BUCKET) \
    .map("function (value) {"
      +  "    var hit = JSON.parse(value.values[0].data);"
      +  "    if (hit.date.substring(0,7) == '" + date.encode('ascii') + "') {"
      +  "        return [{day: parseInt(hit.date.substring(8)), ips: [hit.host] }];"
      +  "    } else {"
      +  "        return []"
      +  "    }"
      +  "}") \
    .reduce("function (values) {"
      +  "    var result = [];"
      +  "    for (var i in values) {"
      +  "      var found = false;"
      +  "      for (var j in result) {"
      +  "        if (result[j].day == values[i].day) {"      
      +  "          var merged = result[j].ips.concat(values[i].ips);"
      +  "          var t;"
      +  "          for(k = 0; k < merged.length; k++) {"
      +  "            if((t = merged.indexOf(k + 1, merged[k])) != -1) {"
      +  "              merged.splice(t, 1);"
      +  "              k--;"
      +  "            }"
      +  "          }"
      +  "          result[j].ips = merged;"
      +  "          found = true;"
      +  "        }"
      +  "      }"
      +  "      if(!found) result.push(values[i]);"
      +  "    }"
      +  "    return result;"
      +  "}") \
    .reduce("Riak.reduceSort", {'arg': "function (a, b) {"
      +  "    return a.day > b.day;"
      +  "}"}) \
    .run()

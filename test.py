import riak

HOST = 'localhost'
PORT = 8098
BUCKET = 'test4'

client = riak.RiakClient(HOST, PORT)
for i in range(1, 19707):
    client = client.add(BUCKET, str(i))
print client \
    .map("function (value) {"
      +  "    if(!value.values) return [];"
      +  "    var hit = JSON.parse(value.values[0].data);"
      +  "    if (hit.date == '2010-02-07') {"
      +  "        return [1];"
      +  "    } else {"
      +  "        return [];"
      +  "    }"
      +  "}", {'timeout': 200000}) \
    .reduce("Riak.reduceSum", {'timeout': 200000}).run()

client = riak.RiakClient(HOST, PORT)
print client.add(BUCKET) \
    .map("function (value) {"
      +  "    return [1];"
      +  "}", {'timeout': 200000}) \
    .reduce("Riak.reduceSum", {'timeout': 200000}).run()

client = riak.RiakClient(HOST, PORT)
print client.add(BUCKET) \
    .map("function (value) {"
      +  "    var hit = JSON.parse(value.values[0].data);"
      +  "    if (hit.date == '2010-02-07') {"
      +  "        return [1];"
      +  "    } else {"
      +  "        return [];"
      +  "    }"
      +  "}", {'timeout': 200000}) \
    .reduce("Riak.reduceSum", {'timeout': 200000}).run()

def blah():
    client \
    .map("function (value) {"
      +  "    var hit = JSON.parse(value.values[0].data);"
      +  "    if (hit.date == '2010-02-07') {"
      +  "        return [1];"
      +  "    } else {"
      +  "        return [];"
      +  "    }"
      +  "}", {'timeout': 200000}) \
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

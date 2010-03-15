import riak
import json

# import pdb
# pdb.set_trace()

HOST = 'localhost'

PORT = 8098

client = riak.RiakClient(HOST, PORT)

print client \
    .add("test2") \
    .map("function (value) {"
      +  "    return [1];"
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

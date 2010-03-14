import riak
import json

# import pdb
# pdb.set_trace()

HOST = 'localhost'

PORT = 8098

client = riak.RiakClient(HOST, PORT)

print client \
    .add("test3") \
    .map("function (value) {"
      +  "    var hit = JSON.parse(value.values[0].data);"
      +  "    if (hit.date == '2010-03-13') {"
      +  "        return [hit.url];"
      +  "    } else {"
      +  "        return []"
      +  "    }"
      +  "}") \
    .reduce("function (values) {"
      +  "    var result = {};"
      +  "    for (var index in values) {"
      +  "        if (values[index] in result) {"
      +  "            result[values[index]] += 1;"
      +  "        } else {"
      +  "            result[values[index]] = 1;"
      +  "        }"
      +  "    }"
      +  "    var sortresult = [];" 
      +  "    for (var index in result) {"
      +  "        sortresult.push( [index, result[index]] );"
      +  "    }"
      +  "    sortresult.sort(function (a, b) {"
      +  "                         return a[1] < b[1];"
      +  "                    });"
      +  "    return sortresult.slice(0, 10);"
      +  "}") \
    .run()

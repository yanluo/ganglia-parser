import urllib2
import re
import sys
import json
from pprint import pprint
import matplotlib.pyplot as plt

if len (sys.argv) < 2:
    print 'Usage: python grepip.py [Ganglia Web UI URL]'
    sys.exit(2)
else:
    gangliaUrl = sys.argv[-1]

contents = urllib2.urlopen(gangliaUrl).read()

pattern = re.compile('ip-\w{1,3}-\w{1,3}-\w{1,3}-\w{1,3}\.ec2\.internal')
result = pattern.findall(contents)

seen = set()
remove_duplicate = []
for item in result:
    if item not in seen:
        seen.add(item)
        remove_duplicate.append(item)
print remove_duplicate

jsonUrl = []
for index, value in enumerate (remove_duplicate):
    jsonUrl.append (gangliaUrl + 'graph.php?r=hour&h='+ value + '&m=load_one&s=by+namei&m=cpu_nice&mc=2&g=cpu_report&c=spark&json=1')

jsonContents = []
data = []
time = []
yaxis = []
for index, value in enumerate (remove_duplicate):
    jsonContents.append( urllib2.urlopen(jsonUrl[index]).read() )
    localFile = open( value+'.json', 'w' )
    localFile.write(jsonContents[index])
    localFile.close()

    jsontmp = json.loads(jsonContents[index])
    data.append(jsontmp)
    for i in xrange (0, len(data[index][0]['datapoints'])):
        time.append(data[index][0]['datapoints'][i][1])
        yaxis.append(data[index][0]['datapoints'][i][0])

plt.plot(time,yaxis, 'k')
plt.show()

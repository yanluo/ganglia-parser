#!/usr/bin/python

__author__ = 'Peilong'

import urllib2
import re
import sys
import json
from pprint import pprint
import matplotlib.pyplot as plt
import ConfigParser
import string
import decimal


if len (sys.argv) < 2:
    print 'Usage: python gangliaParser.py target.conf'
    sys.exit(2)
else:
    filename = sys.argv[-1]

print '-'*45
print ' *** Ganglia Visualization Tool V-0.1.3 ***'
print ''
print ' Usage: python gangliaParser.py target.conf'
print '-'*45

cf = ConfigParser.ConfigParser()    
cf.read(filename)

dnsAddress = cf.get("target","dns")
gangliaUrl = dnsAddress + ':5080/ganglia/'
#print gangliaUrl

contents = urllib2.urlopen(gangliaUrl).read()

pattern = re.compile('ip-\w{1,3}-\w{1,3}-\w{1,3}-\w{1,3}\.ec2\.internal')
result = pattern.findall(contents)

seen = set()
remove_duplicate = []
for item in result:
    if item not in seen:
        seen.add(item)
        remove_duplicate.append(item)
#print remove_duplicate

jsonUrl = []
for index, value in enumerate (remove_duplicate):
    jsonUrl.append (gangliaUrl + 'graph.php?r=hour&c=spark&h='+ value + '&v=0.0&m='+cf.get("option","metric")+'&jr=&js=&vl=KB&json=1')
#print jsonUrl

jsonContents = []
data = []
xaxis = []
yaxis = []
for index, value in enumerate (remove_duplicate):
    jsonContents.append( urllib2.urlopen(jsonUrl[index]).read() )
    localFile = open( value+'.json', 'w' )
    localFile.write(jsonContents[index])
    localFile.close()

    xaxistmp = []
    yaxistmp = []

    jsontmp = json.loads(jsonContents[index])
    data.append(jsontmp)
    if data[index] is not None:
        for i in xrange (0, len(data[index][0]['datapoints'])):
            xaxistmp.append(data[index][0]['datapoints'][i][1])
            yaxistmp.append(data[index][0]['datapoints'][i][0])
        xaxis.append(xaxistmp)
        yaxis.append(yaxistmp)


graph_number = int (cf.get("node","number"))
for index in xrange (0,graph_number):
    plt.figure(index)
    plt.title(remove_duplicate[index])
    plt.plot(xaxis[index], yaxis[index], 'k')
    plt.ylabel('Value')
    plt.xlabel('Time (1 hour in total)')
    
plt.show()
    

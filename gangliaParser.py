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
import os


if len (sys.argv) < 2:
    print 'Usage: python gangliaParser.py target.conf'
    sys.exit(2)
else:
    filename = sys.argv[-1]

### Header
print '-'*45
print ' *** Ganglia JSON Parser Tool V - 0.1.5 ***'
print ''
print ' Usage: python gangliaParser.py target.conf'
print '-'*45

### Configuration file parser
cf = ConfigParser.ConfigParser()    
cf.read(filename)

dnsAddress = cf.get("target","dns")
metric = cf.get("option","metric")
node_number = int (cf.get("node","number"))

### Ganglia web UI IP address
gangliaUrl = dnsAddress + ':5080/ganglia/'

### Ganglia web UI index page
contents = urllib2.urlopen(gangliaUrl).read()

### Regular experssion matching to grab the node internal IP
pattern = re.compile('ip-\w{1,3}-\w{1,3}-\w{1,3}-\w{1,3}\.ec2\.internal')
result = pattern.findall(contents)

seen = set()
remove_duplicate = []
for item in result:
    if item not in seen:
        seen.add(item)
        remove_duplicate.append(item)

### Concatenate the final URL where JSON data locates
jsonUrl = []
for index, value in enumerate (remove_duplicate):
    jsonUrl.append (gangliaUrl + 'graph.php?r=hour&c=spark&h='+ value + '&v=0.0&m='+ metric +'&jr=&js=&vl=KB&json=1')

jsonContents = []
data = []
xaxis = []
yaxis = []

### Create directory
directory = './'+str(node_number)+'_nodes'
if not os.path.exists(directory):
    os.makedirs(directory)

### Generate the JSON files
for index in xrange (0, node_number):
    jsonContents.append( urllib2.urlopen(jsonUrl[index]).read() )
    localFile = open( directory+'/'+remove_duplicate[index]+'-'+metric+'.json', 'w' )
    localFile.write(jsonContents[index])
    localFile.close()

    xaxistmp = []
    yaxistmp = []

    jsontmp = json.loads(jsonContents[index])
    data.append(jsontmp)
    if data[index] is not None:
        # The last one or two points are usually not accurate, so -2
        for i in xrange (0, len(data[index][0]['datapoints']) - 2):
            xaxistmp.append(data[index][0]['datapoints'][i][1])
            yaxistmp.append(data[index][0]['datapoints'][i][0])
        xaxis.append(xaxistmp)
        yaxis.append(yaxistmp)

### Plot JSON data to png figures
for index in xrange (0, len(xaxis)):
    if xaxis[index] and yaxis [index] is not None:
        plt.figure(index)
        plt.title(remove_duplicate[index])
        plt.plot(xaxis[index], yaxis[index], marker='o', linestyle='-', color='r',)
        plt.ylabel('Value '+ metric)
        plt.xlabel('Time (1 hour in total)')
        plt.savefig(directory+'/'+remove_duplicate[index]+'-'+metric+'.png')

### Final printout message
print '+'*45
print '[SUCCESS] .JSON and .PNG files are saved!'
print '+'*45

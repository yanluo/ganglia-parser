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

def get_metric(remove_duplicate, metric):
    for index, value in enumerate (remove_duplicate):
        #print index, value
        ### Concatenate the final URL where JSON data locates
        jsonUrl = gangliaUrl + 'graph.php?r=hour&c=spark&h='+ value + '&v=0.0&m='+ metric +'&jr=&js=&json=1'
        print "--> from host: ", value 

        ### Generate the JSON files
        response = urllib2.urlopen(jsonUrl)
        jsondata = json.load(response)
        localFile = open( remove_duplicate[index] + '-' + metric +'.json', 'w' )
        #print "data =", jsondata
        json.dump(jsondata, localFile)
        localFile.close()

        # check if json file is empty or contains "null"
        if jsondata == None:
            continue

        xaxis = []
        yaxis = []

        #print jsondata[0]
        rawdata = jsondata[0]['datapoints']
        #print "rawdata=", rawdata
        for i in xrange (0, len(rawdata)):
            xaxis.append(rawdata[i][1])
            yaxis.append(rawdata[i][0])

        ### Plot JSON data to png figures
        plt.figure(index)
        plt.title(remove_duplicate[index])
        plt.plot(xaxis[index], yaxis[index], 'k')
        plt.ylabel('Value '+ metric)
        plt.xlabel('Time (1 hour in total)')
        plt.savefig(remove_duplicate[index] + '-' + metric +'.png')

    return

if len (sys.argv) < 2:
    print 'Usage: python gangliaParser.py target.conf'
    sys.exit(2)
else:
    filename = sys.argv[-1]

### Header
print '-'*45
print ' *** Ganglia Visualization Tool V-0.2 ***'
print ''
print ' Usage: python gangliaParser.py target.conf'
print '-'*45

### Configuration file parser
cf = ConfigParser.ConfigParser()    
cf.read(filename)

dnsAddress = cf.get("target","dns")
# metrics is comma separated list
metrics = cf.get("option","metrics")
#node_number = int (cf.get("node","number"))

### Ganglia web UI IP address
gangliaUrl = 'http://'+dnsAddress + ':5080/ganglia/'

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

#print "set size =", len(seen)
num_nodes = len(seen)

# get all the metrics one by one
for metric in metrics.split(','):
    print "Getting metric "+metric
    get_metric(remove_duplicate, metric)

### Final printout message
print '+'*45
print '[SUCCESS] .JSON and .PNG files are saved!'
print '+'*45

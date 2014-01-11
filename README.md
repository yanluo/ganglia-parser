ganglia-parser
==============

Parser to retrieve and plot Ganglia metrics from an EC2 cluster

--------------
How to use:

1. Configure the "target.conf" file with the parameters required 
in each section. Here is a simple example:
	[target]
	dns=http://ec2-54-221-160-93.compute-1.amazonaws.com

	[option]
	metric=cpu_system

	[node]
	number=2
This file contains the DNS server where Ganglia gmetad process
is running, the metric option and the number of nodes.

2. Run script: ./gangliaParser.py target.conf
or python gangliaParser.py target.conf

3. Two kinds of files will be automatically saved to the current
directry. One is JSON files that contains the wanted metric data,
the other is png figures that visualized the JSON data.

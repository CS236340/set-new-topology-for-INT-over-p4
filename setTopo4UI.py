import argparse
import sys
import os
import math
from decimal import Decimal

HOST_NAME = 0
VXLAN_CFG = 1
VXLAN_CFG_NAME = 0
VXLAN_IP = 2
SWITCH_NAME = 1
SWITCH_ID_STR = 1
SWITCH_ID = 0
HEX_VAL_ID = 1
SWITCH_NODE = 0
HOST_NODE = 1
SWITCH_NODE_STR = 1

def getSwitchList(inputFileName):
	inputFile = open(str(inputFileName))
	switches = {}
	keyFlag = 0
	for line in inputFile:
		if (line.find('SwitchConfig(') <> -1 and keyFlag == 0):
			key = line.split(' = ')[SWITCH_NAME].replace(',\n','')
			keyFlag = 1		
		if (line.find('switch_id  = ') <> -1 and keyFlag == 1):
			tempVal = line.split(' = ')[SWITCH_ID_STR].split(', ')[SWITCH_ID]
			val = tempVal[0:2] 
			count = 0
			#print tempVal.split('x')[1]
			for char in tempVal.split('x')[HEX_VAL_ID]:
				if (char <> '0'):
					break
				count += 1
			#print count
			val += tempVal.split('x')[HEX_VAL_ID][count:]
			val = val.lower()
			keyFlag = 0
			switches[key] = '\"' + val + '\"'
	return switches
		

def getHostList(inputFileName):
	inputFile = open(str(inputFileName))
	hosts = {}
	vxlans = {}
	for line in inputFile:
		if (line.find('VxlanConfig(') <> -1):
			key = line.split(' = ')[VXLAN_CFG_NAME].replace(' ','')
			val = line.split(', ')[VXLAN_IP].replace('\'','\"')
			vxlans[key]=val
		if (line.find('HostConfig(') <> -1):	
			key = line.split(' : ')[HOST_NAME].replace(' ','')
			tempVxlansKey = line.split('vxlan_cfg = ')[VXLAN_CFG].replace(',','').split(' ')[VXLAN_CFG_NAME]
			hosts[key] = vxlans[tempVxlansKey]

	return hosts


def setTopo(inputFileName):
#hosts:
	hostList = getHostList(inputFileName)
	FileOutput = open("//home//yamit//project//p4factory//apps//int//monitor//topology.json" , "w+")
	FileOutput.write('{\n')
	hosts = '  "hosts" : [ '
	for ip in hostList.values():
		hosts += ip + ", "
	hosts += '],'	
	hosts = hosts.replace('\", ]', '\" ]')
	FileOutput.write(hosts)
	FileOutput.write('\n')	
	#print hosts

#switches:
	FileOutput.write('  "switches" : [\n')
	switchList = getSwitchList(inputFileName)

	#leaves:
	leaves = "    [ "
	for switch in switchList.keys():
		if (switch.find('leaf') <> -1):
			leaves += switchList[switch] + ', '
	leaves += '],'
	leaves = leaves.replace('\", ]', '\" ]')
	FileOutput.write(leaves)
	FileOutput.write('\n')	

	#spines:
	spines = "    [ "
	for switch in switchList.keys():
		if (switch.find('spine') <> -1):
			spines += switchList[switch] + ', '
	spines += ']'
	spines = spines.replace('\", ]', '\" ]')
	FileOutput.write(spines)
	FileOutput.write('\n')	
	FileOutput.write('  ],\n')
#host_leaf_conns:
	FileOutput.write('  "host_leaf_conns" : {\n')
	inputFile = open(str(inputFileName))
	conns = ''
	for line in inputFile:
		if (line.find('LinkConfig(') <> -1):
			node1 = line.split('( ')[SWITCH_NODE_STR].split(',')[SWITCH_NODE]
			node2 = line.split(', ')[HOST_NODE]
			if (node2 not in hostList.keys()):
				continue
			conns += '    ' + hostList[node2] + " : " + switchList[node1.replace("\"", '')] + ',\n'
	conns = conns [:-2]
	FileOutput.write(conns)
	FileOutput.write('\n')
	FileOutput.write('  }\n')
	FileOutput.write('}')	
	#for line in inputFile:
	#	if (line.find('VxlanConfig(') <> -1):
	#		#print line
	#		hosts = hosts + line.split(', ')[2].replace('\'','\"') +', '
	#hosts = hosts + '],'	
	#FileOutput.write(hosts.replace('\", ]', '\" ]'))
	#FileOutput.write('\n')

	#FileOutput.write('  "switches" : [\n')


def main():
	parser = argparse.ArgumentParser(prog='setTopology', add_help=False)
	parser.add_argument("-h", "--help", action='help', default=argparse.SUPPRESS, help="setting the UI decleration \
	based on input file that should be found in \
	INT over p4 dir path/p4factory/mininet/some_topology.py (e.g.). \
	\n	\t \t	a) for changing the topology read the defaultTopo_with_structural_analysis(README).py . \
	\t \t	b) after change the topology(hosts, nodes, linking and bgp configurs) \
	you should run this script on your topology \
	file(note: this is the file you should run after you set up the INT over p4 program) \
	for changing the UI topology that can be found in \
	https://github.com/p4lang/p4factory/blob/master/apps/int/monitor/client/index.html . \
	\t \t	c) for the INT over p4 - installation \
	guide can be found in https://lccn-cs.atlassian.net/wiki/display/KB/How-to+articles (permissions are necessary).")

	def is_valid_file(parser, arg):
		if not os.path.exists(arg):
			parser.error("The file %s does not exist!" % arg)
		else:
			return open(arg, 'r')  # return an open file handle
	parser.add_argument("-f", "--file", dest="filename", required=True,
						help="input topology file - python file that should be found in p4factory/mininet directory", metavar="FILE", type=lambda x: is_valid_file(parser, x))
	
	#parser.add_argument('-set', action='store_true',  help="set the topology of index.html. \n")

	args = parser.parse_args()

#	if (args.set):
#		if (not sys.argv[2].endswith(".txt")):
#			print "wrong type of file"
#			return

	setTopo(sys.argv[2])

	return
		
if __name__ == "__main__":
    main()

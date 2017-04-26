#!/usr/bin/python
# Copyright 2015-present Barefoot Networks, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#this topologe file need to be saved in your INT over p4 program p4factory/mininet directory : <INT over p4 dir path>/p4factory/mininet.
import argparse
import sys
import os
import math
from decimal import Decimal

from int_cfg import *

#for learning more about the net configuration you can see also:
# - https://github.com/p4lang/p4factory/blob/master/mininet/int_cfg.py
# - http://mininet.org/

def run_cfg(model_dir):
# This is the class configuration for the INT over p4 program that her installation 
# guide can be found in https://lccn-cs.atlassian.net/wiki/display/KB/How-to+articles (permissions are necessary).
# the topology described below is the default one.
# NOTES:
# a) pay attention to white spaces - they are built according to a 
# 	certain legality in the script : setTopo4UI.py - for updating the UI topology.
# b) for each topology change the bgp configuration files for each switch must change accordingly.
# c) model_dir - installations dir.
# d) for changing the topology change sections 1 and 2 under the regulations.
# e) for change the system packeting chang section 3.
# f) for linking switch and host you can see also https://github.com/p4lang/p4factory/blob/master/mininet/int_cfg.py -
#	- configHostRoutesAndArp - line 227




#######################
# -1- vxlan & hosts definition
#######################

# -1.1- default vxlan settings
  vxlan_id = 10
  vxlan_group = '239.0.0.10'
  vxlan_mtu = 1300

# -1.2- config vxlan for hosts
  h1_vxlan_cfg = VxlanConfig( vxlan_id, vxlan_group, '10.2.1.1', 24, '00:11:22:33:44:51', vxlan_mtu  )
  h2_vxlan_cfg = VxlanConfig( vxlan_id, vxlan_group, '10.2.1.2', 24, '00:11:22:33:44:52', vxlan_mtu  )
  h3_vxlan_cfg = VxlanConfig( vxlan_id, vxlan_group, '10.2.1.3', 24, '00:11:22:33:44:53', vxlan_mtu  )
  h4_vxlan_cfg = VxlanConfig( vxlan_id, vxlan_group, '10.2.1.4', 24, '00:11:22:33:44:54', vxlan_mtu  )

# -1.3- config hosts and set up the vxlan_cfg for each host
# -1.3.1- e.g. for host h1 the vxlan_cfg get h1_vxlan_cfg that defined above
  host_cfgs = {
    'h1' : HostConfig( name = 'h1', mac = '00:c0:a0:a0:00:01', ip = '10.0.1.1', prefix_len = 24, vxlan_cfg = h1_vxlan_cfg ), 
    'h2' : HostConfig( name = 'h2', mac = '00:c0:a0:a0:00:02', ip = '10.0.2.2', prefix_len = 24, vxlan_cfg = h2_vxlan_cfg ),
    'h3' : HostConfig( name = 'h3', mac = '00:c0:a0:a0:00:03', ip = '10.0.3.3', prefix_len = 24, vxlan_cfg = h3_vxlan_cfg ),
    'h4' : HostConfig( name = 'h4', mac = '00:c0:a0:a0:00:04', ip = '10.0.4.4', prefix_len = 24, vxlan_cfg = h4_vxlan_cfg )
  }

#######################
# -2- linking & nodes definition
####################### 
  
# -2.1- config each switch ports for hosts

# NOTE : for linking switch and host you can see also https://github.com/p4lang/p4factory/blob/master/mininet/int_cfg.py -
# - configHostRoutesAndArp - line 227

# -2.1.1- leaf1 ports for hosts h1 and h2 as you can see at link configs below
  leaf1_port_cfgs = [
    PortConfig( port_no = 0, ip = '10.0.1.100', prefix_len = 24, mac = '00:01:00:00:00:01' ),
    PortConfig( port_no = 1, ip = '10.0.2.100', prefix_len = 24, mac = '00:01:00:00:00:02' ),
  ] 

# -2.1.2- leaf2 ports for hosts h3 and h4 as you can see at link configs below 
  leaf2_port_cfgs = [
    PortConfig( port_no = 0, ip = '10.0.3.100', prefix_len = 24, mac = '00:02:00:00:00:01' ),
    PortConfig( port_no = 1, ip = '10.0.4.100', prefix_len = 24, mac = '00:02:00:00:00:02' ),
  ]

# -2.2- switch configs
# -2.2.1- note the topology orgenized the switches as leafs and spines
# -2.2.2- a) name - name of the switch
# -2.2.3- b) port_cfgs - ports for hosts as describe in 2.1
# -2.2.4- c) swapi_port - api port - note that the ports are different for each switch
# -2.2.4- d) bmcli_port - cli port - note that the ports are different for each switch
# -2.2.4- e) config_fs - path for bgp configuration - NOTE: 
#	FOR EACH TOPOLOGY CHANGE THE BGP CONFIGURATION FILES, FOR EACH SWITCH, MUST CHANGE ACCORDINGLY
#	you should change ,e.g. for leaf 1 : 
#		https://github.com/p4lang/p4factory/blob/master/mininet/configs/leaf1/l3_int_ref_topo/startup_config.sh
#		https://github.com/p4lang/p4factory/blob/master/mininet/configs/leaf1/l3_int_ref_topo/quagga/bgpd.conf
# -2.2.5- f) model_dir - the model dir which the class generate.
# -2.2.6- g) switch_id - the value of the id increase for each switch. leafs(A) and spine(B) separately.
#	NOTE: switch_id value is an hex number(0x...). 

  switch_cfgs = [
    SwitchConfig( name       = 'leaf1', 
                  port_cfgs  = leaf1_port_cfgs,
                  swapi_port = 26000,
		  bmcli_port = 27000,
                  config_fs  = 'configs/leaf1/l3_int_ref_topo',
		  model_dir  = model_dir,
                  switch_id  = 0x000000A1, pps=400, qdepth=15 ),
    SwitchConfig( name       = 'leaf2',
                  port_cfgs  = leaf2_port_cfgs,
                  swapi_port = 26001,
                  bmcli_port = 27001,
                  config_fs  = 'configs/leaf2/l3_int_ref_topo',
                  model_dir  = model_dir,
                  switch_id  = 0x000000A2, pps=400, qdepth=15 ),
    SwitchConfig( name       = 'spine1',
                  port_cfgs  = [],
                  swapi_port = 26002,
                  bmcli_port = 27002,
                  config_fs  = 'configs/spine1/l3_int_ref_topo',
                  model_dir  = model_dir,
                  switch_id  = 0x000000B1, pps=400, qdepth=15 ),
    SwitchConfig( name       = 'spine2',
                  port_cfgs  = [],
                  swapi_port = 26003,
                  bmcli_port = 27003,
                  config_fs  = 'configs/spine2/l3_int_ref_topo',
                  model_dir  = model_dir,
                  switch_id  = 0x000000B2, pps=400, qdepth=15 ),
  ]
  
# -2.3- link configs
# -2.3.1- for linking switch and host you should note only the switch port number as define in 2.1
# NOTE : for linking switch and host you can see also https://github.com/p4lang/p4factory/blob/master/mininet/int_cfg.py -
# - configHostRoutesAndArp - line 227
# -2.3.2- for linking 2 switches note for each the designated port(index) for the connection which does not appear in 2.1

  link_cfgs = [
    LinkConfig( 'leaf1', 'h1', 0 ),
    LinkConfig( 'leaf1', 'h2', 1 ),
    LinkConfig( 'leaf1', 'spine1', 2, 0 ),
    LinkConfig( 'leaf1', 'spine2', 3, 0 ),

    LinkConfig( 'leaf2', 'h3', 0 ),
    LinkConfig( 'leaf2', 'h4', 1 ),
    LinkConfig( 'leaf2', 'spine1', 2, 1 ),
    LinkConfig( 'leaf2', 'spine2', 3, 1 ),
  ]

#######################
# -3- system set up
#######################

  mgr = NetworkManager( host_cfgs.values(), switch_cfgs, link_cfgs )
  net = mgr.setupAndStartNetwork()

# -3.1- starting ping commnds

  h1 = net.get('h1')
  h2 = net.get('h2')
  h3 = net.get('h3')
  h4 = net.get('h4')

  h1.cmd("iperf -s &")
  h2.cmd("iperf -s &")
  h3.cmd("iperf -s &")
  h4.cmd("iperf -s &")

  # TODO: start iperf clients
  h1.cmd("iperf -c 10.2.1.4 -t 3000 > /dev/null &")
  h3.cmd("iperf -c 10.2.1.2 -t 3000 > /dev/null &")

# -3.2- starting the cli for mininet
  CLI(net)

  mgr.cleanup()
  net.stop()

#running the INT over p4 program by this script
parser = argparse.ArgumentParser(prog='setTopology', add_help=False)
parser.add_argument("-h", "--help", action='help', default=argparse.SUPPRESS, help="1) for initial the INT over p4 program run the \
	script as follows: eg: sudo ./some_topology.py --model-dir=$INSTALL_DIR  \
	\t \t \t \t 2) for changing the topology read the file comments, after change the topology and config the BGP as well you \
	can set up the UI, BEFORE you run the program as describe in 1, by running setTopo4UI.py script on your topology file.    \
	NOTES for topology change: \
	a) pay attention to white spaces - they are built according to a \
		certain legality in the script : setTopo4UI.py - for updating the UI topology.    \
	b) for each topology change the bgp configuration files, for each switch, must change accordingly.    \
	c) model_dir - installations dir.    \
	d) for changing the topology change sections 1 and 2 in defaultTopo_with_structural_analysis(README).py \
	under the regulations.    \
	e) for change the system packeting chang section 3 in defaultTopo_with_structural_analysis(README).py.    \
	f) for linking switch and host you can see also https://github.com/p4lang/p4factory/blob/master/mininet/int_cfg.py - \
		- configHostRoutesAndArp - line 227.")
parser.parse_args()
args = sys.argv
if len(args) < 2:
    print('Too few arguments. For running INT over p4 run the script as follows:')
    print('eg: sudo ./%s --model-dir=$INSTALL_DIR' %
          os.path.basename(__file__))
    exit(1)

if '--model-dir' in args[1]:
    model_dir = args[1].split("=")[1]
#elif '-h' in args[1]:
#	exit(1)
else:
    print('Invalid format. Run the script as follows:')
    print('eg: sudo ./%s --model-dir=$INSTALL_DIR' %
          os.path.basename(__file__))
    exit(1)

model_dir = os.path.join(model_dir, 'bin')

# cleanup from previous run
os.system('./int_cleanup.sh > /dev/null 2>&1')
run_cfg(model_dir)
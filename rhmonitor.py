# rhmonitor  for rhminer 0.92 by secures
#------------------------------------------------------------------------------

# User settings
#------------------------------------------------------------------------------

# List of ips to check for data
IP_LIST = ["localhost", "192.168.1.40", "192.168.1.178", "192.168.1.173", "192.168.1.93"]

# Port of 
PORT = 7111
REFRESH_INTERVAL = 5

#General settings
#------------------------------------------------------------------------------

NAME = "rhmonitor"
VERSION = "0.1b"

# Weight of each sample for total hashrate calculation
SAMPLE_WEIGHT = 0.02

# Network timeout
NETWORK_TIMEOUT = 5



# Program
#------------------------------------------------------------------------------	
import socket
import json
import os
import time

def printHeader():
  os.system ( 'cls' )
  print "--------------------------------------------------------------------------------"
  print " {0} {1} for rhminer 0.92 ".format(NAME, VERSION)
  print "--------------------------------------------------------------------------------\n"
  
def printMinerStatus ( status ):
  hs = 0
  ip = status['ip']
  if 'infos' in status:
    uptime = status['uptime']
    server = status['stratum.server']
    shares = status['accepted']
    for info in status['infos']:
      hs += info['speed']
    print(" {0}\t {1} h/s\ts: {2}\t up: {3}\t{4}".format(ip, hs, shares, uptime, server))
  else:
    print(" {0}\t --- h/s\ts: -\t up: ---\toffline ".format(ip))
  return hs

movingavg = 0;
while 1:
  jsonData = []
  for ip in IP_LIST:
    try:
      client = socket.socket ( socket.AF_INET, socket.SOCK_STREAM )
      client.settimeout ( NETWORK_TIMEOUT )
      client.connect ( ( ip, PORT ) )
      client.send ( "POST" )
      data = json.loads ( client.recv ( 4096 ) )
      client.close()
    except:
	  data = json.loads ( "{}" )
    data['ip'] = ip
    jsonData.append ( data )
  
  printHeader()
  
  hashrate = 0	
  for status in jsonData: 
    hashrate += printMinerStatus ( status )
  movingavg = ( 1 - SAMPLE_WEIGHT ) * movingavg + SAMPLE_WEIGHT * hashrate
  print "\n--------------------------------------------------------------------------------\n"
  print(" Total hashrate {0} h/s ({1} h/s)".format(hashrate, round ( movingavg ) ) )
  time.sleep ( REFRESH_INTERVAL )
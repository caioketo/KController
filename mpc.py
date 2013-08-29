import sys
import time
import telnetlib
import subprocess
import ConfigParser

def sysCmd(cmd):
	p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
	(output, err) = p.communicate()
	return output

def telnetCmd(cmd):
    mpdHost = 'localhost'
    mpdPort = 6600
    tn = telnetlib.Telnet(mpdHost, mpdPort)
    tn.read_until('OK MPD 0.16.0')
    tn.write(cmd + "\n")
    result = tn.read_until('OK', 10)
    tn.close()
    return result

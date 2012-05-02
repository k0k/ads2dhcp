#!/usr/bin/env python 
"""
Just a simple MS Network Shell (netsh) Tool convert format to Linux dhcp ISC format.
Copyright (C) 2008 Wilmer Jaramillo M. <wilmer@fedoraproject.org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>

Command line options:
-f |--file              file with names and ips/mac address.
-h |--help              show help.

The steps to run in Windows 2000/2003 Advanced Server are:
1.- C:\> net stop dhcpserver
2.- C:\> netsh dhcp server dump >> dhcp-dump.txt
3.- C:\> find "Add reservedip" dhcp-dump.txt >> dhcp.csv
	the output find format should be:
Dhcp Server 130.1.10.180 Scope 130.1.0.0 Add reservedip 130.1.12.15 0001e66c2a60 "info15 "" "DHCP"
4.- python ads2dhcp.py -f dhcp.csv

The output after of run this script is a compatible dhcpd.conf file:
host info15 { /* Host Name
hardware ethernet 00:01:e6:6c:2a:60; /* NIC MAC address */
fixed-address 130.1.12.15; /* IP address */
}

This program can be distributed under the GNU GPL
(http://www.gnu.org/licenses/gpl.html)

"""

import os, sys, getopt

__version__ = "0.1"
__copyright__ = "Wilmer Jaramillo M."
__date__ = "(#) Aug 11 2008"
__license__ = "GNU General Public License (GPL)"
copyright = "Version %s / %s, %s / %s" % (__version__, __copyright__, __date__,__license__)

dumpConfig = ""
def usage():
        print '%s %s' % (os.path.basename(sys.argv[0]),copyright)
        print 'Usage: %s -f[--file] -h[--help]'  % os.path.basename(sys.argv[0])
        sys.exit(0)
def files_check():
        if dumpConfig == '':
                usage()
        if not os.path.isfile(dumpConfig):
                print '[-] the dump dhcp windows file %s not exist' % dumpConfig

try:
        opts, args = getopt.getopt(sys.argv[1:], "hf:", ["help", "file="])
except getopt.GetoptError:
        usage()
        sys.exit(1)
for o, a in opts:
        if o in ("-h", "--help"):
                usage()
                sys.exit(0)
        if o in ("-f", "--file"):
                dumpConfig = a

files_check()
for line in open(dumpConfig):
	mac_raw=[]
	mac_format = ""
	ip = line.split(" ")[7]
	mac = line.split(" ")[8]
	name = line.split(" ")[9]
	for i in range(0, 11, 2):
		mac_raw = mac_raw + list(mac)[i:i+2]
		if i < 10:
			mac_raw.append(":")
	mac_format = "".join(mac_raw)
	print "host %s {" % name
	print "hardware ethernet %s;" % mac_format
	print "fixed-address %s;" % ip
	print "}\n"

# vim: set nowrap nu foldmethod=marker:


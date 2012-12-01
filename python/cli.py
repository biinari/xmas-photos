#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Command Line Interface to Bowley Christmas Experience
import os
import sys
import devices
from devices.device import Device
import process
import calendar

def main(calendar=False):
    def cli_log(x):
        print x
	tools.Logger.setCallback(cli_log)
	if calendar:
		calendar.run()
	else:
		process.run()

if __name__ == "__main__":
	if len(sys.argv) > 1:
		calendar = (re.match('^cal.*', sys.argv[1], re.I) != None)
	main()

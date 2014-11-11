#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Command Line Interface to Bowley Christmas Experience
import re
import sys
import process
import calendar
import tools

def main(use_calendar=False):
    def cli_log(message):
        print message

    tools.Logger.setCallback(cli_log)
    if use_calendar:
        calendar.run()
    else:
        process.run()

def run():
    if len(sys.argv) > 1:
        use_calendar = (re.match('^cal.*', sys.argv[1], re.I) != None)
    main(use_calendar)

if __name__ == "__main__":
    run()

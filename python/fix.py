#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Fix-up photos for Bowley Christmas Experience
import os

from process import Process
import tools

def run():
    names = os.listdir('infiles/')
    names.sort()
    for infile in names:
        day = tools.get_day()
        timeid = day + '/' + raw_input('Time id: ')
        group_name = raw_input('Group name: ')
        #timeid = time.strftime('%a/%H%M%S', time.localtime())
        Process.process(infile, group_name, timeid)
        os.rename('infiles/' + infile,
                  'outfiles/{}_{}.jpg'.format(timeid, group_name.replace(' ', '_')))
    print 'Finished.'

if __name__ == "__main__":
    run()

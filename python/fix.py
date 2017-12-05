#!/usr/bin/env python2
# vim: set fileencoding=utf-8 :
# Fix-up photos for Bowley Christmas Experience
import os

from process import Process
import tools

def run():
    names = os.listdir('infiles')
    names.sort()
    for infile in names:
        day = tools.get_day()
        timeid = raw_input('Time id: ')
        group_name = raw_input('Group name: ')
        #timeid = time.strftime('%H%M%S', time.localtime())
        day_timeid = day + '/' + timeid
        Process.process(infile, group_name, day_timeid)
        outfile_name = '{}_{}.jpg'.format(timeid, tools.safe_filename(group_name))
        os.rename(os.path.join('infiles', infile),
                  os.path.join('outfiles', day, outfile_name))
    print 'Finished.'

if __name__ == "__main__":
    run()

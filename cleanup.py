#!/usr/bin/env python
'''
Copyright 2015 Yash Chitalia

This file is part of Sentinel.

Sentinel is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sentinel is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Sentinel.  If not, see <http://www.gnu.org/licenses/>.
'''
import os
import ConfigParser
import subprocess as sp
import datetime

config = ConfigParser.RawConfigParser()
config.read('/etc/sentinel/sentinel_configure.cfg')
archive_directory = config.get('General_configure', 'archive_dir')
pics_directory = config.get('General_configure', 'motion_dir')
current_intrusion_datetime = datetime.datetime.now()

def main():
    '''Move all pics of new intrusion to archive folder'''
    os.mkdir(archive_directory+'/COMPLETE_LOG_'+str(current_intrusion_datetime))
    pics = [f for f in os.listdir(pics_directory)]
    print pics
    for p in pics:
        try:
            os.rename(pics_directory+'/'+p, archive_directory+'/COMPLETE_LOG'+str(current_intrusion_datetime)+'/'+p) 
        except:
            print "Couldn't copy pic:{}. Deleting.".format(p)
            sp.check_output(['sudo', 'rm' , pics_directory+'/'+p])
            continue
if __name__ == '__main__':
    main()

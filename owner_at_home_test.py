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
import ConfigParser
import pickle as pkl
import subprocess as sp
from galileo.dongle import FitBitDongle
from galileo.tracker import FitbitClient
from galileo.utils import a2x
import uuid
import time


config = ConfigParser.RawConfigParser()
config.read('/etc/sentinel/sentinel_configure.cfg')
owner_test_type = (config.get('Network', 'owner_test_type'))#Can be either "FITBIT" or "PHONE_IP"
ip_address = config.get('Network', 'ip_address')
fitbit_tracker_id = config.get('Network', 'fitbit_tracker_id')
SIZE_OF_CHECK_BUFFER = 10
try:
    check_buffer = pkl.load(open("/home/pi/sentinel/at_home.p", "rb"))
    if len(check_buffer) < SIZE_OF_CHECK_BUFFER:
        raise IndexError('Buffer List Size too small. Creating new buffer')
except:
    check_buffer = [True]*(SIZE_OF_CHECK_BUFFER/2) + [False]*(SIZE_OF_CHECK_BUFFER/2)

def main():
    networks = ' '
    if owner_test_type == 'PHONE_IP':
        print 'Imters'
        for i in range(10):
            networks = sp.check_output(['sudo', 'arp-scan', '-interface', 'wlan0', '--localnet'])
            if ip_address in networks:
                check_buffer.append(True)
                check_buffer.pop(0)
                pkl.dump(check_buffer, open("/home/pi/sentinel/at_home.p", "wb"))
                return
            else:
                continue
        check_buffer.append(False)
        check_buffer.pop(0)
        pkl.dump(check_buffer, open("/home/pi/sentinel/at_home.p", "wb"))
    elif owner_test_type == 'FITBIT':
        for i in range(3):
            check_for_fitbit()#Do a check
            time.sleep(16)
    else:
        print owner_test_type

def check_for_fitbit():
    '''This method will check if a FITBIT device of the ID given in the config file 
    is present in the vicinity. If so, it will write a True to the at_home pkl file'''
    dongle = FitBitDongle()
    dongle.setup()
    fitbit = FitbitClient(dongle)
    FitBitUUID = uuid.UUID('{ADAB0000-6E7D-4601-BDA2-BFFAA68956BA}')
    for tracker in fitbit.discover(FitBitUUID):
        tracker_id =  a2x(tracker.id)
        if tracker_id == fitbit_tracker_id:
            check_buffer.append(True)
            check_buffer.pop(0)
            pkl.dump(check_buffer, open("/home/pi/sentinel/at_home.p", "wb"))
            return
        else:
            continue
    check_buffer.append(False)
    check_buffer.pop(0)
    pkl.dump(check_buffer, open("/home/pi/sentinel/at_home.p", "wb"))


if __name__ == '__main__':
    main()

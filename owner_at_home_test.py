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

config = ConfigParser.RawConfigParser()
config.read('/etc/sentinel/sentinel_configure.cfg')
owner_test_type = (config.get('Network', 'owner_test_type'))#Can be either "FITBIT" or "PHONE_IP"
ip_address = config.get('Network', 'ip_address')
fitbit_tracker_id = config.get('Network', 'fitbit_tracker_id')

def main():
    networks = ' '
    if owner_test_type == 'PHONE_IP':
        print 'Imters'
        for i in range(10):
            networks = sp.check_output(['sudo', 'arp-scan', '-interface', 'wlan0', '--localnet'])
            if ip_address in networks:
                pkl.dump(True, open("/home/pi/sentinel/at_home.p", "wb"))
                return
            else:
                continue
        pkl.dump(False, open("/home/pi/sentinel/at_home.p", "wb"))
    elif owner_test_type == 'FITBIT':
        print 'AM testing with FITBIT'
        dongle = FitBitDongle()
        dongle.setup()
        fitbit = FitbitClient(dongle)
        FitBitUUID = uuid.UUID('{ADAB0000-6E7D-4601-BDA2-BFFAA68956BA}')
        print fitbit_tracker_id
        for tracker in fitbit.discover(FitBitUUID):
            tracker_id =  a2x(tracker.id)
            if tracker_id == fitbit_tracker_id:
                pkl.dump(True, open("/home/pi/sentinel/at_home.p", "wb"))
                print 'Owner at home'
                return
            else:
                continue
        print 'OWNER NOT FOUND.'
        pkl.dump(False, open("/home/pi/sentinel/at_home.p", "wb"))
    else:
        print owner_test_type



if __name__ == '__main__':
    main()

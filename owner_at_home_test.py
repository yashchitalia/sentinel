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


config = ConfigParser.RawConfigParser()
config.read('/etc/sentinel/sentinel_configure.cfg')
ip_address = config.get('Network', 'ip_address')

def main():
    networks = ' '
    for i in range(10):
        networks = sp.check_output(['sudo', 'arp-scan', '-interface', 'wlan0', '--localnet'])
        if ip_address in networks:
            pkl.dump(True, open("owner_at_home.p", "wb"))
            return
        else:
            continue
    pkl.dump(False, open("owner_at_home.p", "wb"))


if __name__ == '__main__':
    main()

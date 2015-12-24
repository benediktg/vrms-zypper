#!/usr/bin/python3
'''
<one line to give the program's name and a brief idea of what it does.>
Copyright (C) 2015  Benedikt Geißler <benedikt.geissler@openmailbox.org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

@package zypper_vrms
'''
import subprocess
import shlex


class LicenseCheck:
    def __init__(self):
        tmp = shlex.split(shlex.quote('zypper licenses'))
        tmp = subprocess.Popen(tmp, shell=True, stdout=subprocess.PIPE).stdout
        self.text = tmp.read().decode().split('\n', 2)[2].split('-\n')
        self.packages = list()
        self.classification = dict()
        self.free = open('licenses/free.txt').read().split('\n')
        self.proprietary = open('licenses/proprietary.txt').read().split('\n')

    def parse(self):
        for i in self.text:
            t1 = i.strip().split('\n')
            if len(t1) != 2:
                continue
            nam = t1[0].split(' ')[0]
            lic = t1[1].split(': ')[1]
            t1 = (nam, lic)
            self.packages.append(t1)
        for i in self.packages:
            if i[1] not in self.classification:
                self.classification[i[1]] = set([i[0]])
            else:
                self.classification[i[1]].add(i[0])

    def printL(self, key):
        print('{}:'.format(key))
        for value in self.classification[key]:
            print('\t{}'.format(value))
        print()

    def printDT(self):
        for key in self.classification:
            if (key not in self.free) or (key in self.proprietary):
                for i in self.proprietary:
                    if i in key:
                        self.printL(key)
                for i in self.free:
                    if i in key:
                        break
                else:
                    self.printL(key)


def main():
    L = LicenseCheck()
    L.parse()
    L.printDT()

if __name__ == '__main__':
    main()


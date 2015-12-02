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
        self.text = tmp
        self.packages = list()

    def shorten(self):
        tmp = self.text.read().decode()
        tmp = tmp.split('\n', 2)[2]
        self.text = tmp

    def prepare(self):
        tmp = self.text.split('-\n')
        for i in tmp:
            t1 = i.strip().split('\n')
            if len(t1) != 2:
                continue
            nam = t1[0].split(' ')[0]
            lic = t1[1].split(': ')[1]
            t1 = (nam, lic)
            self.packages.append(t1)


def main():
    L = LicenseCheck()
    L.shorten()
    L.prepare()
    print(len(L.packages))

if __name__ == '__main__':
    try:
        main()
    except:
        print('an error occured')

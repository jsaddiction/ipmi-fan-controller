#!/usr/bin/env python3



import configparser
import subprocess
from time import sleep


sdr_type_fan = '''Fan1             | 30h | ok  |  7.1 | 4680 RPM
Fan2             | 31h | ok  |  7.1 | 4680 RPM
Fan3             | 32h | ok  |  7.1 | 4560 RPM
Fan4             | 33h | ok  |  7.1 | 4680 RPM
Fan5             | 34h | ok  |  7.1 | 4680 RPM
Fan6             | 35h | ok  |  7.1 | 4680 RPM
Fan Redundancy   | 75h | ok  |  7.1 | Fully Redundant'''


class Ipmi:

    MANUAL_FAN_CMD = 'raw 0x30 0x30 0x01 0x00'
    AUTO_FAN_CMD = 'raw 0x30 0x30 0x01 0x01'

    def __init__(self, host=None, user=None, password=None):
        self._cmdList = ['ipmitool']
        if host and user and password:
            self._cmdList.extend(['-I', 'lanplus'])
            self._cmdList.extend(['-H', host])
            self._cmdList.extend(['-U', user])
            self._cmdList.extend(['-P', password])

    def sendCmd(self, cmd):
        # cmd example string 'sdr list'
        # returns unformatted response
        commandList = self._cmdList
        commandList.extend([x.strip() for x in cmd.split(' ')])
        print('Sending: {}'.format(commandList))
        result = subprocess.run(commandList, stdout=subprocess.PIPE)

        return result.stdout.decode()

    def getTemp(self):
        # parses returned temp data from IPMI enabled devices
        result = self.sendCmd('sdr type temp')

        maxTemp = 0

        for line in result.splitlines():
            singleTemp = [x.strip() for x in line.split('|')]

            try:
                temp = int(singleTemp[-1].replace('degrees', '').replace('C', '').strip())
            except ValueError:
                continue

            if temp > maxTemp:
                maxTemp = temp

        return maxTemp

    def getFanRPM(self):
        # parses returned fan data from IPMI enabled devices
        result = self.sendCmd('sdr type fan')

        # Start parsing
        rpms = []
        for line in result.splitlines():
            singleFan = [x.strip() for x in line.split('|')]
            try:
                rpms.append(int(singleFan[-1].replace('RPM', '').strip()))
            except ValueError:
                pass

        totalRpm = 0
        for rpm in rpms:
            totalRpm += rpm

        return totalRpm / len(rpms)

    def setManualFans(self):
        pass

    def setFanSpeed(self, dutyCycle):
        pass
class FanControl:
    # Constants
    MANUAL_FAN_CMD = 'raw 0x30 0x30 0x01 0x00'
    AUTO_FAN_CMD = 'raw 0x30 0x30 0x01 0x01'


if __name__ == '__main__':
    # cooling = FanControl()
    # print(cooling.fanLabels)
    ipmi = Ipmi('192.168.0.7', 'justin', 'Redflyer1!')
    # ipmi.getTemp()
    print(ipmi.getFanRPM())
    # ipmi.sendCmd('sdr list')
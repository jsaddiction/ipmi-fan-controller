#!/usr/bin/env python3



import configparser
import subprocess
from time import sleep

sdr_list = '''Temp             | disabled          | ns
    Ambient Temp     | 30 degrees C      | ok
    Planar Temp      | disabled          | ns
    CMOS Battery     | 0x00              | ok
    ROMB Battery     | Not Readable      | ns
    VCORE            | 0x00              | ok
    0.75 CPU VTT PG  | 0x00              | ok
    1.8V PG          | 0x00              | ok
    3.3V PG          | 0x00              | ok
    PSU PG           | 0x00              | ok
    5V Riser1 PG     | 0x00              | ok
    MEM CPU FAIL     | 0x00              | ok
    VTT CPU FAIL     | 0x00              | ok
    1.8 PLL CPU PG   | 0x00              | ok
    1.2 LOM FAIL     | 0x00              | ok
    1.05V PG         | 0x00              | ok
    1.2 AUX FAIL     | 0x00              | ok
    Heatsink Pres    | 0x00              | ok
    iDRAC6 Ent PRES  | 0x00              | ok
    USB Cable Pres   | 0x00              | ok
    Riser1 Pres      | 0x00              | ok
    FAN 1 RPM        | 3600 RPM          | ok
    FAN 2 RPM        | 3720 RPM          | ok
    FAN 3 RPM        | 3600 RPM          | ok
    PFault Fail Safe | Not Readable      | ns
    Presence         | 0x00              | ok
    Status           | 0x00              | ok
    Status           | 0x00              | ok
    OS Watchdog      | 0x00              | ok
    SEL              | Not Readable      | ns
    Intrusion        | 0x00              | ok
    CPU Temp Interf  | Not Readable      | ns
    iDRAC6 Upgrade   | Not Readable      | ns
    vFlash           | 0x00              | ok
    DKM Status       | 0x00              | ok
    ECC Corr Err     | Not Readable      | ns
    ECC Uncorr Err   | Not Readable      | ns
    I/O Channel Chk  | Not Readable      | ns
    PCI Parity Err   | Not Readable      | ns
    PCI System Err   | Not Readable      | ns
    SBE Log Disabled | Not Readable      | ns
    Logging Disabled | Not Readable      | ns
    Unknown          | Not Readable      | ns
    CPU Protocol Err | Not Readable      | ns
    CPU Bus PERR     | Not Readable      | ns
    CPU Init Err     | Not Readable      | ns
    CPU Machine Chk  | Not Readable      | ns
    Memory Spared    | Not Readable      | ns
    Memory Mirrored  | 0x00              | ok
    Memory RAID      | Not Readable      | ns
    Memory Added     | Not Readable      | ns
    Memory Removed   | Not Readable      | ns
    Memory Cfg Err   | 0x00              | ok
    Mem Redun Gain   | Not Readable      | ns
    PCIE Fatal Err   | 0x00              | ok
    Chipset Err      | 0x00              | ok
    Err Reg Pointer  | 0x00              | ok
    Mem ECC Warning  | Not Readable      | ns
    Mem CRC Err      | Not Readable      | ns
    USB Over-current | 0x00              | ok
    POST Err         | 0x00              | ok
    Hdwr version err | Not Readable      | ns
    Mem Overtemp     | 0x00              | ok
    Mem Fatal SB CRC | Not Readable      | ns
    Mem Fatal NB CRC | Not Readable      | ns
    OS Watchdog Time | Not Readable      | ns
    Non Fatal PCI Er | Not Readable      | ns
    Fatal IO Error   | Not Readable      | ns
    MSR Info Log     | Not Readable      | ns
    Temp             | disabled          | ns
    '''

sdr_type_fan = '''Fan1             | 30h | ok  |  7.1 | 4680 RPM
Fan2             | 31h | ok  |  7.1 | 4680 RPM
Fan3             | 32h | ok  |  7.1 | 4560 RPM
Fan4             | 33h | ok  |  7.1 | 4680 RPM
Fan5             | 34h | ok  |  7.1 | 4680 RPM
Fan6             | 35h | ok  |  7.1 | 4680 RPM
Fan Redundancy   | 75h | ok  |  7.1 | Fully Redundant
'''
sdr_type_fan2 = '''FAN 1 RPM        | 30h | ok  |  7.1 | 3600 RPM
FAN 2 RPM        | 31h | ok  |  7.1 | 3720 RPM
FAN 3 RPM        | 32h | ok  |  7.1 | 3600 RPM'''
class Ipmi:
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

    def getFans(self):
        # parses returned fan data from IPMI enabled devices
        # cmd = 'sdr type fan'
        # result = sendCmd(cmd)
        result = sdr_type_fan

        # Start parsing
        fans = {}
        for line in result.splitlines():
            singleFan = [x.strip() for x in line.split('|')]
            try:
                fans[singleFan[0]] = int(singleFan[-1].replace('RPM', '').strip())
            except ValueError:
                pass

        print(fans)

class FanControl:
    # Constants
    MANUAL_FAN_CMD = 'raw 0x30 0x30 0x01 0x00'
    AUTO_FAN_CMD = 'raw 0x30 0x30 0x01 0x01'
    
    # ipmitool -I lanplus -H <iDRAC-IP> -U <iDRAC-USER> -P <iDRAC-PASSWORD> sensor reading "Ambient Temp" "FAN 1 RPM" "FAN 2 RPM" "FAN 3 RPM"

    def __init__(self, host=None, user=None, password=None):
        self.fanSpeed = 0
        self.cpuTemp = 0
        self.fanLabels = self._getFans()
        if host and user and password:
            self.ipmiPreamble = 'ipmitool -I lanplus -H {} -U {} -P {} '.format(host, user, password)
        else:
            self.ipmiPreamble = 'ipmitool '

    def _sendIpmiCMD(self, cmd):
        pass

    def _getFanSpeed(self):
        pass

    def _getCpuTemp(self):
        pass

    def _setFanSpeed(self, dutyCycle=100):
        pass

    def _setFanMode(self, auto=True):
        pass

    def _getFans(self):
        # Get all fan labels from ipmitool 'sdr list' command
        sensorList = sdr_list.splitlines()
        fanList = []
        for item in sensorList:
            if 'fan' in item.lower():
                fanList.append(item.split('|')[0].strip())
        return fanList


if __name__ == '__main__':
    # cooling = FanControl()
    # print(cooling.fanLabels)
    ipmi = Ipmi('192.168.0.7', 'justin', 'Redflyer1!')
    ipmi.getFans()
    # ipmi.sendCmd('sdr list')
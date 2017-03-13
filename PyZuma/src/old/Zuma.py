#!./bin/python
import sys
from bluepy.btle import Peripheral, BTLEException, DefaultDelegate
from ZumaMonitor import ZumaMonitor


class Zuma():
    def __init__(self, addr):
        try:
            self.device = Peripheral(addr)
        except BTLEException:
            print('Non trovo Zuma!')
            self.device = False
        if(self.device is not False):
            self.comm = self.device.getCharacteristics(uuid='0000ffe1-0000-1000-8000-00805f9b34fb')[0]


class ZumaBtNotify(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.pkt = None

    def handleNotification(self, cHandle, data):
        self.pkt = data.decode()


# Fa qualcosa quando cambiano le velocità
def updateSpeeds(speeds):
    # print(str(int(speeds[0])) + ' ' + str(int(speeds[1])))
    # pk = zuma.Slip.encode(str(int(speeds[0])) + ' ' + str(int(speeds[1])))
    # zuma.Slip.append(pk.encode(encoding='latin1'))
    # print(zuma.Slip.decode())
    # zuma.comm.write(pk.encode(encoding='latin1'))
    # Formato pacchetto: "leftspeed rightspeed>" 192 (C0) and 219 (DB)
    zuma.comm.write(str.encode('SP ' + str(int(speeds[0])) + ' ' + str(int(speeds[1])) + ">"))


monitor = ZumaMonitor()
monitor.handleSpeeds(updateSpeeds)
rcv = ZumaBtNotify()

zuma = Zuma(addr='5c:f8:21:88:26:84')

if(zuma.device is not False):
    zuma.device.withDelegate(rcv)

while monitor.running:
    if(zuma.device is not False):
        if zuma.device.waitForNotifications(0.001):  # Il temout non ho idea a quanto metterlo, ora è 0.001 sec
            if(rcv.pkt[:3] == 'US '):
                _us = rcv.pkt[3:].split(' ')
                print(_us[1])
                if int(_us[1]) > 0 and int(_us[1]) < 15:
                    zuma.comm.write(str.encode("SP 0 0>"))
                    monitor.force_stop = True
                    print("STOOOOP")
                else:
                    monitor.force_stop = False
            continue
    monitor.run()


monitor.quit()

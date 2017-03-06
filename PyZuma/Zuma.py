#!./bin/python
from bluepy.btle import Peripheral, BTLEException
from ZumaMonitor import ZumaMonitor
from ZumaBtNotify import ZumaBtNotify


class Zuma():

    def __init__(self, addr):
        try:
            self.device = Peripheral(addr)
        except BTLEException:
            print('Non trovo Zuma!')
            self.device = False


def updateSpeeds(speeds):
    print(speeds[0])
    print(speeds[1])


monitor = ZumaMonitor()
monitor.handleSpeeds(updateSpeeds)
# zuma = Zuma(addr='5c:f8:21:88:26:84')

# if(zuma.device):
#     zuma.setDelegate(ZumaBtNotify("false"))

while monitor.running:
    monitor.run()

monitor.quit()

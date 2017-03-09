from bluepy.btle import Peripheral, ADDR_TYPE_RANDOM


class HM10(Peripheral):
    def __init__(self, addr):
        Peripheral.__init__(self, addr, addrType=ADDR_TYPE_RANDOM)


per = Peripheral('5c:f8:21:88:26:84')
services = per.getServices()

for service in services:
    characteristics = service.getCharacteristics()
    for characteristic in characteristics:
        print('UUID: ' + str(characteristic.uuid))
        print('- ' + characteristic.propertiesToString())
        if characteristic.supportsRead() is True:
            print('- ' + str(characteristic.supportsRead()))
            print('- ' + str(characteristic.read()))
            print('--- --- ---')

# main_uuid = UUID()
char_main = per.getCharacteristics(uuid='0000ffe1-0000-1000-8000-00805f9b34fb')[0]
msg = "Suca"
char_main.write(str.encode(msg))

from bluepy.btle import Peripheral, DefaultDelegate
import time
import random


class MyDelegate(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)
        # ... initialise here

    def handleNotification(self, cHandle, data):
        # ... perhaps check cHandle
        # ... process 'data'
        print(data)


p = Peripheral('5c:f8:21:88:26:84')
p.setDelegate(MyDelegate("false"))
com = p.getCharacteristics(uuid='0000ffe1-0000-1000-8000-00805f9b34fb')[0]
# random.randrange(0, 100)
# Setup to turn notifications on, e.g.
#   svc = p.getServiceByUUID( service_uuid )
#   ch = svc.getCharacteristics( char_uuid )[0]
#   ch.write( setup_data )

# Main loop --------

while True:
    left = str(random.randint(0, 100))
    right = str(random.randint(0, 100))
    packet = "10 " + left + " " + right + " 0>"
    com.write(str.encode(packet))
    # if p.waitForNotifications(1.0):
    #    z\handleNotification() was called
    #    continue

    time.sleep(0.2)
    # Perhaps do something else here

from bluepy.btle import DefaultDelegate


class ZumaBtNotify(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(data)

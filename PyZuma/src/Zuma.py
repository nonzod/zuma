import os, time
import pygame as py
from bluepy.btle import Peripheral, BTLEException, DefaultDelegate
from ZumaCam import ZumaCam
from ZumaEvents import ZumaEvents

WIDTH = 1280  # width of our game window
HEIGHT = 720  # height of our game window
FPS = 25  # frames per second
POS_CONTROLS = (800, 90)
# Colors (R, G, B)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (120, 120, 120)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Zuma:
    __dir = os.getcwd()
    __labels = {}

    def __init__(self, addr):
        self.running = False
        try:
            self.device = Peripheral(addr)
        except BTLEException:
            print('Non trovo Zuma!')
            self.device = False
        if(self.device is not False):
            self.comm = self.device.getCharacteristics(uuid='0000ffe1-0000-1000-8000-00805f9b34fb')[0]

    def _initialize(self):
        py.init()
        py.display.set_caption("Zuma Control")
        # Initialise time and delta time variables
        self.clock = py.time.Clock()
        self.start_time = py.time.get_ticks()
        self.delta_time = 0
        self.elapsed_time = 0
        self.scene_elapsed_time = 0
        # Main Display
        self.display = py.display.set_mode((WIDTH, HEIGHT), py.DOUBLEBUF)  # py.HWSURFACE|py.FULLSCREEN|py.DOUBLEBUF
        self.display.fill(BLACK)
        # Fonts
        self.font = py.font.SysFont("monospace", 15)
        # WebCam
        self.camera = ZumaCam(self.display)
        # Gestione input
        self.events = ZumaEvents()
        self.events.handleMotorsSpeeds(self.sendSpeed)
        self.events.handleParams(self.updateParamsDisplay)
        self.events.setDefaults()
        # Controlli direzionali
        self.img_controls_x = py.image.load(self.__dir + '/assets/control_arrows_x.png')
        self.img_controls_y = py.image.load(self.__dir + '/assets/control_arrows_y.png')
        self.display.blit(self.img_controls_x, POS_CONTROLS)
        self.display.blit(self.img_controls_y, POS_CONTROLS)
        # Labels
        self.__labels['MAX_SPEED'] = self.font.render("MAX SPEED: ", 1, WHITE)
        self.__labels['ULTRASONIC'] = self.font.render("SENSORI ULTRASUONI: ", 1, WHITE)
        self.display.blit(self.__labels['MAX_SPEED'], (10, 500))
        self.display.blit(self.__labels['ULTRASONIC'], (10, 520))

    def run(self, rcv):
        self._initialize()
        self.running = True
        # Main loop :]
        while self.running:
            self.delta_time = self.clock.tick(FPS) / 1000
            self.elapsed_time = py.time.get_ticks() - self.start_time
            # self.scene_elapsed_time += self.scene_start_time + self.delta_time * 1000
            self.camera.getImage()
            if self.events.listen() == 0:
                self.running = False
            # Leggi da Bluetoth
            self.listen(rcv)
            # *after* drawing everything, flip the display
            py.display.flip()


    def listen(self, rcv):
        if(self.device is not False):
            if self.device.waitForNotifications(0.0001):  # Il temout non ho idea a quanto metterlo :)
                if(rcv.pkt[:3] == 'US '):
                    _us = rcv.pkt[3:].split(' ')
                    # print('L: ' + _us[0] + ' C: ' + _us[1] + ' R: ' + _us[2])
                    print(rcv.pkt)
                    if int(_us[1]) > 0 and int(_us[1]) < 15:
                        self.comm.write(str.encode("10 0 0>"))
                        self.force_stop = True
                        print("STOP!")
                    else:
                        self.force_stop = False

    # Invia la velocità a Zuma
    def sendSpeed(self, speeds, directions):
        self.updateControlsImage(directions)
        if(self.device is not False):
            self.comm.write(str.encode('10 ' + str(int(speeds[0])) + ' ' + str(int(speeds[1])) + ">"))
        # print(speeds)

    def updateParamsDisplay(self, params):
        for k, v in params.items():
            if k == 'BASE_SPEED':
                self.display.fill(BLACK, (10, 500, 130, 20))
                self.__labels['MAX_SPEED'] = self.font.render("MAX SPEED: {0}".format(v), 1, WHITE)
                self.display.blit(self.__labels['MAX_SPEED'], (10, 500))

    def updateControlsImage(self, directions):
        # Controlli direzionali X
        if (directions[0] == 1):
            self.img_controls_x = py.image.load(self.__dir + '/assets/control_arrows_u.png')
        elif (directions[0] == -1):
            self.img_controls_x = py.image.load(self.__dir + '/assets/control_arrows_d.png')
        else:
            self.img_controls_x = py.image.load(self.__dir + '/assets/control_arrows_x.png')
        self.display.blit(self.img_controls_x, POS_CONTROLS)
        # Controlli direzionali Y
        if (directions[1] == -1):
            self.img_controls_y = py.image.load(self.__dir + '/assets/control_arrows_r.png')
        elif (directions[1] == 1):
            self.img_controls_y = py.image.load(self.__dir + '/assets/control_arrows_l.png')
        else:
            self.img_controls_y = py.image.load(self.__dir + '/assets/control_arrows_y.png')
        self.display.blit(self.img_controls_y, POS_CONTROLS)

    def exit(self):
        self.camera.quit()
        self.display.fill(GREY)
        py.display.flip()
        py.quit()


class ZumaBtNotify(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
        self.pkt = None

    def handleNotification(self, cHandle, data):
        self.pkt = data.decode()


if __name__ == '__main__':
    z = Zuma(addr='5c:f8:21:88:26:84')
    rcv = ZumaBtNotify()
    if(z.device is not False):
        z.device.withDelegate(rcv)
    z.run(rcv)
    z.exit()

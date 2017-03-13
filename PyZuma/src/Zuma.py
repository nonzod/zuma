import os
import pygame as py
from ZumaCam import ZumaCam
from ZumaControls import ZumaControls

WIDTH = 1280  # width of our game window
HEIGHT = 720  # height of our game window
FPS = 50  # frames per second
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

    def __init__(self):
        self.running = False

    def _initialize(self):
        py.init()
        py.display.set_caption("Zuma Control")
        self.clock = py.time.Clock()
        self.display = py.display.set_mode((WIDTH, HEIGHT), py.DOUBLEBUF)
        self.display.fill(BLACK)
        # Fonts
        self.font = py.font.SysFont("monospace", 15)
        # WebCam
        self.camera = ZumaCam(self.display)
        # Gestione input
        self.controls = ZumaControls()
        self.controls.handleMotorsSpeeds(self.sendSpeed)
        self.controls.handleParams(self.updateParamsDisplay)
        self.controls.setDefaults()
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

    def run(self):
        self._initialize()
        self.running = True
        # Main loop
        while self.running:
            self.clock.tick(FPS)
            self.camera.getImage(self.display)
            if self.controls.listen() == 0:
                self.running = False
            # *after* drawing everything, flip the display
            py.display.flip()

    def sendSpeed(self, speeds, directions):
        self.updateControlsImage(directions)
        print(speeds)

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


if __name__ == '__main__':
    z = Zuma()
    z.run()
    z.exit()

import pygame
import pygame.camera
import random
import os


class ZumaMonitor():
    FPS = 25
    DISPLAY_SIZE = (1280, 720)  # (1600, 900) (1280, 720) (640, 360)
    CAMERA_DEVICE = '/dev/video0'
    CAMERA_SIZE = (640, 360)
    DEFAULT_SPEED = 100  # Velocità di default dei motori

    __dir = os.getcwd()
    # Conversione per velocità ZumaMotors
    # _input_speed valori assegnati in base ai tasti direzione 0, 1, -1
    # _output_speed valori da passare a setSpeedMotors di arduino per far girare Zuma
    _input_speed = [[0, 0], [0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1]]

    def __init__(self):
        self._obs_speeds = []  # Observer Pattern
        self._obs_params = []  # Observer Pattern
        self._speeds = [0, 0]
        self._params = []
        self.force_stop = False

        pygame.init()
        pygame.camera.init()
        pygame.display.set_caption("Zuma Controls")
        # Main Screen Display
        self.display = pygame.display.set_mode(self.DISPLAY_SIZE, pygame.DOUBLEBUF)
        # Init Webcam
        self.camera = pygame.camera.Camera(self.CAMERA_DEVICE)
        self.camera_enabled = True
        try:
            self.camera.start()
        except:
            self.camera_enabled = False
            print("No Webcam! :(")
        # Area Webcam
        if(self.camera_enabled):
            self.screen = pygame.surface.Surface(self.camera.get_size(), 0, self.display)
        else:
            pygame.draw.rect(self.display, (255, 0, 0), (10, 10, 650, 370))
        self.font = pygame.font.SysFont("monospace", 15)
        # Controlli direzionali
        self.img_controls_x = pygame.image.load(self.__dir + '/assets/control_arrows_x.png')
        self.img_controls_y = pygame.image.load(self.__dir + '/assets/control_arrows_y.png')
        # Clock
        self.clock = pygame.time.Clock()
        # Go!
        self.running = 1

    def run(self):
        # Webcam
        if(self.camera_enabled):
            self.screen = self.camera.get_image(self.screen)
            self.display.blit(self.screen, (10, 10))
        # PNG direzionali
        self.updateControlsImage()
        # Posizione mouse
        self.mouse_pos = pygame.mouse.get_pos()
        # Leggo eventi per controlli
        self.listenControls()
        # Aggiornamento display
        pygame.display.flip()
        # FPS
        self.clock.tick(self.FPS)

    def listenControls(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = 0  # sys.exit() if sys is imported
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.mousePos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    if(self.force_stop is not True):
                        self.setSpeeds(speed_x=+1)
                if event.key == pygame.K_DOWN:
                    self.setSpeeds(speed_x=-1)
                if event.key == pygame.K_LEFT:
                    self.setSpeeds(speed_y=+1)
                if event.key == pygame.K_RIGHT:
                    self.setSpeeds(speed_y=-1)
                if event.key == pygame.K_PLUS and self.DEFAULT_SPEED < 250:
                    self.DEFAULT_SPEED += 5
                    self.updateDefaultSpeed()
                if event.key == pygame.K_MINUS and self.DEFAULT_SPEED >= 0:
                    self.DEFAULT_SPEED -= 5
                    self.updateDefaultSpeed()
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and self._speeds[0] != 0:
                    self.setSpeeds(speed_x=0)
                if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and self._speeds[1] != 0:
                    self.setSpeeds(speed_y=0)

    def updateDefaultSpeed(self):
        label = self.font.render("MAX SPEED: {0}".format(self.DEFAULT_SPEED), 1, (255, 255, 255))
        self.display.fill((0, 0, 0))  # Non va bene ma refresha la velocità
        self.display.blit(label, (10, 500))

    def updateControlsImage(self):
        # Controlli direzionali X
        if (self.getSpeeds()[0] == 1):
            self.img_controls_x = pygame.image.load(self.__dir + '/assets/control_arrows_u.png')
        elif (self.getSpeeds()[0] == -1):
            self.img_controls_x = pygame.image.load(self.__dir + '/assets/control_arrows_d.png')
        else:
            self.img_controls_x = pygame.image.load(self.__dir + '/assets/control_arrows_x.png')
        self.display.blit(self.img_controls_x, (800, 90))
        # Controlli direzionali Y
        if (self.getSpeeds()[1] == -1):
            self.img_controls_y = pygame.image.load(self.__dir + '/assets/control_arrows_r.png')
        elif (self.getSpeeds()[1] == 1):
            self.img_controls_y = pygame.image.load(self.__dir + '/assets/control_arrows_l.png')
        else:
            self.img_controls_y = pygame.image.load(self.__dir + '/assets/control_arrows_y.png')
        self.display.blit(self.img_controls_y, (800, 90))

    def mousePos(self):
        discSize = random.randint(5, 50)
        # r = random.randint(100, 255)
        # g = random.randint(100, 255)
        # b = random.randint(100, 255)
        # discCol = [r, g, b]
        # pygame.draw.circle(self.display, discCol, self.mouse_pos, discSize)

    # Imposta velocità e avverte l'Observer
    def setSpeeds(self, speed_x=None, speed_y=None):
        if(speed_x is not None):
            self._speeds[0] = speed_x
        if(speed_y is not None):
            self.speeds[1] = speed_y
        if(speed_x is None and speed_y is None):
            return None
        # Ritorna la potenza da dare ai motiri L e R in base alla matrice di conversione _output_speed
        _output_speed = [[0, 0], [-self.DEFAULT_SPEED, self.DEFAULT_SPEED], [self.DEFAULT_SPEED, -self.DEFAULT_SPEED], [self.DEFAULT_SPEED, self.DEFAULT_SPEED], [self.DEFAULT_SPEED / 2, self.DEFAULT_SPEED], [self.DEFAULT_SPEED, self.DEFAULT_SPEED / 2], [-self.DEFAULT_SPEED, -self.DEFAULT_SPEED], [-self.DEFAULT_SPEED / 2, -self.DEFAULT_SPEED], [-self.DEFAULT_SPEED, -self.DEFAULT_SPEED / 2]]
        output = _output_speed[self._input_speed.index([self._speeds[0], self._speeds[1]])]
        for callback in self._obs_speeds:
            callback(output)  # Avverto del cambiamento

    def setParams(self, params=[]):
        self._params = params
        for callback in self._obs_params:
            callback(params)  # Avverto del cambiamento

    # Ritorna velocità attuale
    def getSpeeds(self):
        return self._speeds

    speeds = property(getSpeeds, setSpeeds)  # Proprietà virtuale speeds

    def getParams(self):
        return self._param

    params = property(getParams, setParams)  # Proprietà virtuale params

    # Callback
    def handleSpeeds(self, callback):
        self._obs_speeds.append(callback)

    def handleParams(self, callback):
        self._obs_params.append(callback)

    def quit(self):
        if(self.camera_enabled):
            self.camera.stop()

        self.display.fill((120, 120, 120))
        pygame.display.flip()
        pygame.quit()

# zumaGame = ZumaMonitor()
# while zumaGame.running:
#     zumaGame.run()
# zumaGame.quit()

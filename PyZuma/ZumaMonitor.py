import pygame
import pygame.camera
import random
import os


class ZumaMonitor():
    FPS = 60
    DISPLAY_SIZE = (1280, 720)  # (1600, 900) (1280, 720) (640, 360)
    CAMERA_DEVICE = '/dev/video0'
    CAMERA_SIZE = (640, 360)
    speed_motors = [0, 0]  # [x, y]

    __dir = os.getcwd()

    def __init__(self):
        self._observers = []  # Observer Pattern
        self._speeds = [0, 0]

        pygame.init()
        pygame.camera.init()
        pygame.display.set_caption("Zuma Controls")
        # Main Screen Display
        self.display = pygame.display.set_mode(self.DISPLAY_SIZE, 0)
        # Init Webcam
        self.camera = pygame.camera.Camera(self.CAMERA_DEVICE, self.CAMERA_SIZE)
        self.camera_enabled = True
        try:
            self.camera.start()
        except:
            self.camera_enabled = False
            print("No Webcam! :(")
        # Area Webcam
        if(self.camera_enabled):
            self.screen = pygame.surface.Surface(self.CAMERA_SIZE, 0, self.display)
        else:
            pygame.draw.rect(self.display, (255, 0, 0), (10,  10,   650,   370))
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
                    self.setSpeeds(speed_x=+10)
                if event.key == pygame.K_DOWN:
                    self.setSpeeds(speed_x=-10)
                if event.key == pygame.K_LEFT:
                    self.setSpeeds(speed_y=-10)
                if event.key == pygame.K_RIGHT:
                    self.setSpeeds(speed_y=+10)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.setSpeeds(speed_x=0)
                if event.key == pygame.K_DOWN:
                    self.setSpeeds(speed_x=0)
                if event.key == pygame.K_LEFT:
                    self.setSpeeds(speed_y=0)
                if event.key == pygame.K_RIGHT:
                    self.setSpeeds(speed_y=0)

    def updateControlsImage(self):
        # Controlli direzionali X
        if (self.getSpeeds()[0] == 10):
            self.img_controls_x = pygame.image.load(self.__dir + '/assets/control_arrows_u.png')
        elif (self.getSpeeds()[0] == -10):
            self.img_controls_x = pygame.image.load(self.__dir + '/assets/control_arrows_d.png')
        else:
            self.img_controls_x = pygame.image.load(self.__dir + '/assets/control_arrows_x.png')
        self.display.blit(self.img_controls_x, (800, 90))
        # Controlli direzionali Y
        if (self.getSpeeds()[1] == 10):
            self.img_controls_y = pygame.image.load(self.__dir + '/assets/control_arrows_r.png')
        elif (self.getSpeeds()[1] == -10):
            self.img_controls_y = pygame.image.load(self.__dir + '/assets/control_arrows_l.png')
        else:
            self.img_controls_y = pygame.image.load(self.__dir + '/assets/control_arrows_y.png')
        self.display.blit(self.img_controls_y, (800, 90))

    def mousePos(self):
        discSize = random.randint(5, 50)
        r = random.randint(100, 255)
        g = random.randint(100, 255)
        b = random.randint(100, 255)
        discCol = [r, g, b]
        pygame.draw.circle(self.display, discCol, self.mouse_pos, discSize)

    # Imposta velocità e avverte l'Observer
    def setSpeeds(self, speed_x=None, speed_y=None):
        if(speed_x is not None):
            self._speeds[0] = speed_x
        if(speed_y is not None):
            self.speeds[1] = speed_y

        for callback in self._observers:
            callback(self._speeds)  # Avverto del cambiamento

    # Ritorna velocità attuale
    def getSpeeds(self):
        return self._speeds

    speeds = property(getSpeeds, setSpeeds) # Proprietà virtuale speeds

    # Callback
    def handleSpeeds(self, callback):
        self._observers.append(callback)

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

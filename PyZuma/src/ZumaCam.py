from pygame import camera
import pygame as py

CAMERA_DEVICE = '/dev/video0'  # Non usato, solo per test
CAMERA_SIZE = (640, 360)


class ZumaCam(object):
    def __init__(self, display):
        self.display = display
        camera.init()
        self.clist = camera.list_cameras()
        if not self.clist:
            self.is_enabled = False
            # raise ValueError("Nessuna WebCam trovata! :[")
        else:
            self.device = camera.Camera(self.clist[0], CAMERA_SIZE)
            try:
                self.device.start()
                self.is_enabled = True
                self.surface = py.surface.Surface(self.device.get_size(), 0, display)
            except:
                self.is_enabled = False
                print("Errore nell'avvio della Webcam >:[")
                self.surface = None

    def getDevice(self):
        return self.surface

    def getImage(self):
        if self.is_enabled:
            self.device.get_image(self.surface)
            self.display.blit(self.surface, (10, 10))

    def quit(self):
        if self.is_enabled:
            self.device.stop()

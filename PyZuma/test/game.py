import _thread
import time
from bluepy.btle import Peripheral, ADDR_TYPE_RANDOM, BTLEException, DefaultDelegate
import pygame


class MyDelegate(DefaultDelegate):
    def __init__(self, params):
        DefaultDelegate.__init__(self)

    def handleNotification(self, cHandle, data):
        print(data)


try:
    per = Peripheral('5c:f8:21:88:26:84')
except BTLEException:
    print('Non trovo Zuma!')
    exit()

pygame.init()
pygame.display.set_mode([800, 600])

char_main = per.getCharacteristics(uuid='0000ffe1-0000-1000-8000-00805f9b34fb')[0]
msg = "Daje \n"
char_main.write(str.encode(msg))

def thread_game(threadName):
    print(threadName + ': start')

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # sys.exit() if sys is imported
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    print("Su")
                if event.key == pygame.K_DOWN:
                    print("Giù")
                if event.key == pygame.K_LEFT:
                    print("Sinistra")
                if event.key == pygame.K_RIGHT:
                    print("Destra")
                if event.key == pygame.K_q:
                    run = False
                char_main.write(str.encode(str(event.key) + "\n"))
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    print("Fine Su")
                if event.key == pygame.K_DOWN:
                    print("Fine Giù")
                if event.key == pygame.K_LEFT:
                    print("Fine Sinistra")
                if event.key == pygame.K_RIGHT:
                    print("Fine Destra")
                char_main.write(str.encode("-\n"))


def thread_ble_write(threadName):
    print(threadName + ': start')
    per.setDelegate(MyDelegate("false"))
    while True:
    if per.waitForNotifications(1.0):
        # handleNotification() was called
        continue

try:
    _thread.start_new_thread(thread_game, ("thread_game", ))
    _thread.start_new_thread(thread_ble_write, ("thread_ble_write", ))
except:
    print("Numm'avvio! :(")

while True:
    pass

per.disconnect()
pygame.quit()

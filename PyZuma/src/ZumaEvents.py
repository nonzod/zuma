import pygame as py


class ZumaEvents(object):
    __obs_speeds = []  # Observers Motori
    __obs_params = []  # Observers Parametri
    __speeds = [0, 0]
    __input_speed = [[0, 0], [0, 1], [0, -1], [1, 0], [1, 1], [1, -1], [-1, 0], [-1, 1], [-1, -1]]
    __output_speed = []
    __force_stop = False
    __base_speed = 100

    def setDefaults(self):
        self.setBaseSpeed(0)

    def listen(self):
        for event in py.event.get():
            if event.type == py.QUIT:
                return 0
            # if event.type == py.MOUSEBUTTONDOWN:
            #    self.mousePos()
            if event.type == py.KEYDOWN:
                if event.key == py.K_UP:
                    if(self.__force_stop is not True):
                        self.setMotorsSpeeds(speed_x=+1)
                if event.key == py.K_DOWN:
                    self.setMotorsSpeeds(speed_x=-1)
                if event.key == py.K_LEFT:
                    self.setMotorsSpeeds(speed_y=+1)
                if event.key == py.K_RIGHT:
                    self.setMotorsSpeeds(speed_y=-1)
                if event.key == py.K_PLUS and self.__base_speed < 250:
                    self.setBaseSpeed(+5)
                if event.key == py.K_MINUS and self.__base_speed > 0:
                    self.setBaseSpeed(-5)
            if event.type == py.KEYUP:
                if (event.key == py.K_UP or event.key == py.K_DOWN) and self.__speeds[0] != 0:
                    self.setMotorsSpeeds(speed_x=0)
                if (event.key == py.K_LEFT or event.key == py.K_RIGHT) and self.__speeds[1] != 0:
                    self.setMotorsSpeeds(speed_y=0)

    '''
    Modifica delle velocità dei motori Destro e Sinistro
    '''
    def setMotorsSpeeds(self, speed_x=None, speed_y=None):
        if(speed_x is not None):
            self.__speeds[0] = speed_x
        if(speed_y is not None):
            self.__speeds[1] = speed_y
        if(speed_x is None and speed_y is None):
            return None
        # Ritorna la potenza da dare ai motori L e R in base alla matrice di conversione __output_speed
        motors_speed = self.__output_speed[self.__input_speed.index([self.__speeds[0], self.__speeds[1]])]
        for callback in self.__obs_speeds:
            callback(motors_speed, self.__speeds)  # Avverto del cambiamento

    def getMotorsSpeeds(self):
        return self.__speeds

    motorsSpeeds = property(getMotorsSpeeds, setMotorsSpeeds)  # Proprietà virtuale speeds

    '''
    Modifica della velocità base di Zuma da GUI
    '''
    def setBaseSpeed(self, value):
        self.__base_speed += value
        self.__output_speed = [[0, 0], [-self.__base_speed, self.__base_speed], [self.__base_speed, -self.__base_speed], [self.__base_speed, self.__base_speed], [self.__base_speed / 2, self.__base_speed], [self.__base_speed, self.__base_speed / 2], [-self.__base_speed, -self.__base_speed], [-self.__base_speed / 2, -self.__base_speed], [-self.__base_speed, -self.__base_speed / 2]]
        for callback in self.__obs_params:
            callback({'BASE_SPEED': self.__base_speed})  # Avverto del cambiamento

    def getBaseSpeed(self):
        return self.__base_speed

    baseSpeed = property(getBaseSpeed, setBaseSpeed)  # Proprietà virtuale speeds

    # Callbacks
    def handleMotorsSpeeds(self, callback):
        self.__obs_speeds.append(callback)

    def handleParams(self, callback):
        self.__obs_params.append(callback)

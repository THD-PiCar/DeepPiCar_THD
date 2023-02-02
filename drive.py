import picar

class DeepPiCar_driving(object):

    def __init__(self):

        picar.setup()

        self.back_wheels = picar.back_wheels.Back_Wheels()
        self.back_wheels.speed = 0  # Speed Range is 0 (stop) - 100 (fastest)
        self.front_wheels = picar.front_wheels.Front_Wheels()
         # calibrate servo to center
        self.front_wheels.turn(100)

    def function_30(self):
        print("30")
        self.front_wheels.turn(100)
        self.back_wheels.speed = 50

    def function_80(self):
        print("80")
        self.front_wheels.turn(100)
        self.back_wheels.speed = 100

    def function_Stop(self):
        self.back_wheels.speed = 0

    def function_None(self):
        print("None")

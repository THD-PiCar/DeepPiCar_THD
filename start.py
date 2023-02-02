import re
import os
import cv2
import argparse
import sys
import time
from test_drive import DeepPiCar_driving

from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter
from pycoral.adapters import common
from pycoral.adapters import classify
from PIL import Image

class DeepPiCar_recognition(object):

    def __init__(self):
        self.DeepPiCar_driving = DeepPiCar_driving()
        self.current_img = "None"

# This function takes in a TFLite Interptere and Image, and returns classifications
    def classifyImage(self, interpreter, image):
        size = common.input_size(interpreter)
        common.set_input(interpreter, cv2.resize(image, size, fx=0, fy=0,
                                             interpolation=cv2.INTER_CUBIC))
        interpreter.invoke()
        return classify.get_classes(interpreter)

    # This function displays images
    def show_image(self, name, img, size, loc_x, loc_y):
        cv2.namedWindow(name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(name, size, size)
        cv2.moveWindow(name, loc_x, loc_y)
        cv2.imshow(name, img)

    # This function calls the driving functions
    def call_driving_functions(self, name):
        function = getattr(self.DeepPiCar_driving, r"function_%s" % (name))
        function()

    # This function decides whether an image recognition was accurate enough
    def image_handeling(self, name, result, current_img):

        if result > 0.7 or (name == "None" and result > 0.5):
            
            self.call_driving_functions(name)
            path = r"images/%s.png" % (name)
            self.show_image("Aktuell", cv2.imread(path, cv2.IMREAD_ANYCOLOR), 350, 200, 50)
            
            if (name != "None"):
                path = r"images/%s.png" % (name)
                self.show_image("Erkennung", cv2.imread(path, cv2.IMREAD_ANYCOLOR), 350, 200, 500)

    def main(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        # the TFLite converted to be used with edgetpu    
        parser.add_argument(
            '-m', '--model', required=True, help='File path of .tflite file.')

        # The path to labels.txt that was downloaded with your model
        parser.add_argument(
            '-l', '--labels', required=True, help='File path of labels file.')

        args = parser.parse_args()

        # Load your model onto the TF Lite Interpreter
        print('Loading {} with {} labels.'.format(args.model, args.labels))
        interpreter = make_interpreter(args.model)
        interpreter.allocate_tensors()
        labels = read_label_file(args.labels)

        cap = cv2.VideoCapture(0)
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Flip image so it matches the training input
            frame = cv2.flip(frame, 1)

            # Classify and display image
            results = self.classifyImage(interpreter, frame)
            self.show_image('frame', frame, 800, 750, 50)

            print(f'Label: {labels[results[0].id]}, Score: {results[0].score}')

        ###########

            self.image_handeling(labels[results[0].id], results[0].score, self.current_img )
            self.current_img = labels[results[0].id]

        ##########

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.call_driving_functions("Stop")
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    DeepPiCar = DeepPiCar_recognition()
    DeepPiCar.main()

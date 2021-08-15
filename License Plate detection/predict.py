from keras.models import load_model
import cv2
import numpy as np
from matplotlib import pyplot as plt
import easyocr

def predict_output(f):
    img = cv2.imread(f)
    img = cv2.resize(img, (200, 200))
    img = img/255
    model = load_model('cnn_vgg16.h5')
    img = np.reshape(img, (1,200,200,3))
    prediction = model.predict(img)
    prediction = prediction*255
    x1 = int(prediction[0][0])
    y1 = int(prediction[0][1])
    x2 = int(prediction[0][2])
    y2 = int(prediction[0][3])
    image = cv2.rectangle(img[0],(x1,y1),(x2,y2),(0, 255, 0))
    image = image*255
    cv2.imwrite('new2.png',image)

predict_output('/Users/krishma/Downloads/download.png')
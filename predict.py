import keras.models as md
import tools, numpy as np
from numpy import random as rd
from PIL import Image

def pred(img, model):
    m = md.load_model(model)

    # Zero pad data
    X = tools.zeropad(img, 5)
    data = np.ndarray((img.shape[0] * img.shape[1], 103, 11, 11, 1), dtype=np.int32)
    count = 0
    for w in range(img.shape[0]):
        for h in range(img.shape[1]):
            smp = tools.reshape(tools.make_sample(X, w+5, h+5, 11))
            data[count] = smp
            count+=1
    print("Start")
    return m.predict_classes(data, verbose=1)
    #return [np.argmax(m.predict(tools.reshape2(z))) + 1 for z in data]

def toImg(pred, shape, palette=None):
    arr = np.asarray(pred)
    arr = arr.reshape(shape)
    print(arr, arr.shape)
    #img=Image.fromarray(np.subtract(255, np.divide(255, arr).astype(int)))
    img = Image.fromarray(arr.astype(int))
    img = img.convert(mode='P')
    if not palette:
        print("Generating New Palette")
        palette = [rd.randint(0,256) for _ in range(10 * 3 - 1)]
    palette[0:2] = [0,0,0]
    print(palette)
    img.putpalette(palette)
    return img
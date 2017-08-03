import numpy as np
from PIL import Image
import copy
import tools.mat_helper as mh

import caffe

# load image, switch to BGR, subtract mean, and make dims C x H x W for Caffe
im = Image.open(mh.hypermat('../data/pavia/PaviaU.mat','../data/pavia/PaviaU_gt.mat'))
in_ = np.array(im, dtype=np.float32)
in_ = in_[:,:,::-1]
in_ = in_.transpose((2,0,1))

# load net
net = caffe.Net('deploy.prototxt', 'snapshot/train_iter_116000.caffemodel', caffe.TEST)
# shape for input (data blob is N x C x H x W), set data
net.blobs['data'].reshape(1, *in_.shape)
net.blobs['data'].data[...] = in_
# run net and take argmax for prediction
net.forward()
out = net.blobs['score'].data[0].argmax(axis=0)
out_8 = np.empty_like(out, dtype=np.uint8)
np.copyto(out_8, out, casting='unsafe')
img = Image.fromarray(out_8)
img.save("infer_out.png")

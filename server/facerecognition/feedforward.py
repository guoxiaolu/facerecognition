# coding: utf-8

from scipy import misc
import tensorflow as tf
import facenet
import numpy as np
from align_dlib import AlignDlib

with tf.Graph().as_default() as graph:
    with tf.Session() as sess:
        # Load the model
        facenet.load_model('./model/20170512-110547.pb')

        # Get input and output tensors
        images_placeholder = graph.get_tensor_by_name("input:0")
        embeddings = graph.get_tensor_by_name("embeddings:0")
        phase_train_placeholder = graph.get_tensor_by_name("phase_train:0")

face_predictor_path = './model/shape_predictor_68_face_landmarks.dat'
align = AlignDlib(face_predictor_path)
landmarkIndices = AlignDlib.OUTER_EYES_AND_NOSE

def readimg(img_path):
    img = misc.imread(img_path, mode='RGB')

    img = misc.imresize(img, (160, 160))
    img = facenet.prewhiten(img)
    img = np.expand_dims(img, axis=0)

    return img

def get_embedding(img_path):
    img = misc.imread(img_path, mode='RGB')

    # judge alignment
    aligned = align.align(160, img, [0, 0, img.shape[1], img.shape[0]], landmarkIndices=landmarkIndices)


    img = facenet.prewhiten(img)
    img = np.expand_dims(img, axis=0)

    aligned = facenet.prewhiten(aligned)
    aligned = np.expand_dims(aligned, axis=0)


    # Run forward pass to calculate embeddings
    feed_dict = {images_placeholder: img, phase_train_placeholder: False}
    emb = sess.run(embeddings, feed_dict=feed_dict)

    # Run forward pass to calculate embeddings
    feed_dict_aligned = {images_placeholder: aligned, phase_train_placeholder: False}
    emb_aligned = sess.run(embeddings, feed_dict=feed_dict_aligned)

    return emb.ravel(), emb_aligned.ravel()

# # for test
# import os
# from time import time
# def main(dir_path):
#     img_all = os.listdir(dir_path)
#     for f in img_all:
#         start = time()
#         embedding_result = get_embedding(os.path.join(dir_path, f))
#         print time() - start
#         print embedding_result
#
# main('./data')

# coding: utf-8

from scipy import misc
import tensorflow as tf
import facenet
import numpy as np

with tf.Graph().as_default() as graph:
    with tf.Session() as sess:
        # Load the model
        facenet.load_model('./model/20170512-110547.pb')

        # Get input and output tensors
        images_placeholder = graph.get_tensor_by_name("input:0")
        embeddings = graph.get_tensor_by_name("embeddings:0")
        phase_train_placeholder = graph.get_tensor_by_name("phase_train:0")


def get_embedding(img_path):
    img = misc.imread(img_path, mode='RGB')
    img = misc.imresize(img, (160, 160))
    img = facenet.prewhiten(img)
    img = np.expand_dims(img, axis=0)

    # align face pose



    # Run forward pass to calculate embeddings
    feed_dict = {images_placeholder: img, phase_train_placeholder: False}
    emb = sess.run(embeddings, feed_dict=feed_dict)

    return emb

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

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

def readimg(img_path):
    img = misc.imread(img_path, mode='RGB')

    img = misc.imresize(img, (160, 160))
    img = facenet.prewhiten(img)
    img = np.expand_dims(img, axis=0)

    return img

def get_embedding(img_path, aligned_path):
    img = readimg(img_path)
    aligned_img = readimg(aligned_path)


    # Run forward pass to calculate embeddings
    feed_dict = {images_placeholder: img, phase_train_placeholder: False}
    emb = sess.run(embeddings, feed_dict=feed_dict)

    feed_dict_aligned = {images_placeholder: aligned_img, phase_train_placeholder: False}
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


import os
import cv2
from scipy.misc import imread, imsave
from align_dlib import AlignDlib


face_predictor_path = '/Users/Lavector/git-back/facerecognition/server/model/shape_predictor_68_face_landmarks.dat'

flist = os.listdir()
img_name = '/Users/Lavector/git-back/facerecognition/client/my_faces/acbc32c963d52017081414205615711930.jpg'

align = AlignDlib(face_predictor_path)
landmarkIndices = AlignDlib.OUTER_EYES_AND_NOSE

img = imread(img_name, mode='RGB')
aligned = align.align(160, img, [445, 197, 816, 569], landmarkIndices=landmarkIndices)

# thumbnail = cv2.warpAffine(img[445:816,197:569], aligned, (160, 160))

imsave('./result.jpg', aligned)

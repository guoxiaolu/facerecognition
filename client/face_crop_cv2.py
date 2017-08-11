import cv2

cascade = cv2.CascadeClassifier("haarcascade_frontalface_alt.xml")
cap = cv2.VideoCapture(0)
while True:
    ret,frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    rect = cascade.detectMultiScale(frame,scaleFactor=1.3,minNeighbors=9,minSize=(50,50))
    # for x, y, z, w in rect:
    #     img = cv2.rectangle(frame, (x, y), (x + z, y + w), (0, 0, 255), 2)
    left = 0
    right = 0
    top = 0
    bottom = 0
    #
    for (x, y, w, h) in rect:
         img = frame[y - top:y + h + bottom, x - left:x + w + right]
         cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255),2)
    # for x, y, w, h in rect:
    #     cv2.rectangle(frame, (x-2*left, y-2*top), (x + w+right, y + h+bottom), (0, 0, 255), 2)
    #     img = frame[y - 2*top:y + h + bottom, x - 2*left:x + w + right]
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) &0xFF == ord('q'):
        #cv2.imwrite('/Users/samyzhang/Documents/xin/face_recognition/image/face.jpg', img)

        break
cap.release()
cv2.destroyAllWindows()
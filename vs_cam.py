import cv2

# from predictionpage import predictcnn

from PIL import Image
from lobefunction import predictcnn
# output=["A","B","C","D","del","E","F","G","H","I","J","K","L","M","N","nothing","O","P","Q","R","S","space","T","U","V","W","X","Y","Z"]

import os
output=os.listdir(r"C:\Users\USER\PycharmProjects\SiLingo\static\dataset_new")
print("Labels ", output)


# Importing Libraries
import cv2
import mediapipe as mp
from math import hypot

import numpy as np


# Initializing the Model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
	static_image_mode=False,

	min_detection_confidence=0.75,
	min_tracking_confidence=0.75,
	max_num_hands=2)

Draw = mp.solutions.drawing_utils
#listimg=[r"C:\Users\athul\PycharmProjects\sign language recognition - Copy\dataSet\trainingData\H\2.jpg",r"C:\Users\athul\PycharmProjects\sign language recognition - Copy\dataSet\trainingData\I\0.jpg",r"C:\Users\athul\PycharmProjects\sign language recognition - Copy\dataSet\trainingData\-1\1.jpg",
     #    r"C:\Users\athul\PycharmProjects\sign language recognition - Copy\dataSet\trainingData\H\1.jpg",r"C:\Users\athul\PycharmProjects\sign language recognition - Copy\dataSet\trainingData\O\1.jpg",
      #  r"C:\Users\athul\PycharmProjects\sign language recognition - Copy\dataSet\trainingData\W\1.jpg"]
listimg=[]
def startcam(lid,u):
    countval = 0
    # Start capturing video from webcam
    cap = cv2.VideoCapture(0)
    jj=0
    txt=""
    lastchar=""
    while True:
        # Read video frame by frame
        _, frame = cap.read()
        try:
            img1=frame.copy()

            xx1 = int(0.5 * frame.shape[1])
            xy1 = 10
            xx2 = frame.shape[1] - 10
            xy2 = int(0.35 * frame.shape[1])

            cv2.rectangle(frame, (xx1 - 1, xy1 - 1), (xx2 + 1, xy2 + 1), (255, 0, 0), 1)
            cv2image = frame # cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)


            # Flip image
            frame = cv2.flip(frame, 1)

            # Convert BGR image to RGB image
            frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Process the RGB image
            Process = hands.process(frameRGB)

            landmarkList = []
            # if hands are present in image(frame)
            if Process.multi_hand_landmarks:
                # detect handmarks
                for handlm in Process.multi_hand_landmarks:
                    for _id, landmarks in enumerate(handlm.landmark):
                        # store height and width of image
                        height, width, color_channels = frame.shape

                        # calculate and append x, y coordinates
                        # of handmarks from image(frame) to lmList
                        x, y = int(landmarks.x * width), int(landmarks.y * height)
                        landmarkList.append([_id, x, y])

                    # draw Landmarks
                    Draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)
            x1, y1, x2, y2 = 10000, 10000, 0, 0
            jj = jj + 1
            # If landmarks list is not empty
            if landmarkList != []:
                cv2image = cv2image[xy1: xy2, xx1: xx2]
                cv2.imwrite(r"C:\Users\USER\PycharmProjects\SiLingo\static\sampleeee.jpg", cv2image)


                for i in range(0,len(landmarkList)):
                    x,y=landmarkList[i][1], landmarkList[i][2]
                    if(x1>x):
                        x1=x
                    if x>x2:
                        x2=x

                    if(y1>y):
                        y1=y
                    if y>y2:
                        y2=y

                color = (255, 0, 0)

                # Line thickness of 2 px
                thickness = 2
                x1 = x1 - 10
                y1 = y1 - 10
                x2 = x2 + 10
                y2 = y2 + 10
                # Using cv2.rectangle() method
                # Draw a rectangle with blue line borders of thickness of 2 px
                # cv2.rectangle(frame, (x1,y1), (x2,y2), color, thickness)

                h = y2 - y1
                w = x2 - x1
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)  # draw rectangle to main image

                # print(x1,y1,x2,y2,"=================================")
                #
                # print(x1,y1)
                try:
                    print(jj)
                    if jj >= 100:
                    # print(y1,y2-y1,x1,x2-x1,"++++++++++++++++++++++++++++++++")


                        cv2image = cv2.flip(cv2image, 1)
                        # cv2image = cv2image[y1 : y2, x1 : x2]
                        # cv2image = frame[ y1:(y1+h),x1:(x1+w)]
                        # cv2.imwrite(r"C:\Users\USER\PycharmProjects\SiLingo\static\sample.jpg",img1)
                        cv2.imwrite(r"C:\Users\USER\PycharmProjects\SiLingo\static\sample.jpg",cv2image)
                        print("img1++++++++++===========================")
                        im = Image.open(r"C:\Users\USER\PycharmProjects\SiLingo\static\sample.jpg")
                        im1 = im.crop( (x1,y1,x2, y2))
                        #
                        # # Shows the image in image viewer
                        im1 = im1.save(r"C:\Users\USER\PycharmProjects\SiLingo\static\samplecrop1.jpg")
                        #
                        jj=0
                        image = cv2.imread(r"C:\Users\USER\PycharmProjects\SiLingo\static\sampleeee.jpg")
                        # image = cv2.imread(r"C:\Users\USER\PycharmProjects\SiLingo\static\samplecrop1.jpg")
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

                        invert = cv2.bitwise_not(gray)  # OR
                        # invert = 255 - image


                        # Setting parameter values
                        t_lower = 50  # Lower Threshold
                        t_upper = 150  # Upper threshold

                        # Applying the Canny Edge filter
                        edge = cv2.Canny(invert, t_lower, t_upper)

                        invert = cv2.bitwise_not(edge)  # OR

                        cv2.imwrite(r"C:\Users\USER\PycharmProjects\SiLingo\static\samplecrop2.jpg",invert)
                        # res=predictcnn(r"C:\Users\athul\PycharmProjects\sign language recognition - Copy\samplecrop2.jpg")
                        # res=predictcnn(r"C:\Users\athul\PycharmProjects\sign language recognition - Copy\dataSet\trainingData\N\1.jpg")
                        print("CC ", countval)
                        if countval<len(listimg):
                            res = predictcnn(r"C:\Users\USER\PycharmProjects\SiLingo\static\samplecrop2.jpg")
                            # res = predictcnn(r"C:\Users\USER\PycharmProjects\SiLingo\static\sample.jpg")
                            countval=countval+1
                        else:
                            res=predictcnn(r"C:\Users\USER\PycharmProjects\SiLingo\static\samplecrop2.jpg")
                            # res=predictcnn(r"C:\Users\USER\PycharmProjects\SiLingo\static\sample.jpg")
                        print("abc  ", res)
                        # print(output[res[0]])
                        # print(res, output[res[0]])
                        # res=output[res[0]]
                        if lastchar=="" and res=="space":
                            pass
                        elif res=="space":
                            txt=txt+" "
                            lastchar=""
                        else:
                            try:
                                lastchar=txt[-1]
                            except:
                                pass
                            txt=txt+res


                except Exception as e:
                    print(e)
            else:
                image=frame
                # set brightness
                # sbc.set_brightness(int(b_level))

            # Display Video and when 'q' is entered,
            # destroy the window
            font = cv2.FONT_HERSHEY_SIMPLEX

            # org
            org = (350, 100)

            # fontScale
            fontScale = 1

            # Blue color in BGR
            color = (255, 0, 0)

            # Line thickness of 2 px
            thickness = 2
            print("=======",txt)
            # Using cv2.putText() method
            cv2.putText(frame, txt, org, font,
                                fontScale, color, thickness, cv2.LINE_AA)
            cv2.imshow('Image', frame)
            if cv2.waitKey(1) & 0xff == ord('q'):
                # if u=='student':
                #     from Dbconnection import Db
                #     db = Db()
                #     if txt != "":
                #         q = db.selectOne(
                #             "select * from studies where Student_id='" + lid + "' and  Words='" + txt + "' and Date=curdate()")
                #         if q is None:
                #             db.insert(
                #             "insert into `studies`(`Studies_id`,`Words`,`Student_id`,`Date`) values ( '','" + txt + "','" + lid + "',curdate());")
                break
        except Exception as e:
            print(e)
            pass


startcam('1', 'h')
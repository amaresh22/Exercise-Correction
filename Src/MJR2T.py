import cv2
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import pickle
import os

os.chdir("C:\\Users\\mamar\\OneDrive\\Desktop")

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode = True , min_detection_confidence = 0.2 , model_complexity = 0 )
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

DATA_DIR = ('C:\\Users\\mamar\\OneDrive\\Desktop\\Major Project 1')
data = []
labels = []
for dir_ in os.listdir(DATA_DIR):
    data_aux = []
    for img_path in os.listdir(os.path.join(DATA_DIR,dir_)):
        img = cv2.imread(os.path.join(DATA_DIR,dir_,img_path))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        #detecting the landmarks in the images
        result = pose.process(img_rgb)

        
        #  #this line below is drawing the skeleton structure ie the lines

        if result.pose_landmarks:
            
        #             mp_drawing.draw_landmarks(
        #             img_rgb,
        #             result.pose_landmarks,
        #             mp_pose.POSE_CONNECTIONS,
        #             mp_drawing_styles.get_default_pose_landmarks_style())

            for i in range (33):
                x = result.pose_landmarks.landmark[i].x
                y = result.pose_landmarks.landmark[i].y
                
                data_aux.append(x)
                data_aux.append(y)
                
            if (len(data_aux) == 33):

                data.append(data_aux)
                labels.append(dir_)

            

f = open('data.pickle','wb')
pickle.dump({'data':data,'labels':labels},f)
f.close()



##############to ptint the images
#         plt.figure()
        
#         plt.imshow (img_rgb)

# plt.show()
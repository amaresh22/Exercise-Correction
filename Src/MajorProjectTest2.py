
import mediapipe as mp
import math
import cv2
from time import time
import matplotlib.pyplot as plt
import numpy as np
import nbformat


# In[2]:


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode = False , min_detection_confidence = 0.3 , model_complexity =1 )
mp_drawing = mp.solutions.drawing_utils



# In[3]:


import os
# os.chdir('C:\\Users\\mamar\\Major Project')
os.chdir("C:\\Users\\mamar\\OneDrive\\Desktop\\prj")

# In[4]:


def detectPose(image,pose,display=True):
    output_image=image.copy()
    imageRGB = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
    results=pose.process(imageRGB)
    height,width,_=image.shape
    landmarks=[]
    if results.pose_landmarks:
        mp_drawing.draw_landmarks(image=output_image,landmark_list=results.pose_landmarks,
                                  connections=mp_pose.POSE_CONNECTIONS)
        for landmark in results.pose_landmarks.landmark:
            landmarks.append((int(landmark.x *width),int(landmark.y * height),(landmark.z *width)))

    if display:

        plt.figure(fidsize=[22,22])
        plt.subplot(121);plt,imshow(image[:,:,::-1]);plt.title("original");plt.axis('off');
        plt.subplot(122);plt,imshow(output_image[:,:,::-1]);plt.title("output");plt.axis('off');

        mp_drawing.plot_landmarks(results.pose_world_landmarks,mp_pose.POSE_CONNECTIONS)

    else:
        return output_image,landmarks
        
            
    


# In[5]:


def calculateAngle(landmark1 , landmark2, landmark3,):
    x1,y1,_ = landmark1
    x2,y2,_ = landmark2
    x3,y3,_ = landmark3

    angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1 -y2,x1-x2))

    if angle < 0 :
        angle+=360
        
    return angle


# In[6]:


def squat(landmarks , frame , display =False):
    label = ' Squat' 
    color = (0,0,255)

   

    cv2.putText(frame, label,(30,30), cv2.FONT_HERSHEY_PLAIN,2, color,2)
    if display:
            #S plt.figure(figsize=[10,10])
            plt.imshow(frame[:,:,::-1]);plt.title("output image");plt.axis('off');label;
        
    else:
        return frame , label
    

    


# In[7]:


def classifyPose(landmarks , output_image , display = False ):
    label = 'Unknown Exercise'
    color = (0,0,255)
    #getting angles between the lines

    #hip angle
    left_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value])
    
    right_hip_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value])
    #knee angle
    left_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    right_knee_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_KNEE.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])
    #elbow angle
    left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    #shoulder
    left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
                                    landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    
    # # check for squat pose
    if (( left_hip_angle < 75 and left_hip_angle > 50 )or(right_hip_angle<75 and right_hip_angle>50)):
        if((left_knee_angle < 75 and left_knee_angle > 55 )or(right_hip_angle<75 and right_knee_angle>50)):
           label = 'Squat start' 

    #checking for pushup
    # if left_elbow_angle >165 and left_elbow_angle < 195 and right_elbow_angle>165 and right_elbow_angle<195:
    #     if left_knee_angle>160 and left_knee_angle <195 or right_knee_angle>160 and right_knee_angle<195:
    #             label = 'T Pose'
    if ((left_hip_angle <165 and left_hip_angle >180) or(right_hip_angle<165 and right_hip_angle<180)):
        if((left_shoulder_angle>60 and left_shoulder_angle<72)or(right_shoulder_angle>60 and right_shoulder_angle<72)):
            if((left_elbow_angle> 170 and left_elbow_angle<180)or(right_elbow_angle> 170 and right_elbow_angle<180 )):
                label = 'push up position start'

    #checking for shoulder press
    if((left_shoulder_angle > 85 and left_shoulder_angle < 110) or(right_shoulder_angle> 85 and right_shoulder_angle<110)):
        if((left_elbow_angle >80 and left_shoulder_angle < 100  ) or(right_shoulder_angle >80 and right_shoulder_angle < 100 )):
            label = 'dumbbell shoulder press start'
            
    #checking for curls
    if((left_elbow_angle > 80 and left_elbow_angle < 100) or(right_elbow_angle >80 and right_elbow_angle <100)):
        if((left_shoulder_angle > 0 and left_shoulder_angle <30) or (right_shoulder_angle >0 and right_shoulder_angle <30)):
            label = 'dumbbell curls start'
            
    #correctionof poses
    #calling executable files based on the label;
    if label == 'Squat start':
        # get_ipython().run_line_magic('run', './Squat.ipynb')
        exec(open("Squat.py").read())

        

    if label == 'push up position start':
        # get_ipython().run_line_magic('run', './Chest.ipynb')
        exec(open("Chest.py").read())



    if label == 'T Pose':
        # get_ipython().run_line_magic('run', './Chest.ipynb')
        exec(open("Chest.py").read())



    if label == 'dumbbell shoulder press start':
        # get_ipython().run_line_magic('run', './Shoulder.ipynb')
        exec(open("Shoulder.py").read())



    if label == 'dumbbell curls start':
        # get_ipython().run_line_magic('run', './bicep.ipynb')
        exec(open("bicep.py").read())
    
        # while video.isOpened():
        #     frame,label = squat(landmarks,output_image,display=False)
        #     #cv2.namedWindow('Squat Detection', cv2.WINDOW_NORMAL)
        #     cv2.imshow('Squat Detection', frame)
        #     key = cv2.waitKey(1) & 0xFF
        #     if key == 32:
        #         break
        #  # space key to close the window
        # cv2.destroyWindow('Squat Detection') 

    # standing still 
    # if ( left_hip_angle > 160 and left_knee_angle >150) or (right_hip_angle >160 and right_knee_angle >150 ):
    #     label = 'Standing still'
    if label!='Unknown Pose':
        color = (0,255,0)

    cv2.putText(output_image, label,(30,30), cv2.FONT_HERSHEY_PLAIN,2,color,2)

    if display:
       #S plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("output image");plt.axis('off');label;

    else:
        return output_image , label


# In[8]:


pose_video = mp_pose.Pose(static_image_mode = False , min_detection_confidence = 0.5 , model_complexity =1 )
video = cv2.VideoCapture(0)
# cv2.namedWindow('PoseDetection',cv2.WINDOW_NORMAL)

video.set(3,1920)

video.set(4,1080)

time1=0
# while video.isOpened():
while video.isOpened():
    ok , frame = video.read()
    if not ok :
        break 
              
    frame  = cv2.flip(frame , 1)
    # frame_height , frame_width , _ = frame.shape 
    #  frame = cv2.resize(frame,(int(frame_width*(640/frame_height)),640))
    frame,landmarks=detectPose(frame,pose_video,display=False)
            
    if landmarks:
        frame,_ = classifyPose(landmarks, frame,display = False)
            
                
            # time2 = time()
            # if(time2-time1)>0:
            #     frames_per_second = 1.0/(time2-time1)
            #     cv2.putText(frame,'FPS:{}'.format( int (frames_per_second)),(10,30),cv2.FONT_HERSHEY_PLAIN,4,(0,255,0),3)
            # time1=time2
            
            
    cv2.imshow('Pose Classification', frame)
    # cv2.resizeWindow('Pose Classification', 1920, 1080)
            
#         # k = cv2.waitKey(1)&0xFF
#         # if(k==27):
#         #     break
        
    
    k = cv2.waitKey(1)&0xFF
    if(k==27):
        break
       
            
video.release()
cv2.destroyWindow('Pose Classification')


# In[ ]:





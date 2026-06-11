
import mediapipe as mp
import math
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import nbformat
# from gtts import gTTS
# import pygame , sys 
# pygame.mixer.init()
count =0
# In[2]:
import threading
import os
# os.chdir('C:\\Users\\mamar\\Major Project')
os.chdir("C:\\Users\\mamar\\OneDrive\\Desktop\\prj")
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode = False , min_detection_confidence = 0.3 , model_complexity =1 )
mp_drawing = mp.solutions.drawing_utils

print("squat")


# In[3]:


def squatPose(image,pose,display=True):
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
        plt.subplot(121);plt,imshow(image[:,:,::-1]);plt.title("original1");plt.axis('off');
        plt.subplot(122);plt,imshow(output_image[:,:,::-1]);plt.title("output1");plt.axis('off');

        mp_drawing.plot_landmarks(results.pose_world_landmarks,mp_pose.POSE_CONNECTIONS)

    else:
        return output_image,landmarks
        
            


# In[4]:


def calculateAngle(landmark1 , landmark2, landmark3,):
    x1,y1,_ = landmark1
    x2,y2,_ = landmark2
    x3,y3,_ = landmark3

    angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1 -y2,x1-x2))

    if angle < 0 :
        angle+=360
        
    return angle


# In[5]:
def play_audio(audio_file):
    pygame.mixer.music.load(audio_file)
    pygame.mixer.music.play()


def classifysquat(landmarks , output_image ,count ,display = False ):
    label = 'Do a squat'
    text = count
    # language ='en'
    color = (0,255,)
    # speech = gTTS(text = text , lang = language , slow = false , )
    # speec
    text = str(count)
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
    # #elbow angle
    # left_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
    #                                 landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
    #                                 landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value])

    # right_elbow_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
    #                                 landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
    #                                 landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value])
    # #shoulder
    # left_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value],
    #                                 landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value],
    #                                 landmarks[mp_pose.PoseLandmark.LEFT_HIP.value])

    # right_shoulder_angle = calculateAngle(landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value],
    #                                 landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value],
    #                                 landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value])

    if(left_knee_angle > 75):
        label = "bend your knees"
        # pygame.mixer.music.load('bendyourknees.mp3')
        # pygame.mixer.music.play()
        # pygame.time.wait(1000)
        # pygame.mixer.music.unload()
        # threading.Thread(target=play_audio, args=("bendyourknees.mp3",)).start()

    elif(left_knee_angle<50):
        label = "lift your knees"
        # pygame.mixer.music.load('liftyourknees.mp3')
        # pygame.mixer.music.play()
        # pygame.time.wait(1000)
        # threading.Thread(target=play_audio, args=("liftyourknees.mp3",)).start()

        # pygame.mixer.music.unload()

    elif(left_hip_angle >85 ):
        label = "bend your back"
        # pygame.mixer.music.load('bendyourback.mp3')
        # pygame.mixer.music.play()
        # pygame.time.wait(1000)
        # pygame.mixer.music.unload()
        # threading.Thread(target=play_audio, args=("bendyourback.mp3",)).start()


    elif(left_hip_angle<50):
        label= "lift your back"    
        # pygame.mixer.music.load('Liftyourknees.mp3')
        # pygame.mixer.music.play()
        # pygame.time.wait(1000)
        # pygame.mixer.music.unload()
        # threading.Thread(target=play_audio, args=("Liftyourknees.mp3",)).start()


    # if(left_knee_angle > 285):
    #     label = "bend your knees"

    # if(left_knee_angle<265):
    #     label = "lift your knees"

    # if(left_hip_angle >285 ):
    #     label = "bend your back"

    # if(left_hip_angle<265):
    #     label= "lift your back" 
    
    if (( left_hip_angle < 75 and left_hip_angle > 50 )or(right_hip_angle<285 and right_hip_angle>265)):
        if((left_knee_angle < 75 and left_knee_angle > 55 )or(right_hip_angle<285 and right_knee_angle>260)):
            label = 'Perfect Squat Achieved' 
            # pygame.mixer.music.load('SquatAchieved.mp3')
            # pygame.mixer.music.play()
            # pygame.time.wait(3000)
            count = count +1
            text = str(count)
            # cv2.putText(output_image, label,(30,70), cv2.FONT_HERSHEY_PLAIN,6,color,4)
            # cv2.putText(output_image, text,(50,170), cv2.FONT_HERSHEY_PLAIN,6,color,4)
            # time.sleep(1.5)

    cv2.putText(output_image, label,(30,70), cv2.FONT_HERSHEY_PLAIN,5,color,3)
    # cv2.putText(output_image, text,(50,170), cv2.FONT_HERSHEY_PLAIN,5,color,3)

    if display:
       #S plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("squat");plt.axis('off');label;#count;

    else:
        return output_image , label


# In[18]:


pose_video = mp_pose.Pose(static_image_mode = False , min_detection_confidence = 0.5 , model_complexity =1 )
video = cv2.VideoCapture(0)
# cv2.namedWindow('PoseDetection',cv2.WINDOW_NORMAL)

video.set(3,1920)
video.set(4,1080)

time1=0

while video.isOpened():
    ok , frame = video.read()
    if not ok :
        break 

    frame  = cv2.flip(frame , 1)
   # frame_height , frame_width , _ = frame.shape 
  #  frame = cv2.resize(frame,(int(frame_width*(640/frame_height)),640))
    frame,landmarks=squatPose(frame,pose_video,display=False)

    if landmarks:
        frame,_ = classifysquat(landmarks, frame,count,display = False)

    
    # time2 = time()
    # if(time2-time1)>0:
    #     frames_per_second = 1.0/(time2-time1)
    #     cv2.putText(frame,'FPS:{}'.format( int (frames_per_second)),(10,30),cv2.FONT_HERSHEY_PLAIN,4,(0,255,0),3)
    # time1=time2


    cv2.imshow('Pose squat', frame)
    # cv2.resizeWindow('Pose squat', 1920, 1080)

    k = cv2.waitKey(1)&0xFF
    if(k==32):

        break

# video.release()

cv2.destroyWindow('Pose squat')


# In[ ]:





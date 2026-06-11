
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

print("bicep curls")


# In[3]:


def BicepPose(image,pose,display=True):
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
        plt.subplot(121);plt,imshow(image[:,:,::-1]);plt.title("original4");plt.axis('off');
        plt.subplot(122);plt,imshow(output_image[:,:,::-1]);plt.title("output4");plt.axis('off');

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


# In[22]:


def classifyBicep(landmarks , output_image , display = False ):
    label = 'bicep curls'
    color = (0,0,255)
    count = 0 
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
    if((left_elbow_angle <180) or(right_elbow_angle <180 )):
        if((left_shoulder_angle > 0 and left_shoulder_angle <30) or (right_shoulder_angle >0 and right_shoulder_angle <30)):
            label = 'dumbbell curls start'

    if((left_elbow_angle <150) or(right_elbow_angle <150 )):
        if((left_shoulder_angle > 0 and left_shoulder_angle <30) or (right_shoulder_angle >0 and right_shoulder_angle <30)):
            label = 'beginning of curl, curl more'

    if((left_elbow_angle <90) or(right_elbow_angle <90 )):
        if((left_shoulder_angle > 0 and left_shoulder_angle <30) or (right_shoulder_angle >0 and right_shoulder_angle <30)):
            label = 'Middle of curl, go further'
             
    if((left_elbow_angle <60) or(right_elbow_angle <60 )):
        if((left_shoulder_angle > 0 and left_shoulder_angle <45) or (right_shoulder_angle >0 and right_shoulder_angle <45)):
            label = 'Bicep Curl Complete'
    if label!='Bicep curls':
        color = (0,255,0)

    cv2.putText(output_image, label,(30,90), cv2.FONT_HERSHEY_PLAIN,3,color,3)

    if display:
       #S plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("squat");plt.axis('off');label;

    else:
        return output_image , label


# In[24]:


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
    frame,landmarks=BicepPose(frame,pose_video,display=False)

    if landmarks:
        frame,_ = classifyBicep(landmarks, frame,display = False)

    
    # time2 = time()
    # if(time2-time1)>0:
    #     frames_per_second = 1.0/(time2-time1)
    #     cv2.putText(frame,'FPS:{}'.format( int (frames_per_second)),(10,30),cv2.FONT_HERSHEY_PLAIN,4,(0,255,0),3)
    # time1=time2


    cv2.imshow('Pose CURLS', frame)
    # cv2.resizeWindow('Pose CURLS', 1920, 1080)

    # cv2.setWindowProperty('Pose CURLS', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    k = cv2.waitKey(1)&0xFF
    if(k==32):

        break

# video.release()

cv2.destroyWindow('Pose CURLS')


# In[ ]:





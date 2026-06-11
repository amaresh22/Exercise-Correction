
import mediapipe as mp
import math
import cv2
from time import time
import matplotlib.pyplot as plt
import numpy as np
import nbformat


# In[18]:


mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode = False , min_detection_confidence = 0.3 , model_complexity =1 )
mp_drawing = mp.solutions.drawing_utils

print("Shoulder press")


# In[20]:


def  ShoulderPose(image,pose,display=True):
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
        plt.subplot(121);plt,imshow(image[:,:,::-1]);plt.title("original2");plt.axis('off');
        plt.subplot(122);plt,imshow(output_image[:,:,::-1]);plt.title("output2");plt.axis('off');

        mp_drawing.plot_landmarks(results.pose_world_landmarks,mp_pose.POSE_CONNECTIONS)

    else:
        return output_image,landmarks
        


# In[22]:


def calculateAngle(landmark1 , landmark2, landmark3,):
    x1,y1,_ = landmark1
    x2,y2,_ = landmark2
    x3,y3,_ = landmark3

    angle = math.degrees(math.atan2(y3-y2,x3-x2)-math.atan2(y1 -y2,x1-x2))

    if angle < 0 :
        angle+=360
        
    return angle


# In[24]:


def classifyShoulder(landmarks , output_image , display = False ):
    label = 'Start'
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

    if((left_shoulder_angle > 85 and left_shoulder_angle < 110) or(right_shoulder_angle> 85 and right_shoulder_angle<110)):
        if((left_elbow_angle >80 and left_shoulder_angle < 100  ) or(right_shoulder_angle >80 and right_shoulder_angle < 100 )):
            label = 'Start Position'

    if((left_shoulder_angle > 105 and left_shoulder_angle < 150) or(right_shoulder_angle> 105 and right_shoulder_angle<150)):
        if((left_elbow_angle >100 and left_shoulder_angle < 150  ) or(right_shoulder_angle >100 and right_shoulder_angle < 150 )):
            label = 'Lift Arm even more(straighten)'
            
    if((left_shoulder_angle > 150 and left_shoulder_angle < 180) or(right_shoulder_angle> 150 and right_shoulder_angle<180)):
        if((left_elbow_angle >150 and left_shoulder_angle < 180  ) or(right_shoulder_angle >150 and right_shoulder_angle < 180 )):
            label = 'shoulder press complete'
    
    
    

    
    if label!='Shoulder press':
        color = (0,255,0)

    cv2.putText(output_image, label,(30,70), cv2.FONT_HERSHEY_PLAIN,6,color,4)

    if display:
       #S plt.figure(figsize=[10,10])
        plt.imshow(output_image[:,:,::-1]);plt.title("Pose ShoulderPress");plt.axis('off');label;

    else:
        return output_image , label


# In[30]:


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
    frame,landmarks=ShoulderPose(frame,pose_video,display=False)

    if landmarks:
        frame,_ = classifyShoulder(landmarks, frame,display = False)

    
    # time2 = time()
    # if(time2-time1)>0:
    #     frames_per_second = 1.0/(time2-time1)
    #     cv2.putText(frame,'FPS:{}'.format( int (frames_per_second)),(10,30),cv2.FONT_HERSHEY_PLAIN,4,(0,255,0),3)
    # time1=time2


    cv2.imshow('Pose ShoulderPress', frame)
    # cv2.resizeWindow('Pose ShoulderPress', 1920, 1080)

    k = cv2.waitKey(1)&0xFF
    if(k==32):

        break

# video.release()

cv2.destroyWindow('Pose ShoulderPress')


# In[ ]:





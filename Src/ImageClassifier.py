import pickle
import os
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

os.chdir("C:\\Users\\mamar\\OneDrive\\Desktop")

data_dict = pickle.load(open('C:\\Users\\mamar\\OneDrive\\Desktop\\data.pickle' , 'rb'))

# print(data_dict.keys())
# print(data_dict)



# print(len(data_dict['data']))
# print(len(data_dict['labels']))


# print("Loaded labels:", data_dict['labels'])

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])
print (data,labels)

x_train, x_test , y_train , y_test = train_test_split(data,labels,test_size=0.2,shuffle=True,stratify=labels)

model = RandomForestClassifier()

model.fit(x_train,y_train)

y_predict = model.predict(x_test)

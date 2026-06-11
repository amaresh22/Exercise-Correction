# modules
from PyQt5.QtWidgets import QApplication, QWidget,QTextEdit,QComboBox,QPushButton,QLabel,QHBoxLayout,QVBoxLayout
import os
import subprocess
import threading
import pygame
# os.chdir('C:\\Users\\mamar\\Major Project')
os.chdir("C:\\Users\\mamar\\OneDrive\\Desktop\\prj")
#Class
class Home(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.settings()
        self.button_click()
        

    def initUI(self):
        self.title = QLabel("Choose your Exercise")
        self.title2 = QLabel("EXFIT:Exercise Correction Desktop App")
        self.Squat = QPushButton("Squat")
        self.PushUp = QPushButton("PushUP")
        self.ShoulderPress = QPushButton("ShoulderPress")
        self.BicepCurls = QPushButton("BicepCurls")
        self.PoseEstimation = QPushButton("Exercise Detection")

        self.master = QVBoxLayout()
        
        self.master.addWidget(self.title2)
        self.title2.setContentsMargins(0, 0, 0, 10)
        self.title2.setFixedSize(1000, 50)
        self.master.setSpacing(10)

        self.button=QHBoxLayout()
        col1=QVBoxLayout()
        col2=QVBoxLayout()
        col3=QVBoxLayout()
        
        col1.addWidget(self.title)
        col2.addWidget(self.Squat)
        col2.addWidget(self.ShoulderPress)
        col2.addWidget(self.PoseEstimation)
        col3.addWidget(self.PushUp)
        col3.addWidget(self.BicepCurls)
        
        self.button.addLayout(col1,20)
        self.button.addLayout(col2,40)
        self.button.addLayout(col3,40)

        self.master.addLayout(self.button)
        self.setLayout(self.master)


    def settings(self):
        self.setWindowTitle("EX Fit")
        self.setGeometry(250,250,1500,800)

    def button_click(self):
        self.Squat.clicked.connect(lambda:self.run_squat_script())
        self.PushUp.clicked.connect(lambda:self.run_PushUp_script())
        self.ShoulderPress.clicked.connect(lambda:self.run_ShoulderPress_script())
        self.BicepCurls.clicked.connect(lambda:self.run_BicepCurls_script())
        self.PoseEstimation.clicked.connect(lambda:self.run_PoseEstimation_script())
        

    def run_squat_script(self):
        # import subprocess

        # subprocess.run(["python", "Squat.py"])
        script_path = "C:\\Users\\mamar\\OneDrive\\Desktop\\prj\\Squat.py"
    
        if os.path.exists(script_path):
            # subprocess.run(["python", script_path])
            threading.Thread(target=subprocess.run, args=(["python", script_path],)).start()
        else:
            print("Error: Squat.py not found!")

    def run_ShoulderPress_script(self):
        # import subprocess

        # subprocess.run(["python", "Squat.py"])
        script_path = "C:\\Users\\mamar\\OneDrive\\Desktop\\prj\\Shoulder.py"
    
        if os.path.exists(script_path):
            # subprocess.run(["python", script_path])
            threading.Thread(target=subprocess.run, args=(["python", script_path],)).start()
        else:
            print("Error: Shoulder.py not found!")

    def run_PushUp_script(self):
        # import subprocess

        # subprocess.run(["python", "Squat.py"])
        script_path = "C:\\Users\\mamar\\OneDrive\\Desktop\\prj\\Chest.py"
    
        if os.path.exists(script_path):
            # subprocess.run(["python", script_path])
            threading.Thread(target=subprocess.run, args=(["python", script_path],)).start()
        else:
            print("Error: Chest.py not found!")
    
    def run_BicepCurls_script(self):
        # import subprocess

        # subprocess.run(["python", "Squat.py"])
        script_path = "C:\\Users\\mamar\\OneDrive\\Desktop\\prj\\bicep.py"
    
        if os.path.exists(script_path):
            # subprocess.run(["python", script_path])
            threading.Thread(target=subprocess.run, args=(["python", script_path],)).start()
        else:
            print("Error: bicep.py not found!")
    def run_PoseEstimation_script(self):
        # import subprocess

        # subprocess.run(["python", "Squat.py"])
        script_path = "C:\\Users\\mamar\\OneDrive\\Desktop\\prj\\MajorProjectTest2.py"
    
        if os.path.exists(script_path):
            # subprocess.run(["python", script_path])
            threading.Thread(target=subprocess.run, args=(["python", script_path],)).start()
        else:
            print("Error: PoseEstimation.py not found!")         





if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet("""
        QWidget{
            background-color: #C8F2FC ;
            color: #00A7C3;
            font-family: 'Roboto'

        }
        QPushButton{
            font-size:35px;
            background-color:#BFFCDD


        }
        QPushButton:Hover{
            font-size:40px;
            background-color:#FFE1C0
            

        }
        QLabel{
            font-size:40px;
            font-family: "Arial";
            margin-top: -10px;
            font-weight: bold;

        }


    """)
    main = Home()
    main.show()
    app.exec()

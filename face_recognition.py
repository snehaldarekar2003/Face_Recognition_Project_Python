# import re
from sys import path
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
import os
import mysql.connector
import csv
import cv2
import numpy as np
from tkinter import messagebox
from time import strftime
from datetime import datetime
class Face_Recognition:

    def __init__(self,root):
        self.root=root
        self.root.geometry("1366x768+0+0")
        self.root.title("Face Recognition Pannel")

        # This part is image labels setting start 
        # first header image  
        img=Image.open(r"C:\Users\user\Documents\Python_Test_Projects\Images_GUI\banner.jpg")
        img=img.resize((1366,130),Image.Resampling.LANCZOS)
        self.photoimg=ImageTk.PhotoImage(img)

        # set image as lable
        f_lb1 = Label(self.root,image=self.photoimg)
        f_lb1.place(x=0,y=0,width=1366,height=130)

        # backgorund image 
        bg1=Image.open(r"C:\Users\user\Documents\Python_Test_Projects\Images_GUI\bg2.jpg")
        bg1=bg1.resize((1366,768),Image.Resampling.LANCZOS)
        self.photobg1=ImageTk.PhotoImage(bg1)

        # set image as lable
        bg_img = Label(self.root,image=self.photobg1)
        bg_img.place(x=0,y=130,width=1366,height=768)


        #title section
        title_lb1 = Label(bg_img,text="Welcome to Face Recognition Pannel",font=("verdana",30,"bold"),bg="white",fg="navyblue")
        title_lb1.place(x=0,y=0,width=1366,height=45)

        # Create buttons below the section 
        # ------------------------------------------------------------------------------------------------------------------- 
        # Training button 1
        std_img_btn=Image.open(r"C:\Users\user\Documents\Python_Test_Projects\Images_GUI\f_det.jpg")
        std_img_btn=std_img_btn.resize((180,180),Image.Resampling.LANCZOS)
        self.std_img1=ImageTk.PhotoImage(std_img_btn)

        std_b1 = Button(bg_img,command=self.face_recog,image=self.std_img1,cursor="hand2")
        std_b1.place(x=600,y=170,width=180,height=180)

        std_b1_1 = Button(bg_img,command=self.face_recog,text="Face Detector",cursor="hand2",font=("tahoma",15,"bold"),bg="white",fg="navyblue")
        std_b1_1.place(x=600,y=350,width=180,height=45)

        back_btn = Button(bg_img, command=self.go_back,text="Back",font=("tahoma",15,"bold"),bg="red",fg="white",bd=2,relief="solid",  cursor="hand2")
        back_btn.place(relx=0.9, y=600-85, width=100, height=40)
    
    def go_back(self):
        # Define the action when back is clicked, you can change this to whatever you need (e.g., closing the window or going to a previous screen)
        self.root.destroy()  # This will close the current window



    #=====================Attendance===================

    def mark_attendance(self, i, r, n):
        file_path = "attendance.csv"
        # if not os.path.exists(file_path):
        #     with open(file_path, "w",newline="") as f:
        #         writer = csv.writer(f)
        #         writer.writerow(["Student_ID", "Roll_No", "Name", "Time", "Date", "Status"])  # Headers

        now=datetime.now()
        time_now=now.strftime("%H:%M:%S")
        date_now=now.strftime("%d/%m/%Y")

        if not os.path.exists(file_path):
            with open(file_path, "w",newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Student_ID", "Roll_No", "Name", "Time", "Date", "Status"])  # Headers



    
    # Read existing data
        existing_records=set()
        with open(file_path, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader,None)  # Skip header
            for row in reader:
              if row and row[0]==str(i) and row[4]==date_now:  # Ensure row is not empty
                existing_records.add((row[0], row[4]))  # (Student_ID, Date)





            # name_list = [line.strip().split(",")for line in myDatalist[1:] if line.strip()]

            # Extract (Student_ID, Date) pairs from the existing records



    # Append new entry if not already present
# Append new entry only if the student is not already marked today
        if (str(i), date_now) not in existing_records:
            with open(file_path, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([i, r, n, time_now, date_now, "Present"])
            print(f"✅ Attendance Marked: {i}, {r}, {n}, {time_now}, {date_now}, Present")  # Debugging Line
        
        else:
            print(f"⚠️ Attendance already marked for {n} ({i}) on {date_now}")  # Debugging Line



    #================face recognition==================
    def face_recog(self):
        def draw_boundray(img,classifier,scaleFactor,minNeighbors,color,text,clf):
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            featuers=classifier.detectMultiScale(gray_image,scaleFactor,minNeighbors)

            coord=[]
            
            for (x,y,w,h) in featuers:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
                id,predict=clf.predict(gray_image[y:y+h,x:x+w])

                confidence=int((100*(1-predict/300)))

                conn = mysql.connector.connect(username='root', password='root',host='localhost',database='face_recognition',port=3306)
                cursor = conn.cursor()

                cursor.execute("select Name from student where Student_ID=%s",(id,))
                n=cursor.fetchone()
                # n="+".join(n)

                if n is not None:
                    n = n[0]  # Get the first element from the tuple
                else:
                    n = "Unknown"  # Default value in case the student is not found


                cursor.execute("select Roll_No from student where Student_ID="+str(id))
                r=cursor.fetchone()
                # r="+".join(r)
                r = r[0] if r else "Unknown"


                cursor.execute("select Student_ID from student where Student_ID="+str(id))
                i=cursor.fetchone()
                # i="+".join(i)
                i = i[0] if i else "Unknown"


                if confidence > 50 and i !="Unknown":
                    cv2.putText(img,f"Student_ID:{i}",(x,y-80),cv2.FONT_HERSHEY_COMPLEX,0.8,(64,15,223),2)
                    cv2.putText(img,f"Name:{n}",(x,y-55),cv2.FONT_HERSHEY_COMPLEX,0.8,(64,15,223),2)
                    cv2.putText(img,f"Roll-No:{r}",(x,y-30),cv2.FONT_HERSHEY_COMPLEX,0.8,(64,15,223),2)
                    self.mark_attendance(i,r,n)
                else:
                    cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),3)
                    cv2.putText(img,"Unknown Face",(x,y-5),cv2.FONT_HERSHEY_COMPLEX,0.8,(255,255,0),3)    

                coord=[x,y,w,h]
            
            return coord    


        #==========
        def recognize(img,clf,faceCascade):
            coord=draw_boundray(img,faceCascade,1.1,10,(255,25,255),"Face",clf)
            return img
        
        faceCascade=cv2.CascadeClassifier(r"C:\Users\user\Documents\Python_Test_Projects\haarcascade_frontalface_default.xml")
        clf=cv2.face.LBPHFaceRecognizer_create()
        clf.read(r"C:\Users\user\Documents\Python_Test_Projects\clf.xml")


        videoCap=cv2.VideoCapture(0)

        while True:
            ret,img=videoCap.read()
            img=recognize(img,clf,faceCascade)
            cv2.imshow("Face Detector",img)

            if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Face Detector", cv2.WND_PROP_VISIBLE) < 1:
                break
        videoCap.release()
        cv2.destroyAllWindows()




if __name__ == "__main__":
    root=Tk()
    obj=Face_Recognition(root)
    root.mainloop()
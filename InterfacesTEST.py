#For attendance 
#https://www.youtube.com/watch?v=4BZL3cF_Dww
import csv
import datetime
import mimetypes
import os
import win32api
import win32gui
import re
_GETIMAGE = 0x01


#email
import smtplib
import sqlite3
import sys
import time
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import cv2
import face_recognition
import numpy as np


#voice
import speech_recognition as sr
from threading import Thread
import pyaudio

#pyqt for interfaces library
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import QDate, Qt, QTimer, pyqtSlot, QThread,QObject,pyqtSignal, QSize
from PyQt5.QtGui import *
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QWidget
from PyQt5.uic import loadUi
from PyQt5.QtGui import QFont


import sys
from PyQt5.QtWidgets import QWidget,QPushButton,QApplication,QListWidget,QGridLayout,QLabel
from PyQt5.QtCore import QTimer,QDateTime
from pyqtconfig import ConfigManager
import as608_combo_lib as as608

conn = sqlite3.connect("Cognito.db")
class WelcomeScreen(QDialog):
    def __init__(self):
        super(WelcomeScreen, self).__init__()
        loadUi("FirstIn.ui",self)
        
        self.InstructorLoginButton.clicked.connect(self.gotoInstrScr)
        self.StudentLoginButton.clicked.connect(self.gotoStudenScr)
        self.StudentRegisterButton.clicked.connect(self.gotoStudentRegister)
        self.RegisterInstrcButton.clicked.connect(self.gotoRegisterInstructor)
        self.AdminLogin.clicked.connect(self.gotoAdmin)
    
         
    def gotoInstrScr(self):
        widget.setCurrentIndex(1)
    
    def gotoStudentRegister(self):
        widget.setCurrentIndex(2)

    def gotoRegisterInstructor(self):
        widget.setCurrentIndex(3)

    def gotoStudenScr(self):
        widget.setCurrentIndex(4)

    def gotoAdmin(self):
        widget.setCurrentIndex(9)

        
##################################################################################################################################
class InstructorLogin(QDialog):
    def __init__(self):
        super(InstructorLogin, self).__init__()
        loadUi("NewInstructorLogin.ui",self)
        self.user=None
        self.LoginInst.clicked.connect(self.gotoAfterInstLogin)
        self.ExitLoginInst.clicked.connect(self.gotoMainExit1)
        self.PmuPassInstButton.setEchoMode(QtWidgets.QLineEdit.Password)
        self.ExitLoginInst.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.ExitLoginInst.setIconSize(QSize(45,45))

        
     #For the password  
    def gotoAfterInstLogin(self):
        self.user = self.PmuIDInstButton.text()
        password = self.PmuPassInstButton.text()
    
        if len(self.user)==0 or len(password)==0:
            self.InvalidPassLab.setText("Please input all fields.")

        else:
                conn = sqlite3.connect("Cognito.db")
                cur = conn.cursor()
                queryID = 'SELECT Instructor_id FROM Instructor WHERE Instructor_id =\''+self.user+"\'"
            
                result=cur.execute(queryID).fetchall()

                if result:
                
                    #if self.user in y:
                        conn.commit()

                        conn = sqlite3.connect("Cognito.db")
                        cur  = conn.cursor()
                        query = 'SELECT Password FROM Instructor WHERE Instructor_id =\''+self.user+"\'"
                        cur.execute(query)
                        conn.commit()

                        result_pass = cur.fetchone()[0] #to compare password 
                        if result_pass == password:
                            widget.addWidget(ChooseCourseInst(self.user))
                            #widget.setCurrentIndex(27)
                            widget.setCurrentIndex(widget.count()-1)
                            self.PmuIDInstButton.setText("")
                            self.PmuPassInstButton.setText("")
                            self.InvalidPassLab.setText("")
        
                        else:
                            self.InvalidPassLab.setText("Invalid password")
                    # else:
                    #         self.InvalidPassLab.setText("Invalid password")

                else:
                    self.InvalidPassLab.setText("User does not exist")
                    
       
    def gotoMainExit1(self):
        self.PmuIDInstButton.setText("")
        self.PmuPassInstButton.setText("")
        self.InvalidPassLab.setText("")
        widget.setCurrentIndex(0)

########################################################################################################################
class ChooseCourseInst(QMainWindow):

    def __init__(self,user1):
        self.user1=user1
        super(ChooseCourseInst, self).__init__()
        loadUi("CoursesChosenInt.ui",self)  
        self.courses()
        self.Exit.clicked.connect(self.gotoexitCourse)
        self.coursesreq.activated.connect(self.gotoInstServButton)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))

    def courses(self):
        conn = sqlite3.connect("Cognito.db")
        query = 'SELECT DISTINCT Course_name FROM Course WHERE Instructor_id =\''+self.user1+"\'"
       
       
        cur = conn.cursor()
        conn.commit()
        cur.execute(query)
        final_result = [i[0] for i in cur.fetchall()]
        for i in range(len(final_result)):
            self.coursesreq.addItem(final_result[i])

    def gotoexitCourse(self):
        widget.setCurrentIndex(0)

    def gotoInstServButton(self):
        self.course=self.coursesreq.currentText()
        #afterInstructorLogin=AfterInstructorLogin(self.user1, self.course)
        widget.addWidget(AfterInstructorLogin(self.user1, self.course))
        widget.setCurrentIndex(widget.count()-1)

##################################################################################################################################
class StudentLogin(QDialog):
    def __init__(self):
        super(StudentLogin, self).__init__()
        loadUi("NewStudentLogin.ui",self)
        self.userStudent=None
        self.Exit.clicked.connect(self.gotoExit)
        self.LoginSTButton.clicked.connect(self.gotoLoginST)
        self.AttendanceTakenButton.clicked.connect(self.gotoAttendanceTakenButton)
        self.PmuPassST.setEchoMode(QtWidgets.QLineEdit.Password) #for the student pass 
        self.AttendanceTakenButtonFP.clicked.connect(self.gotoattendancebyfingerprint)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))


    def gotoLoginST(self):
        self.userStudent = self.PmuStID.text()
        password = self.PmuPassST.text()

        if len(self.userStudent)==0 or len(password)==0:
            self.InvalidPassLab.setText("Please input all fields.")

        else:
                conn = sqlite3.connect("Cognito.db")
                cur = conn.cursor()
                queryID = 'SELECT Student_ID FROM StudentN WHERE Student_ID =\''+self.userStudent+"\'"
            
                result=cur.execute(queryID).fetchall()

                if result:
                
                    #if self.user in y:
                        conn.commit()

                        conn = sqlite3.connect("Cognito.db")
                        cur  = conn.cursor()
                        query = 'SELECT Password FROM StudentN WHERE Student_ID =\''+self.userStudent+"\'"
                        cur.execute(query)
                        conn.commit()

                        result_pass = cur.fetchone()[0] #to compare password 
                        if result_pass == password:
                            widget.addWidget(ChoseCourseStudent(self.userStudent))
                            self.PmuStID.setText("")
                            self.PmuPassST.setText("")
                            self.InvalidPassLab.setText("")
                            widget.setCurrentIndex(widget.count()-1)
                
        
                        else:
                            self.InvalidPassLab.setText("Invalid password")

                else:
                    self.InvalidPassLab.setText("User does not exist")
    

    def gotoExit(self):
        widget.setCurrentIndex(0)

    def gotoAttendanceTakenButton(self):
        widget.setCurrentIndex(6) 

    def gotoattendancebyfingerprint(self):
        widget.setCurrentIndex(5)  
################################################################################################################
class AfterLoginStudent(QDialog):
    def __init__(self, userid, coursestu):
        self.userid=userid
        self.coursestu=coursestu
        super(AfterLoginStudent, self).__init__()
        loadUi("CoosingAttOrClassNote.ui",self)
        self.username.setText(self.userid)
        self.crs.setText(self.coursestu)
        self.Exit.clicked.connect(self.gotoExit)
        self.AttendanceRecordStButton.clicked.connect(self.gotoStudentAttendanceRecord)
        self.ClassNoteStuButton.clicked.connect(self.gotoStudentClassNote)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.GoBack.clicked.connect(self.gotoGoBack)


    def gotoStudentAttendanceRecord(self):
        widget.addWidget(StudentAttendanceRecord(self.userid, self.coursestu))
        widget.setCurrentIndex(widget.count()-1)
        
    def gotoStudentClassNote(self):
        widget.addWidget(StudentClassNote(self.userid, self.coursestu))
        widget.setCurrentIndex(widget.count()-1)

    def gotoExit(self):
        widget.setCurrentIndex(0) 
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
    def gotoGoBack(self):
            
            widget.setCurrentIndex(widget.count()-2)
            print(widget.count()) 
            n=13
            for i in range(n):
                wid = widget.widget(n)
                widget.removeWidget(wid)   
            print(widget.count())     

##################################################################################################################################  
class StudentAttendanceRecord(QDialog):
    def __init__(self, userID, coursestd):
        self.userID=userID
        self.coursestd=coursestd
        super(StudentAttendanceRecord, self).__init__()
        loadUi("AttendanceOneStInterface.ui",self)
        self.username.setText(self.userID)
        self.crs.setText(self.coursestd)
        self.Exit.clicked.connect(self.gotoExit)
        self.GoBack.clicked.connect(self.gotoGoBack_StuAttendance)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))


        self.attStTable.setColumnWidth(0,200)
        self.attStTable.setColumnWidth(1,100)
        self.attStTable.setColumnWidth(2,200)
        self.attStTable.setColumnWidth(3,100)
        self.attStTable.setColumnWidth(4,400)
        self.attStTable.setHorizontalHeaderLabels(["Name", "Student_id","Date_Time","Status","Course_name"])
        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        #query = 'SELECT * FROM Attendance WHERE Student_id =\''+self.userID+"\' AND Student_id =\''+self.userID+"\''
        query=f"""SELECT * FROM Attendance WHERE Student_id ='{self.userID}' AND Course_name ='{self.coursestd}'"""
        #query="SELECT * FROM Attendance WHERE Student_id ='201801636' AND Course_name = 'Robotics LAB 210"

        self.attStTable.setRowCount(10)
        tablecount=0
        results = cur.execute(query)
        conn.commit()
        for row in results:
            self.attStTable.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.attStTable.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.attStTable.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.attStTable.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.attStTable.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4])) 
            tablecount+=1

    def gotoExit(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   

    def gotoGoBack_StuAttendance(self):
       
        widget.setCurrentIndex(widget.count()-2)
        print(widget.count()) 
        n=14
        
        for i in range(n):
            print(f"i: {i}")
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 

        #widget.setCurrentIndex(18)    
################################################################################################################################## 
class StudentClassNote(QMainWindow):
    def __init__(self, user, course):
        self.user=user
        self.course=course
        super(StudentClassNote, self).__init__()
        loadUi("ClassNoteStu.ui",self)
        self.username.setText(self.user)
        self.crs.setText(self.course)
        self.ClassNoteTableStu.setColumnWidth(0,600)
        self.ClassNoteTableStu.setColumnWidth(1,100)
        self.SendEmailButton.clicked.connect(self.gotoSendEmailButtonst)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))


        

        self.Exit.clicked.connect(self.gotoMainExit)
        self.GoBack.clicked.connect(self.gotoGoBack_StuClassNotes)
        self.ClassNoteTableStu.setHorizontalHeaderLabels(["Content","Course Name"])

        self.gotoLecNoteStud(self)
        
    def gotoLecNoteStud(self,conn):
         #########checknotes:#######
        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT Content, Course_Name FROM Notes_Instructor WHERE Course_name =\''+self.course+"\'"
       
        
        self.ClassNoteTableStu.setRowCount(10)

        tablecount=0
        #cur.execute(query)
        results = cur.execute(query)
        
        for row in results:
            self.ClassNoteTableStu.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.ClassNoteTableStu.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
             
            tablecount+=1

    def gotoGoBack_StuClassNotes(self):
      
        widget.setCurrentIndex(widget.count()-2)
        print(widget.count()) 
        n=13
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
         

    def gotoMainExit(self):
        widget.setCurrentIndex(0) 
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   

    def gotoSendEmailButtonst(self):
        text=self.textEditnotes.toPlainText()

        emailfrom = "cognito.pmu@gmail.com"
        emailto = self.user+"@pmu.edu.sa"
        print(text, file=open("Class_Notes.txt","w"))
        fileToSend = "Class_Notes.txt"

        username = "cognito.pmu@gmail.com"
        password = 'yvptzapuawnbdvpx'

      

        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = "Class Notes: "+ self.course
        msg.preamble = "Class Notes: "+ self.course

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()
  
###############################################################################################################################
class ChoseCourseStudent(QMainWindow):
    def __init__(self, userStudent1):
        self.userStudent1=userStudent1
        super(ChoseCourseStudent, self).__init__()
        loadUi("StudentCourses.ui",self)
        self.Exit.clicked.connect(self.gotoexitstbutt)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))

        self.coursesreqstu.activated.connect(self.gotoStServButton)
        self.coursesStudent()
        
    def gotoStServButton(self):
        self.coursestu=self.coursesreqstu.currentText()
        widget.addWidget(AfterLoginStudent(self.userStudent1, self.coursestu))
        widget.setCurrentIndex(widget.count()-1)  

    def gotoexitstbutt(self):
       widget.setCurrentIndex(0) 
       n=11
       for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
    
        
    def coursesStudent(self):
        conn = sqlite3.connect('Cognito.db')
        cur = conn.cursor()

        query = 'SELECT DISTINCT Course_name FROM Course WHERE Student_id =\''+self.userStudent1+"\'"

        cur.execute(query)
        final_result = [i[0] for i in cur.fetchall()]
        for i in range(len(final_result)):
            self.coursesreqstu.addItem(final_result[i])
        
################################################################################################################################## 
class StudentRegister(QMainWindow):
    def __init__(self):
        super(StudentRegister, self).__init__()
        loadUi("StudentRegistration.ui",self)
        self.Exit.clicked.connect(self.gotoMainExit3)
        self.SubmitStu.clicked.connect(self.gotoSubmitStu)
        self.RigesterFinger.clicked.connect(self.gotoFingerprintForRegestration)
        self.RegisterMyFace.clicked.connect(self.gotoFaceRecogForReg)
        self.passStu.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))

        

    def gotoFingerprintForRegestration(self):
        widget.setCurrentIndex(7)

    def gotoFaceRecogForReg(self):
        widget.setCurrentIndex(8)



    def gotoSubmitStu(self):
        fname = self.firstNameStu.text()
        mname = self.middleNameStu.text()
        lname = self.lastNameIns.text()
        pmu_id = self.pmuIDStu.text()
        email = self.pmuEmailStu.text()
        major = self.majorStu.currentText()
        level = self.levelStu.currentText()
        password = self.passStu.text()
        confirm_password = self.confPass.text()

        if len(fname)==0 or len(mname )==0 or len(lname)==0 or len(pmu_id)==0 or len(email)==0 or len(major)==0 or len(level)==0 or len(password)==0 or len(confirm_password)==0:
            mbox=QMessageBox()
            mbox.information(self,"Warning","Please Input all fields")
        else:    

            if (confirm_password==password):
            
                
                    # if (len(password)<6):
                    #         self.invalidMsgSt.setText("Password length should be not less than 6")
                            
                    # elif not re.search("[a-z]",password):
                    #         self.invalidMsgSt.setText("Password must include lower case")
                            
                    # elif not re.search("[A-Z]", password):
                    #         self.invalidMsgSt.setText("Password must include at least 1 captial letter")
                            
                    # elif not re.search("[0-9]", password):
                    #         self.invalidMsgSt.setText("Password must include at least 1 number")
                            
                    # else:
        
                
                        conn = sqlite3.connect("Cognito.db")
                        with conn:
                            cur=conn.cursor()
                            cur.execute("INSERT INTO StudentN(First_Name, Middle_Name, Last_Name, Student_ID, Email, Major, Level, Password)"
                                        "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (''.join(fname),
                                                                ''.join(mname),
                                                                ''.join(lname),
                                                                ''.join(pmu_id),
                                                                ''.join(email),
                                                                ''.join(major),
                                                                ''.join(level),
                                                                ''.join(password)
                                                                ))
                        # widget.addWidget(RegisterFacialStInDB(pmu_id))
                        # widget.setCurrentIndex(widget.count()-1)   
                #widget.setCurrentIndex(10)  
            

            else:
                self.invalidMsgSt.setText("Passwords do not match.")


    def gotoMainExit3(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid) 
        print(widget.count())      
##################################################################################################################################
class InstructorRegister(QDialog):
    def __init__(self):
        super(InstructorRegister, self).__init__()
        loadUi("InstructorReg.ui",self)
        self.Exit.clicked.connect(self.gotoExit)
        self.SubmitInstButton.clicked.connect(self.gotoSubmitInstButton)
        self.passIns.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confPassIns.setEchoMode(QtWidgets.QLineEdit.Password)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))


    def gotoSubmitInstButton(self):
        fname = self.firstNameIns.text()
        lname = self.lastNameIns.text()
        pmu_id = self.pmuIDIns.text()
        email = self.pmuEmailIns.text()
        college = self.collegeIns.currentText()
        dept = self.deptIns.text()
        password = self.passIns.text()
        confirm_password=self.confPassIns.text()

#Enter Courses
        inputs=[self.Course1.text(), self.Course2.text(), self.Course3.text(), 
        self.Course4.text(), self.Course5.text(), self.Course6.text(),
        self.Course7.text(), self.Course8.text()]

        courses=[]

        for i in range(8):
            if len(inputs[i]) != 0:
                courses.append(inputs[i])   
        

        if len(fname)==0 or len(lname)==0 or len(pmu_id)==0 or len(email)==0 or len(college)==0 or len(dept)==0 or len(password)==0 or len(confirm_password)==0 or len(courses)==0:
            self.invalidMsg.setText("Please input all fields.")

        else:    

            if (confirm_password == password):
                conn = sqlite3.connect("Cognito.db")
                with conn:
                    cur=conn.cursor()
                    cur.execute("INSERT INTO Instructor(First_name, Last_name, Instructor_id, Email, College, Department, Password)"
                                "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (''.join(fname),
                                                        ''.join(lname),
                                                        ''.join(pmu_id),
                                                        ''.join(email),
                                                        ''.join(college),
                                                        ''.join(dept),
                                                        ''.join(password)
                                                        ))
                    for i in range(len(courses)):
                        cur.execute("INSERT INTO Course(Course_name, Instructor_id)"
                                "VALUES('%s', '%s')" % (''.join(courses[i]),
                                                        ''.join(pmu_id)
                                                        ))
                                                            

                widget.setCurrentIndex(widget.currentIndex()-2)  
            else: 
                self.invalidMsg.setText("Passwords do not match")


    def gotoExit(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid) 
             
##################################################################################################################################
class AfterInstructorLogin(QMainWindow):
    def __init__(self, user, course):
        self.course=course
        self.user=user
        super(AfterInstructorLogin, self).__init__()
        loadUi("AfterInstructorLogin.ui",self)
        self.username.setText(self.user)
        self.crs.setText(self.course)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))

        self.CheckNoteInsButton.clicked.connect(self.gotoClassNote)
        self.CheckAttendanceInsButton.clicked.connect(self.gotoAttendance)
        self.setexamButton.clicked.connect(self.gotoSetExam)
        self.Exit.clicked.connect(self.gotoExitLoginInstButton)
        self.GoBack.clicked.connect(self.gotoGoBack)
        self.RecordLecturebtn.clicked.connect(self.gotoStartRecordLecture)
        self.Gradesbtn.clicked.connect(self.gotoGradeCenter)

    def gotoClassNote(self):
            widget.addWidget(ClassNoteIns(self.user,self.course))
            widget.setCurrentIndex(widget.count()-1)

    def gotoAttendance(self):
        widget.addWidget(AttendanceIns(self.user,self.course))
        widget.setCurrentIndex(widget.count()-1)

    def gotoSetExam(self):
            
            widget.addWidget(ExamSetup(self.user,self.course))
            widget.setCurrentIndex(widget.count()-1)
    
    def gotoExitLoginInstButton(self):
        widget.setCurrentIndex(0)
            
            
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)

    def gotoGradeCenter(self):
        widget.addWidget(ViewGrades(self.user,self.course))
        widget.setCurrentIndex(widget.count()-1)

               
    def gotoStartRecordLecture(self):
        widget.addWidget(RecordLectureInst(self.user,self.course))
        widget.setCurrentIndex(widget.count()-1)

    def gotoGoBack(self):
            widget.setCurrentIndex(widget.count()-2)
            print(widget.count()) 
            n=13
            for i in range(n):
                wid = widget.widget(n)
                widget.removeWidget(wid)   
            print(widget.count()) 
       
##################################################################################################################################
class ClassNoteIns(QMainWindow):
    def __init__(self, user, course):
        self.user=user
        self.course=course
        super(ClassNoteIns, self).__init__()
        loadUi("ClassNoteInstr.ui",self)
        self.username.setText(self.user)
        self.crs.setText(self.course)
        self.ClassNoteTableInst.setColumnWidth(0,400)
        self.ClassNoteTableInst.setColumnWidth(1,100)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))

        self.sendemail.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\sendee.png"))
        self.sendemail.setIconSize(QSize(50,45))

        
        self.Exit.clicked.connect(self.gotoMainExit5)
        self.GoBack.clicked.connect(self.gotoGoBack_InsNote)
        self.ClassNoteTableInst.setHorizontalHeaderLabels(["Content.", "Course Name","Content"])
        self.gotoLec1InButtonRobo(self)
        self.sendemail.clicked.connect(self.GotoSendemail)

    def gotoMainExit5(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid) 

        print(widget.count())      

    def gotoGoBack_InsNote(self):
        widget.setCurrentIndex(widget.count()-2)
        print(widget.count()) 
        n=13
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 
        
        #widget.setCurrentIndex(11)

    def gotoLec1InButtonRobo(self,conn):

        #########checknotes:#######
        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT Content, Course_Name FROM Notes_Instructor WHERE Course_name =\''+self.course+"\'"
       
        
        self.ClassNoteTableInst.setRowCount(10)

        tablecount=0
        #cur.execute(query)
        results = cur.execute(query)
        
        for row in results:
            self.ClassNoteTableInst.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.ClassNoteTableInst.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
             
            tablecount+=1

    def id_to_email(self, l):
        for i in range(len(l)):
            l[i] = l[i] + "@pmu.edu.sa"      

    def GotoSendemail(self):

        text=self.EditSendRevise.toPlainText()

        emailfrom = "cognito.pmu@gmail.com"
        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query= f"""SELECT Student_id FROM Course WHERE Instructor_id='{self.user}' AND Course_name='{self.course}'"""
        cur.execute(query)
        res = cur.fetchall()
        y=[i[0] for i in res] 
        self.id_to_email(y)
        x=",".join(y)
        print(text, file=open("Class_Notes.txt","w"))
        fileToSend = "Class_Notes.txt"

        username = "cognito.pmu@gmail.com"
        password = 'yvptzapuawnbdvpx'


        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = x #emailto
        msg["Subject"] = "Class Notes: "+ self.course
        msg.preamble = "Class Notes: "+ self.course

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, y, msg.as_string())
        server.quit()

        ########################

         
        #result_pass = cur.fetchone()[0] #to compare password 

##################################################################################################################################   


class AttendanceIns(QMainWindow):
    def __init__(self, user, course):
        self.user=user
        self.course=course

        

        super(AttendanceIns, self).__init__()

        loadUi("AttendanceRecordIns.ui",self)
         #Exit button
        self.username.setText(self.user)
        self.crs.setText(self.course)
        self.Exit.clicked.connect(self.gotoExit)
        self.GoBack.clicked.connect(self.gotoGoBack_InsAttendance)
        self.attendanceInstTable.setColumnWidth(0,200)
        self.attendanceInstTable.setColumnWidth(1,100)
        self.attendanceInstTable.setColumnWidth(2,200)
        self.attendanceInstTable.setColumnWidth(3,100)
        self.attendanceInstTable.setColumnWidth(4,400)
        self.attendanceInstTable.setHorizontalHeaderLabels(["Name", "Student_id","Date_Time","Status","Course_name"])
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
    
        self.sendemail.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\sendee.png"))
        self.sendemail.setIconSize(QSize(50,45))
        self.sendemail.clicked.connect(self.gotoSendEmailButtonst)

        self.GoBack.setIconSize(QSize(45,45))



        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT * FROM Attendance WHERE Course_name =\''+self.course+"\'"
        self.attendanceInstTable.setRowCount(10)
        tablecount=0
        results = cur.execute(query)
        conn.commit()
        for row in results:
            self.attendanceInstTable.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.attendanceInstTable.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.attendanceInstTable.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.attendanceInstTable.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.attendanceInstTable.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4])) 
            tablecount+=1


    def gotoGoBack_InsAttendance(self):
        widget.setCurrentIndex(widget.count()-2)
        print(widget.count()) 
        n=13
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 

    def gotoExit(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid) 
    def gotoLecNoteStud(self,conn):
         #########checknotes:#######
        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT Content, Course_Name FROM Notes_Instructor WHERE Course_name =\''+self.course+"\'"
       
        
        self.ClassNoteTableStu.setRowCount(10)

        tablecount=0
        #cur.execute(query)
        results = cur.execute(query)
        
        for row in results:
            self.ClassNoteTableStu.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.ClassNoteTableStu.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
             
            tablecount+=1

    def gotoGoBack_StuClassNotes(self):
        widget.setCurrentIndex(widget.count()-2)
        print(widget.count()) 
        n=13
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count())    

    def gotoMainExit(self):
        widget.setCurrentIndex(0) 
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   

    def gotoSendEmailButtonst(self):
        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT * FROM Attendance WHERE Course_name =\''+self.course+"\'"
        # cur.execute(query)
        # res = cur.fetchall()
        # y=[i[0] for i in res] 
        # x=",".join(y)
        #print(text, file=open("Class_Notes.txt","w"))
        fileToSend = f"Attendance_Record:{self.course}.csv" 

        cur.execute(query)
        rows = cur.fetchall()
    

    # Continue only if there are rows returned.
        if rows:
            # New empty list called 'result'. This will be written to a file.
            result = list()

            # The row name is the first entry for each entity in the description tuple.
            column_names = list()
            for i in cur.description:
                column_names.append(i[0])

            result.append(column_names)
            for row in rows:
                result.append(row)

            # Write result to file.
            with open(fileToSend, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in result:
                    csvwriter.writerow(row)



        emailfrom = "cognito.pmu@gmail.com"
        #emailto = self.user+"@pmu.edu.sa"
        emailto = self.user+"@pmu.edu.sa"
       
        
        # print(x, file=open("Attendance_Record.csv","w"))
        # csv_reader = csv.reader(x, delimiter=',')

        #fileToSend = "Attendance_Record.csv"

        username = "cognito.pmu@gmail.com"
        password = 'yvptzapuawnbdvpx'

      

        msg = MIMEMultipart()
        msg["From"] = emailfrom
        msg["To"] = emailto
        msg["Subject"] = "Class Notes: "+ self.course
        msg.preamble = "Class Notes: "+ self.course

        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fp = open(fileToSend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "image":
            fp = open(fileToSend, "rb")
            attachment = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == "audio":
            fp = open(fileToSend, "rb")
            attachment = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(fileToSend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fp.read())
            fp.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
        msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(username,password)
        server.sendmail(emailfrom, emailto, msg.as_string())
        server.quit()  


   

#########################################################################################################################
class ExamSetup(QDialog):
    def __init__(self, user, course):
        self.user=user
        self.course=course
        super(ExamSetup, self).__init__()
        loadUi("SetUpExam2.ui",self)
        self.username.setText(self.user)
        self.crs.setText(self.course)
        self.Exit.clicked.connect(self.gotoMainExit7)
        self.GoBack.clicked.connect(self.gotoGoBack_InsExamsetup)
        self.closetimerload.clicked.connect(self.closetimerforloadimage)
        self.SubmitExam.clicked.connect(self.destory)
        self.PressLoadingImageButton.clicked.connect(self.LoadingImageButton)
        self.CorrectExambutton.clicked.connect(self.CorrectExambuttonf)
        self.submitans.clicked.connect(self.submitanss)
        self.submitgrades.clicked.connect(self.GoTosubmitgrades)
        self.showAllStudents.setHorizontalHeaderLabels(["First name","Last name","Student ID","Grade"])
        self.showAllStudents.setColumnWidth(0,70)
        self.showAllStudents.setColumnWidth(1,75)
        self.showAllStudents.setColumnWidth(2,75)
        self.showAllStudents.setColumnWidth(3,50)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        

        self.image=None

        
        conn = sqlite3.connect("Cognito.db")
        cur = conn.cursor()
        #query = 'SELECT Student_ID,First_Name,Last_Name, Course_name FROM StudentN,Course WHERE Course_name =\''+self.course+"\'"
        query='SELECT First_Name,Last_Name, StudentN.Student_ID FROM StudentN, Course WHERE StudentN.Student_ID=Course.Student_id AND Course.Course_name=\''+self.course+"\'"
        self.showAllStudents.setRowCount(7)

        tablecount=0
        results = cur.execute(query)
        
        for row in results:
            self.showAllStudents.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.showAllStudents.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.showAllStudents.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
           
            tablecount+=1

    def  submitanss(self):
        global ans
        global questions
        questions=self.numofques.value()

        ans= [self.Ans1S.value(), self.Ans2S.value(),self.Ans3S.value(),
              self.Ans4S.value(),self.Ans5S.value(), self.Ans6S.value(), 
              self.Ans7S.value(),self.Ans8S.value(),self.Ans9S.value(),
              self.Ans10S.value(), self.Ans11S.value(), self.Ans12S.value(),
              self.Ans13S.value(),self.Ans14S.value(),self.Ans15S.value(),
              self.Ans16S.value(), self.Ans17S.value(),self.Ans18S.value(),
              self.Ans19S.value(),self.Ans20S.value()]

        global ans2

        ans2=[]
        for i in range(len(ans)):
            if ans[i]!=None:
                ans2.append(ans[i])
            break   
###########From here to load image and displat it###############
    def LoadingImageButton(self):
        global readimg
        global capture
        capture = cv2.VideoCapture(0)
        ret, image = capture.read()


        self.timer = QTimer(self)  # Create Timer
        self.timer.timeout.connect(self.update_frame_for_Losding)
        self.timer.start(10)
        readimg=cv2.imwrite(f"C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ExamImagesDataset\\{self.user}.png",image)
    def update_frame_for_Losding(self):
        ret, self.imageLoad = capture.read()
        self.displayImage_Loading(self.imageLoad, 1)

    def displayImage_Loading(self, imageLoad,window=1) :
        imageLoad = cv2.resize(imageLoad, (640, 480))
        #convert it using qt format
        qformat = QImage.Format_Indexed8
        if len(imageLoad.shape) == 3:
            if imageLoad.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(imageLoad, imageLoad.shape[1], imageLoad.shape[0], imageLoad.strides[0], qformat)
        outImage = outImage.rgbSwapped()
        if window == 1:
            self.Loadimage.setPixmap(QPixmap.fromImage(outImage))
            self.Loadimage.setScaledContents(True)

    def closetimerforloadimage(self):
        self.timer.stop()
        capture.release()
###########From here to load image and displat it###############

    def CorrectExambuttonf(self):
        QApplication.processEvents()

        global img
        global cap
        global score
        global imageCap
        import utlis
        heightImg = 400
        widthImg  = 400

        webCamFeed = True
        cap = cv2.VideoCapture(1)
        ret, imageCap = cap.read()

        self.timer = QTimer(self)  # Create Timer
        self.timer.start(10)
        
        ReadStud=cv2.imwrite(f"C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ExamStudent\\{self.user}.png",imageCap)

        pathImage=readimg

        choices=5
        count=0
        while True:

            if webCamFeed:success, img = cap.read()
            else:
                img = cv2.imread(pathImage)
            print(pathImage)
        
            img = cv2.resize(img, (widthImg, heightImg)) # RESIZE IMAGE
            imgFinal = img.copy()
            imgBlank = np.zeros((heightImg,widthImg, 3), np.uint8) # CREATE A BLANK IMAGE FOR TESTING DEBUGGING IF REQUIRED
            imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # CONVERT IMAGE TO GRAY SCALE
            imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1) # ADD GAUSSIAN BLUR
            imgCanny = cv2.Canny(imgBlur,10,70) # APPLY CANNY 

            try:
                ## FIND ALL COUNTOURS
                imgContours = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
                imgBigContour = img.copy() # COPY IMAGE FOR DISPLAY PURPOSES
                contours, hierarchy = cv2.findContours(imgCanny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # FIND ALL CONTOURS
                cv2.drawContours(imgContours, contours, -1, (0, 255, 0), 10) # DRAW ALL DETECTED CONTOURS
                rectCon = utlis.rectContour(contours) # FILTER FOR RECTANGLE CONTOURS
                biggestPoints= utlis.getCornerPoints(rectCon[0]) # GET CORNER POINTS OF THE BIGGEST RECTANGLE
                gradePoints = utlis.getCornerPoints(rectCon[1]) # GET CORNER POINTS OF THE SECOND BIGGEST RECTANGLE

                

                if biggestPoints.size != 0 and gradePoints.size != 0:

                    # BIGGEST RECTANGLE WARPING
                    biggestPoints=utlis.reorder(biggestPoints) # REORDER FOR WARPING
                    cv2.drawContours(imgBigContour, biggestPoints, -1, (0, 255, 0), 20) # DRAW THE BIGGEST CONTOUR
                    pts1 = np.float32(biggestPoints) # PREPARE POINTS FOR WARP
                    pts2 = np.float32([[0, 0],[widthImg, 0], [0, heightImg],[widthImg, heightImg]]) # PREPARE POINTS FOR WARP
                    matrix = cv2.getPerspectiveTransform(pts1, pts2) # GET TRANSFORMATION MATRIX
                    imgWarpColored = cv2.warpPerspective(img, matrix, (widthImg, heightImg)) # APPLY WARP PERSPECTIVE

                    # SECOND BIGGEST RECTANGLE WARPING
                    cv2.drawContours(imgBigContour, gradePoints, -1, (255, 0, 0), 20) # DRAW THE BIGGEST CONTOUR
                    gradePoints = utlis.reorder(gradePoints) # REORDER FOR WARPING
                    ptsG1 = np.float32(gradePoints)  # PREPARE POINTS FOR WARP
                    ptsG2 = np.float32([[0, 0], [325, 0], [0, 150], [325, 150]])  # PREPARE POINTS FOR WARP
                    matrixG = cv2.getPerspectiveTransform(ptsG1, ptsG2)# GET TRANSFORMATION MATRIX
                    imgGradeDisplay = cv2.warpPerspective(img, matrixG, (325, 150)) # APPLY WARP PERSPECTIVE

                    # APPLY THRESHOLD
                    imgWarpGray = cv2.cvtColor(imgWarpColored,cv2.COLOR_BGR2GRAY) # CONVERT TO GRAYSCALE
                    imgThresh = cv2.threshold(imgWarpGray, 170, 255,cv2.THRESH_BINARY_INV )[1] # APPLY THRESHOLD AND INVERSE

                    boxes = utlis.splitBoxes(imgThresh) # GET INDIVIDUAL BOXES
                    #cv2.imshow("Split Test ", boxes[3])
                    countR=0
                    countC=0
                    myPixelVal = np.zeros((questions,choices)) # TO STORE THE NON ZERO VALUES OF EACH BOX
                    for image in boxes:
                        #cv2.imshow(str(countR)+str(countC),image)
                        totalPixels = cv2.countNonZero(image)
                        myPixelVal[countR][countC]= totalPixels
                        countC += 1
                        if (countC==choices):countC=0;countR +=1

                    # FIND THE USER ANSWERS AND PUT THEM IN A LIST
                    myIndex=[]
                    for x in range (0,questions):
                        arr = myPixelVal[x]
                        myIndexVal = np.where(arr == np.amax(arr))
                        myIndex.append(myIndexVal[0][0])
                    #print("USER ANSWERS",myIndex)

                    # COMPARE THE VALUES TO FIND THE CORRECT ANSWERS
                    grading=[]
                    for x in range(0,questions):
                        if ans[x] == myIndex[x]:
                            grading.append(1)
                        else:grading.append(0)
                    #print("GRADING",grading)
                    score = (sum(grading)/questions)*100 # FINAL GRADE
                    #print("SCORE",score)

                    # DISPLAYING ANSWERS
                    utlis.showAnswers(imgWarpColored,myIndex,grading,ans) # DRAW DETECTED ANSWERS
                    utlis.drawGrid(imgWarpColored) # DRAW GRID
                    imgRawDrawings = np.zeros_like(imgWarpColored) # NEW BLANK IMAGE WITH WARP IMAGE SIZE
                    utlis.showAnswers(imgRawDrawings, myIndex, grading, ans) # DRAW ON NEW IMAGE
                    invMatrix = cv2.getPerspectiveTransform(pts2, pts1) # INVERSE TRANSFORMATION MATRIX
                    imgInvWarp = cv2.warpPerspective(imgRawDrawings, invMatrix, (widthImg, heightImg)) # INV IMAGE WARP

                    # DISPLAY GRADE
                    imgRawGrade = np.zeros_like(imgGradeDisplay,np.uint8) # NEW BLANK IMAGE WITH GRADE AREA SIZE
                    cv2.putText(imgRawGrade,str(int(score))+"%",(70,100)
                                ,cv2.FONT_HERSHEY_COMPLEX,3,(0,255,255),3) # ADD THE GRADE TO NEW IMAGE
                    invMatrixG = cv2.getPerspectiveTransform(ptsG2, ptsG1) # INVERSE TRANSFORMATION MATRIX
                    imgInvGradeDisplay = cv2.warpPerspective(imgRawGrade, invMatrixG, (widthImg, heightImg)) # INV IMAGE WARP

                    # SHOW ANSWERS AND GRADE ON FINAL IMAGE
                    imgFinal = cv2.addWeighted(imgFinal, 1, imgInvWarp, 1,0)
                    imgFinal = cv2.addWeighted(imgFinal, 1, imgInvGradeDisplay, 1,0)

                    # IMAGE ARRAY FOR DISPLAY
                    imageArray = ([img,imgGray,imgCanny,imgContours],
                                [imgBigContour,imgThresh,imgWarpColored,imgFinal])
                    cv2.imshow("Final Result", imgFinal)
                    QApplication.processEvents()

            except:
                imageArray = ([img,imgGray,imgCanny,imgContours],
                            [imgBlank, imgBlank, imgBlank, imgBlank])

            # LABELS FOR DISPLAY
            lables = [["Original","Gray","Edges","Contours"],
                    ["Biggest Contour","Threshold","Warpped","Final"]]

            stackedImage = utlis.stackImages(imageArray,0.5,lables)
            #cv2.imshow("Result",stackedImage)##############

            # SAVE IMAGE WHEN 's' key is pressed
            if cv2.waitKey(1) & 0xFF == ord('s'):
                cv2.imwrite("Scanned/myImage"+str(count)+".jpg",imgFinal)
                cv2.rectangle(stackedImage, ((int(stackedImage.shape[1] / 2) - 230), int(stackedImage.shape[0] / 2) + 50),
                            (1100, 350), (0, 255, 0), cv2.FILLED)
                cv2.putText(stackedImage, "Scan Saved", (int(stackedImage.shape[1] / 2) - 200, int(stackedImage.shape[0] / 2)),
                            cv2.FONT_HERSHEY_DUPLEX, 3, (0, 0, 255), 5, cv2.LINE_AA)
                cv2.imshow('Result', stackedImage)###########
                QApplication.processEvents()

                cv2.waitKey(300)
                count += 1


       

    def GoTosubmitgrades(self):

        
        ExamName=self.ExamName.text()
        
        rowCount = self.showAllStudents.rowCount()
        columnCount = self.showAllStudents.columnCount()

        for row in range (rowCount):
            
            rowData = []
            for column in range (columnCount):
                widgetItem = self.showAllStudents.item(row, column)

                if(widgetItem and widgetItem.text):

                    rowData.append(widgetItem.text())
                else:
                    rowData.append('')
            #print(rowData)

    

            if(rowData[0]!='' and rowData[1]!='' and rowData[2]!='' and rowData[3]!=''):
                conn = sqlite3.connect("Cognito.db")
                cur = conn.cursor()
                #cur.execute(f"INSERT INTO Exam(Student_FName, Student_LName, Student_ID, Student_Grade) VALUES('{rowData[0]}','{rowData[1]}','{rowData[2]}','{rowData[3]}' )")
                query=f"INSERT INTO Exam(Student_FName, Student_LName, Student_ID, Student_Grade, Instructor_ID, Exam_name, Course) VALUES('{rowData[0]}','{rowData[1]}','{rowData[2]}','{rowData[3]}' , '{self.user}', '{ExamName}', '{self.course}')"
                self.showAllStudents.setRowCount(4)
                tablecount=0
                result=cur.execute(query)
                
                for row in result:
                    self.InstAdm.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
                    self.InstAdm.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
                    self.InstAdm.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
                    self.InstAdm.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
                    
                    tablecount+=1
                conn.commit()
                
                

    def destory(self):
        #self.grade.setText(str(score))

        while True:

            if cv2.waitKey(1) == ord('q'):
        
        # press q to terminate the loop
                cv2.destroyAllWindows()
                break
    ######################################################  
  
    def gotoMainExit7(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   

    def gotoGoBack_InsExamsetup(self):
        widget.setCurrentIndex(widget.count()-2)
        print(widget.count()) 
        n=13
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
       
    
################################################################################################################################## 

class FacialRecSt(QDialog):
    def __init__(self):
       

        #global current_date
        #global current_time
        super(FacialRecSt, self).__init__()
        loadUi("FacialRecSetup.ui",self) 
        #self.AttendanceTakenButtonFP(self.gotoFP) if we connect FP
        self.Exit.clicked.connect(self.gotoExitFacialSetUp)  
        self.TakeMyAttendanceButton.clicked.connect(self.showTime) 
        self.closetimersubmit.clicked.connect(self.closetimer) 
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.image = None
    #####################courses:
    def closetimer(self):
        self.timer.stop()
        self.capture.release()
        with open('attendanceName.csv', 'a') as f:
            f.writelines(f'\n {fullname}, {name}, {date_time_string}, {status}, {self.AvailableCourse.text()}')
        conn = sqlite3.connect("Cognito.db")
        with conn:
            cur=conn.cursor()
            
            cur.execute("INSERT INTO Attendance(Name, Student_id, Date_Time, Status, Course_name)"
                        "VALUES('%s', '%s', '%s', '%s', '%s')" % (
                                                ''.join(fullname),
                                                ''.join(name),
                                                ''.join(date_time_string),
                                                ''.join(status),
                                                ''.join(self.AvailableCourse.text())
                                                ))
            conn.commit()

          

    def gotoExitFacialSetUp(self):
            widget.setCurrentIndex(0)
            self.IDOutput.setText("")
            self.InstructorIDCourse.setText("")
            self.Name_Output.setText("")
            self.Date_Output.setText("")
            self.Time_Output.setText("")
            self.AV2.setText("")
            self.AvailableCourse.setText("")
            #self.Label_Show_Image.setText("")
            self.Label_Show_Image.clear()

            


    # def time_in_range(self, start, end, current):

    #         """Return true if x is in the range [start, end]"""
    #         """Returns whether current is in the range [start, end]"""
    #         return start <= current <= end

    def showTime(self):
        QApplication.processEvents()
        

        
 #format of date
    #########START MATCH-CASES############
        
        week_days = ["Sunday","Monday","Tuesday","Wednsday","Thursday"]

        for day in week_days:
            tday = datetime.datetime.now()
            d1 = tday.strftime("%A")
        current = datetime.datetime.now().time()
        global status
        status= "Present"


        t = time.localtime()
        current_time = time.strftime("%H:%M", t)

        #if d1=="Sunday":
        if d1=="Sunday":

            #Software Testing

            if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):

                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Software Testing & Quality Assurance 201")
                self.InstructorIDCourse.setText("tsoussan")
                if datetime.time(8,10,0) <= current <= datetime.time(9,15,0):
                    status = 'Late'
                self.startVideo1()
            #CS Lab
            elif datetime.time(10,0,0) <= current <= datetime.time(11,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("\nComputer Science II LAB_210")
                self.InstructorIDCourse.setText("stohmeh")
                if datetime.time(10,0,0) <= current <= datetime.time(11,50,0):
                    status = 'Late'
                self.startVideo1()
            #Robotics Lec
            elif datetime.time(15,0,0) <= current <= datetime.time(16,15,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Robotics_201")
                self.InstructorIDCourse.setText("abashar")
                if datetime.time(15,0,0) <= current <= datetime.time(16,15,0):
                    status = 'Late'
                self.startVideo1()
            else: 
                self.AvailableCourse.setText("No available courses at this time ")
        elif d1=="Monday":
            #Software Mana
            if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):


                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Software Project Management 201")
                self.InstructorIDCourse.setText("tsoussan")
                if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):
                    status = 'Late'
                self.startVideo1()
            #DSP Lab
            elif datetime.time(13,0,0) <= current <= datetime.time(14,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Digital Signal Processing LAB 201")
                self.InstructorIDCourse.setText("zalkassim")
                if datetime.time(13,0,0) <= current <= datetime.time(14,50,0):

                    status = 'Late'
                self.startVideo1()
            #DSP Lec
            elif datetime.time(15,0,0) <= current <= datetime.time(15,50,0):

                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Digital Signal Processing 201")
                self.InstructorIDCourse.setText("abashar")
                if datetime.time(15,50,0) <= current <= datetime.time(15,50,0):

                    status = 'Late'
                self.startVideo1()
            else: 
                self.AvailableCourse.setText("No available courses at this time")
        elif d1=="Tuesday":
            #Software Testing
            # if datetime.time(8,0,0) <= current <= datetime.time(19,15,0):
            #     self.AV2.setText("The course available Now is: \n ")
            #     self.AvailableCourse.setText("Software Testing & Quality Assurance 201")
            #     self.InstructorIDCourse.setText("tsoussan")
            #     if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):
            #         status = 'Late'
            #     self.startVideo1()

                ###############delete this:
            if datetime.time(16,0,0) <= current <= datetime.time(23,15,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Software Testing & Quality Assurance 201")
                self.InstructorIDCourse.setText("tsoussan")
                if datetime.time(16,10,0) <= current <= datetime.time(23,15,0):
                    status = 'Late'
                self.startVideo1()

                ##########################
            #CS Lab
            elif datetime.time(10,0,0) <= current <= datetime.time(11,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Computer Science II LAB_110")
                self.InstructorIDCourse.setText("stohmeh")
                if datetime.time(10,0,0) <= current <= datetime.time(11,50,0):
                    status = 'Late'
                self.startVideo1()
            #Robotics Lec
            elif datetime.time(13,0,0) <= current <= datetime.time(14,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Robotics LAB 210")
                self.InstructorIDCourse.setText("zalkassim")
                if datetime.time(13,0,0) <= current <= datetime.time(14,50,0):
                    status = 'Late'
                self.startVideo1()
            else: 
                self.AvailableCourse.setText("No available courses at this time ")
        elif d1=="Wednesday":

            #Software Mana
            if datetime.time(8,0,0) <= current <= datetime.time(13,15,0):
            #if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):


                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Software Project Management 201")
                self.InstructorIDCourse.setText("tsoussan")
                if datetime.time(8,10,0) <= current <= datetime.time(13,15,0):
                #if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):

                    status = 'Late'
                self.startVideo1()
            #DSP Lab

            elif datetime.time(13,0,0) <= current <= datetime.time(14,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Digital Signal Processing LAB 201")
                self.InstructorIDCourse.setText("zalkassim")
                if datetime.time(13,10,0) <= current <= datetime.time(14,50,0):

                    status = 'Late'
                self.startVideo1()

            #####delete it:

            elif datetime.time(18,0,0) <= current <= datetime.time(21,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Computer Science II LAB 210")
                self.InstructorIDCourse.setText("stohmeh")
                if datetime.time(18,10,0) <= current <= datetime.time(21,50,0):
                    status = 'Late'
                self.startVideo1()
                QApplication.processEvents()
            #####delete it:
            else: 
                self.AvailableCourse.setText("No available courses at this time ")
        elif d1=="Thursday": 
        #elif d1=="Saturday": 
             if datetime.time(18,0,0) <= current <= datetime.time(20,15,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Business Intelligence 201")
                self.InstructorIDCourse.setText("gbrahim")
                if datetime.time(19,10,0) <= current <= datetime.time(20,15,0):

                    status = 'Late'
                self.startVideo1()
                
             else: 
                self.AvailableCourse.setText("No available courses at this time ")
        else: 
                self.AvailableCourse.setText("No available courses at this time ")
    
    def startVideo1(self):

        """
        :param camera_name: link of camera or usb camera
        :return:
        """
       

        self.capture = cv2.VideoCapture(0)
        
        self.timer = QTimer(self)  # Create Timer

        path = 'DatasetFacialRec'
        if not os.path.exists(path):
            os.mkdir(path)
        # known face encoding and known face name list
        images = []
        self.class_names = []
        self.encode_list = []
        self.TimeList1 = []
        attendance_list = os.listdir(path)

        for cl in attendance_list:
            cur_img = cv2.imread(f'{path}/{cl}')
            images.append(cur_img)
            self.class_names.append(os.path.splitext(cl)[0])
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            boxes = face_recognition.face_locations(img)
            encodes_cur_frame = face_recognition.face_encodings(img,boxes)[0]
            #encode = face_recognition.face_encodings(img)[0]
            self.encode_list.append(encodes_cur_frame)
        
        #self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.update_frame)  # Connect timeout to the output function
        self.timer.start(10)  # emit the timeout() signal at x=40ms
        # self.timer.singleShot(200, self.updateCaption)

   
        #face rec:
    def face_rec_(self, frame, encode_list_known, class_names):
        """
        :param frame: frame from camera
        :param encode_list_known: known face encoding
        :param class_names: known face names
        :return:
        """
        def mark_attendance(name):

            """
            :param name: detected face known or unknown one
            :return:
            """
            if self.TakeMyAttendanceButton.isChecked():
                self.TakeMyAttendanceButton.setEnabled(False)
      
            ########################################
            global current_time
            global current_date
            now = QDate.currentDate()
            current_date = now.toString('ddd dd MMMM yyyy') #format of date
            current_time = datetime.datetime.now().strftime("%I:%M %p") #for time,p: pm or am
            self.Date_Output.setText(current_date)
            self.Time_Output.setText(current_time)
            self.IDOutput.setText(name)
            
            # conn = sqlite3.connect("Cognito.db")
            # cur = conn.cursor()
            # query=f"SELECT First_Name || ' ' || Last_Name FROM StudentN WHERE Student_id={name}"
            # fullname = cur.execute(query).fetchall()
            # self.Name_Output.setText(fullname)

            with open('attendanceName.csv', 'a') as f:
                    #global id
                    #id=self.IDOutput

                    idInst=self.InstructorIDCourse.text()
                 
                    conn = sqlite3.connect("Cognito.db")
                    cur = conn.cursor()
                    #self.IDOutput.setText(name)
                    
                

                    query=f" SELECT First_Name ||  ' ' || Last_Name FROM StudentN WHERE Student_ID='{name}' "
                    global fullname
                    fullname = cur.execute(query).fetchone()
                    conn.commit()
                    # ''.join(str(e) for e in fullname) 
                    str1=""

                    if(name=='unknown'):
                        self.Name_Output.setText('unknown')
                    else:
                        self.Name_Output.setText(str1.join(fullname) )

                        
                    global date_time_string
                    date_time_string = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
                    todaysdate = datetime.datetime.now().strftime("%d/%m/%y")

                    self.TakeMyAttendanceButton.setChecked(False)

                    self.Time1 = datetime.datetime.now()
                            
                    self.TakeMyAttendanceButton.setEnabled(True)
                        
        # face recognition
        global name
        faces_cur_frame = face_recognition.face_locations(frame)
        encodes_cur_frame = face_recognition.face_encodings(frame, faces_cur_frame)
        # count = 0
        for encodeFace, faceLoc in zip(encodes_cur_frame, faces_cur_frame):
            match = face_recognition.compare_faces(encode_list_known, encodeFace, tolerance=0.50)
            face_dis = face_recognition.face_distance(encode_list_known, encodeFace)
            name = "unknown"
            best_match_index = np.argmin(face_dis)
            # print("s",best_match_index)
            if match[best_match_index]:
                name = class_names[best_match_index].upper()
                y1, x2, y2, x1 = faceLoc
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 20), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
            mark_attendance(name)

        return frame
        

    def ElapseList(self,name):
        with open('attendanceName.csv', "r") as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 2

            Time1 = datetime.datetime.now()
            
            # for row in csv_reader:
            #     for field in row:
            #         if field in row:
            #             if field == 'Clock In':
            #                 if row[0] == name:
            #                     #print(f'\t ROW 0 {row[0]}  ROW 1 {row[1]} ROW2 {row[2]}.')
            #                     Time1 = (datetime.datetime.strptime(row[1], '%y/%m/%d %H:%M:%S'))
            #                     self.TimeList1.append(Time1)
    
            
    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, self.encode_list, self.class_names, 1)

    def displayImage(self, image, encode_list, class_names, window=1):
        """
        :param image: frame from camera
        :param encode_list: known face encoding list
        :param class_names: known face names
        :param window: number of window
        :return:
        """
        image = cv2.resize(image, (640, 480))
        try:
            image = self.face_rec_(image, encode_list, class_names)
        except Exception as e:
            print(e)
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.Label_Show_Image.setPixmap(QPixmap.fromImage(outImage))
            self.Label_Show_Image.setScaledContents(True)
    #def gotoFP(self):


##################################################################################################################################
class TakeATTthroughFPP(QDialog):

    def __init__(self):
        super(TakeATTthroughFPP, self).__init__()
        loadUi("TakeATTthroughFP.ui",self)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.Exit.clicked.connect(self.gotoExitRegisterFingerATT)
        self.TakemyFingerPrintAtt.clicked.connect(self.showTime)
        self.SubmitFingerToDbButtonAtt.clicked.connect(self.gotosubmit) 

    def gotoExitRegisterFingerATT(self):
        widget.setCurrentIndex(0)
        self.IDOutput.setText("")
        self.Name_Output.setText("")
        self.Date_Output.setText("")
        self.Time_Output.setText("")
        self.AV2.setText("")
        self.InstructorIDCourse.setText("")
        self.PlaceFinger.setText("")
        self.AvailableCourse.setText("")
        self.Matching.setText("")

    def gotosubmit(self):
            date_time_string = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
            # font=QFont("Tw Cen MT Condensed Extra Bold",11)

            if self.Name_Output.text()=="unknown":
                mbox=QMessageBox()

                mbox.information(self,"Warning!"," Sorry your fingerprint is not registered")
                mbox.setStyleSheet("background-color: rgb(0,0,0,0);font:11pt 'Tw Cen MT Condensed Extra Bold';")


            else:
          
       
        
                with open('attendanceName.csv', 'a') as f:
                    f.writelines(f'\n {self.Name_Output.text()}, {id}, {date_time_string}, {status}, {self.AvailableCourse.text()}')
                conn = sqlite3.connect("Cognito.db")
                with conn:
                    cur=conn.cursor()
                    
                    cur.execute("INSERT INTO Attendance(Name, Student_id, Date_Time, Status, Course_name)"
                                "VALUES('%s', '%s', '%s', '%s', '%s')" % (
                                                        ''.join(self.Name_Output.text()),
                                                        ''.join(id),
                                                        ''.join(date_time_string),
                                                        ''.join(status),
                                                        ''.join(self.AvailableCourse.text())
                                                        ))
                    conn.commit()
                    mbox=QMessageBox()
                    mbox.information(self,"Success"," Your attendance successfully taken ")
      
        
            

   
    def runFp(self):

        session = as608.connect_serial_session("COM6")
        print(session)
        #session1= as608.connect_serial_session("COM14")
                                      
        if session:
            
            as608.get_templates_list(session)
            as608.get_templates_count(session)
            as608.get_device_size(session)
            self.fingerprint_check_all_file(session, as608, "DatabaseFingerprint") #check all in db "templ2"))

      

    def fingerprint_check_all_file(self,session, as608_lib, save_location):
        """Compares a new fingerprint template to an existing template stored in a file
        This is useful when templates are stored centrally (i.e. in a database)"""
        file_check_res = False
        self.PlaceFinger.setText("1. Please place your finger in the Fingerprint Scanner...")
        QtWidgets.qApp.processEvents()


        while session.get_image() != as608_lib.OK:
            pass
        print("Templating...")
        if session.image_2_tz(1) != as608_lib.OK:
            return False

        print("Loading file template...", end="", flush=True)
        

        if os.path.exists(save_location):
            # print(os.listdir(save_location))
            for each_file in os.listdir(save_location):
                print("=-=-=-ENtering file-=-=-=-=--=",each_file)

                global id
                id=each_file.replace(".dat", "")

                with open(save_location+"/"+each_file, "rb") as file:
                    data = file.read()
                session.send_fpdata(list(data), "char", 2)
                now = QDate.currentDate()
                global current_time
                global current_date
                current_date = now.toString('ddd dd MMMM yyyy') #format of date
                current_time = datetime.datetime.now().strftime("%I:%M %p") #for time,p: pm or am

                i = session.compare_templates()
                if i == as608_lib.OK:
                    self.Matching.setText("Fingerprint Successfully matched")
                    self.mark_attendance(id)


                    
                    global name
                    name=self.Name_Output.text()
                    self.Date_Output.setText(current_date)
                    self.Time_Output.setText(current_time)
                    self.IDOutput.setText(id)

                    return True
                
                if i == as608_lib.NOMATCH:
                    self.Matching.setText("Sorry, your Fingerprint does not exist")
                    self.Date_Output.setText(current_date)
                    self.Time_Output.setText(current_time)
                    self.Name_Output.setText("unknown") 
                    self.IDOutput.setText("unknown") 
                    QtWidgets.qApp.processEvents()

                file_check_res = False
            return file_check_res
        else:
            print("NO")
            return False

    def showTime(self):
        QApplication.processEvents()
    
        
        week_days = ["Sunday","Monday","Tuesday","Wednsday","Thursday","Friady"]

        for day in week_days:
            tday = datetime.datetime.now()
            d1 = tday.strftime("%A")
        current = datetime.datetime.now().time()
        global status
        status= "Present"


        t = time.localtime()
        current_time = time.strftime("%H:%M", t)
     
        #if d1=="Sunday":
        if d1=="Sunday":

            #Software Testing

            if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):

                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Software Testing & Quality Assurance 201")
                self.InstructorIDCourse.setText("tsoussan")
                if datetime.time(8,10,0) <= current <= datetime.time(9,15,0):
                    status = 'Late'
                self.runFp()
            #CS Lab
            elif datetime.time(10,0,0) <= current <= datetime.time(11,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("\nComputer Science II LAB_210")
                self.InstructorIDCourse.setText("stohmeh")
                if datetime.time(10,0,0) <= current <= datetime.time(11,50,0):
                    status = 'Late'
                self.runFp()
            #Robotics Lec
            elif datetime.time(15,0,0) <= current <= datetime.time(16,15,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Robotics_201")
                self.InstructorIDCourse.setText("abashar")
                if datetime.time(15,0,0) <= current <= datetime.time(16,15,0):
                    status = 'Late'
                self.runFp()
            else: 
                self.AvailableCourse.setText("No available courses at this time ")
        elif d1=="Monday":
            #Software Mana
            if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):
            


                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Software Project Management 201")
                self.InstructorIDCourse.setText("tsoussan")
                if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):
                    status = 'Late'
                self.runFp()
            # #DSP Lab
            # #elif datetime.time(13,0,0) <= current <= datetime.time(14,50,0):
            #     self.AV2.setText("The course available Now is: \n ")
            #     self.AvailableCourse.setText("Digital Signal Processing LAB 201")
            #     self.InstructorIDCourse.setText("zalkassim")
            #     #if datetime.time(13,0,0) <= current <= datetime.time(14,50,0):

            #         status = 'Late'
            #     self.runFp()
            #DSP Lec
            #elif datetime.time(15,0,0) <= current <= datetime.time(15,50,0):
            elif datetime.time(14,30,0) <= current <= datetime.time(16,50,0):

                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Digital Signal Processing 201")
                self.InstructorIDCourse.setText("abashar")
                #if datetime.time(15,50,0) <= current <= datetime.time(15,50,0):
                if datetime.time(14,50,0) <= current <= datetime.time(16,50,0):

                    status = 'Late'
                self.runFp()
            else: 
                self.AvailableCourse.setText("No available courses at this time")
        elif d1=="Tuesday":
            #Software Testing
            if datetime.time(8,0,0) <= current <= datetime.time(19,15,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Software Testing & Quality Assurance 201")
                self.InstructorIDCourse.setText("tsoussan")
                if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):
                    status = 'Late'
                self.runFp()
            #CS Lab
            elif datetime.time(10,0,0) <= current <= datetime.time(11,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Computer Science II LAB_110")
                self.InstructorIDCourse.setText("stohmeh")
                if datetime.time(10,0,0) <= current <= datetime.time(11,50,0):
                    status = 'Late'
                self.runFp()
            #Robotics Lec
            elif datetime.time(13,0,0) <= current <= datetime.time(14,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Robotics LAB 210")
                self.InstructorIDCourse.setText("zalkassim")
                if datetime.time(13,0,0) <= current <= datetime.time(14,50,0):
                    status = 'Late'
                self.runFp()
            else: 
                self.AvailableCourse.setText("No available courses at this time ")
        elif d1=="Wednesday":

            #Software Mana
            if datetime.time(8,0,0) <= current <= datetime.time(23,15,0):
            #if datetime.time(8,0,0) <= current <= datetime.time(9,15,0):


                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Software Project Management 201")
                self.InstructorIDCourse.setText("tsoussan")
                if datetime.time(8,10,0) <= current <= datetime.time(9,15,0):
                    status = 'Late'
                self.runFp()
            #DSP Lab

            elif datetime.time(13,0,0) <= current <= datetime.time(14,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Digital Signal Processing LAB 201")
                self.InstructorIDCourse.setText("zalkassim")
                if datetime.time(13,10,0) <= current <= datetime.time(14,50,0):

                    status = 'Late'
                self.runFp()

            #####delete it:

            elif datetime.time(18,0,0) <= current <= datetime.time(21,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Computer Science II LAB 210")
                self.InstructorIDCourse.setText("stohmeh")
                if datetime.time(18,10,0) <= current <= datetime.time(21,50,0):
                    status = 'Late'
                self.runFp()
                QApplication.processEvents()
            #####delete it:
            else: 
                self.AvailableCourse.setText("No available courses at this time ")
        elif d1=="Thursday": 
        #elif d1=="Saturday": 
            if datetime.time(8,0,0) <= current <= datetime.time(12,15,0):
            #if datetime.time(18,0,0) <= current <= datetime.time(20,15,0):

            
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Business Intelligence 201")
                self.InstructorIDCourse.setText("gbrahim")
                if datetime.time(8,10,0) <= current <= datetime.time(12,15,0):
                #if datetime.time(19,10,0) <= current <= datetime.time(20,15,0):


                    status = 'Late'
                self.runFp()
                
            else: 
                self.AvailableCourse.setText("No available courses at this time ")
        ##delete this later:

        elif d1=="Friday": 
            if datetime.time(19,0,0) <= current <= datetime.time(23,50,0):
                self.AV2.setText("The course available Now is: \n ")
                self.AvailableCourse.setText("Computer Science II LAB 210")
                self.InstructorIDCourse.setText("stohmeh")
                if datetime.time(19,10,0) <= current <= datetime.time(23,50,0):
                    status = 'Late'
                self.runFp()
                QApplication.processEvents()
            else: 
                self.AvailableCourse.setText("No available courses at this time ")

    def mark_attendance(self, id):

        
            if self.TakemyFingerPrintAtt.isChecked():
                self.TakemyFingerPrintAtt.setEnabled(False)
      
            ########################################
            # global current_time
            # global current_date
            # now = QDate.currentDate()
            # current_date = now.toString('ddd dd MMMM yyyy') #format of date
            # current_time = datetime.datetime.now().strftime("%I:%M %p") #for time,p: pm or am
            # self.Date_Output.setText(current_date)
            # self.Time_Output.setText(current_time)
            
            with open('attendanceName.csv', 'a') as f:
                    #global id
                    #id=self.IDOutput

                    # idInst=self.InstructorIDCourse.text()
                    # if id == "201901448":
                    #     self.Name_Output.setText("Wed AlGhamdi")
                    # elif id == "201800608":
                    #     self.Name_Output.setText("Noor AlBasara") 
                    # elif  id == "201801636":
                    #     self.Name_Output.setText("Fatimah Alali") 
                    # else:
                    #     self.Name_Output.setText("unknown")
                    conn = sqlite3.connect("Cognito.db")
                    cur = conn.cursor()
                    self.IDOutput.setText(id)
                    
                

                    query=f" SELECT First_Name ||  ' ' || Last_Name FROM StudentN WHERE Student_ID='{id}' "
                    global fullnameFinger
                    fullnameFinger = cur.execute(query).fetchone()
                    conn.commit()
                    # ''.join(str(e) for e in fullname) 
                    str1=""

                    if(id=='unknown'):
                        self.Name_Output.setText('unknown')
                    else:
                        self.Name_Output.setText(str1.join(fullnameFinger) )
 

                    
                   
                    # if name=="NOOR ALBASARA":
                    #     id.setText("201800608")
                    #     self.Name_Output.setText(name)

                    # elif name=="FATIMAH ALALI":
                    #     id.setText("201801636")
                    #     self.Name_Output.setText(name)

                    # elif name=="WED ALGHAMDI":
                    #     id.setText("201901448")
                    #     self.Name_Output.setText(name)

                    # else:
                    #    id.setText("unknown")
                    #    self.Name_Output.setText("unknown")
                       
     
                    global date_time_string
                    date_time_string = datetime.datetime.now().strftime("%d/%m/%y %H:%M:%S")
                    todaysdate = datetime.datetime.now().strftime("%d/%m/%y")
                    
                    self.TakemyFingerPrintAtt.setChecked(False)

                    self.Time1 = datetime.datetime.now()
                            
                    self.TakemyFingerPrintAtt.setEnabled(True)

                  


##################################################################################################################################


class RegisterFingerStInDB(QDialog):
    def __init__(self):
        

        super(RegisterFingerStInDB, self).__init__()
        loadUi("RegisterFingerprintToDB.ui",self) 
        
        self.Exit.clicked.connect(self.gotoExitRegisterFinger)
        self.SubmitFingerToDbButton.clicked.connect(self.gotoSubmitFingerToDbButton)
       # self.TakemyFingerPrint.clicked.connect(self.fingerprintArduino)
        self.GoBack.clicked.connect(self.gotoGoBack)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))


        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.TakemyFingerPrint.clicked.connect(self.runFp)

   
    

    def runFp(self):

        session = as608.connect_serial_session("COM6")

        global file_name
        file_name=self.PmuIdFingerpint.text()
        if session:
            #session.set_sysparam(4,12)
            as608.get_templates_list(session)
            as608.get_templates_count(session)
            as608.get_device_size(session)
            #as608.enroll_finger_to_device(session, as608)
            # print(as608.search_fingerprint_on_device(session, as608))
            self.enroll_save_to_file(session, as608, "DatabaseFingerprint", file_name)
            # as608.enroll_save_to_file(session, as608, "database", "templ000000001")
            #as608.fingerprint_check_one_file(session, as608, "database", "templ1")
            # as608.fingerprint_check_one_file(session, as608, "database", "templ000000001")
            #as608.fingerprint_check_all_file(session, as608, "DatabaseFingerprint") #check all in db "templ2"))

    def gotoSubmitFingerToDbButton(self):
        widget.setCurrentIndex(4)

    def gotoExitRegisterFinger(self):
         widget.setCurrentIndex(0)

    def get_image(self):
            """Requests the sensor to take an image and store it memory, returns
            the packet error code or OK success"""
            as608.Operation._send_packet([_GETIMAGE])
            return as608.Operation._get_packet(12)[0]
    
    def enroll_save_to_file(self, session, as608_lib, save_location, file_name):
     
        """Take a 2 finger images and template it, then store it in a file"""
        saved_directory_file_name = save_location+"/"+file_name+".dat"
        for fingerimg in range(1, 3):
            if fingerimg == 1:
               
                self.placefinger.setText("Place finger on sensor...")
                QtWidgets.qApp.processEvents()

                print("", end="", flush=True)

            else:
                self.placefinger_2.setText("Place same finger again...")
                QtWidgets.qApp.processEvents()

                print("", end="", flush=True)

            print(session)


            while True:
                i = session.get_image()
                if i == as608_lib.OK:
                    self.imageTaken.setText("Image taken")
                    QtWidgets.qApp.processEvents()

                    break
                if i == as608_lib.NOFINGER:
                    print(".", end="", flush=True)
                elif i == as608_lib.IMAGEFAIL:
                    self.ImageError.setText("Imaging error")
                    QtWidgets.qApp.processEvents()

                    return False
                else:
                    self.ImageError.setText("Other error")
                    QtWidgets.qApp.processEvents()

                    return False

            print("Templating...", end="", flush=True)
            i = session.image_2_tz(fingerimg)
            if i == as608_lib.OK:
                self.Temp.setText("Templated")
                QtWidgets.qApp.processEvents()

            else:
                if i == as608_lib.IMAGEMESS:
                    self.TempError.setText("Image too messy")
                    QtWidgets.qApp.processEvents()

                elif i == as608_lib.FEATUREFAIL:
                    self.TempError.setText("Could not identify features")
                    QtWidgets.qApp.processEvents()

                elif i == as608_lib.INVALIDIMAGE:
                    self.TempError.setText("Image invalid")
                    QtWidgets.qApp.processEvents()

                else:
                    self.TempError.setText("Other error")
                    QtWidgets.qApp.processEvents()

                return False

            if fingerimg == 1:
                self.removefinger.setText("Remove finger")
                QtWidgets.qApp.processEvents()

                while i != as608_lib.NOFINGER:
                    i = session.get_image()

        print("Creating model...", end="", flush=True)
        i = session.create_model()
        if i == as608_lib.OK:
            self.Success.setText("Fingerprint Succesfully created")
            QtWidgets.qApp.processEvents()

        else:
            if i == as608_lib.ENROLLMISMATCH:
                self.Success.setText("Prints did not match")
                QtWidgets.qApp.processEvents()

            else:
                print("Other error")
            return False

        print("Downloading template...")
        data = session.get_fpdata("char", 1)
        try:
            file = open(saved_directory_file_name, "wb")
        except FileNotFoundError as e:
            os.makedirs(save_location)
            file = open(saved_directory_file_name, "wb")
        file.write(bytearray(data))
        file.close()
        print("Template is saved in",saved_directory_file_name,"file.")

        return True
    
    def gotoGoBack(self):
        #widget.setCurrentIndex(widget.count()-1)
        widget.setCurrentIndex(2)
        print(widget.count()) 
        # n=14
        # for i in range(n):
        #     wid = widget.widget(n)
        #     widget.removeWidget(wid) 

    

        
            

##################################################################################################################################
class RegisterFacialStInDB(QDialog):
    def __init__(self):
        # global IDfaceRecog
        # IDfaceRecog=self.ID.text()
        
        super(RegisterFacialStInDB, self).__init__()
        loadUi("RegisterFacialInDBst.ui",self) 
        self.Exit.clicked.connect(self.gotoExitLoadingFacial)
        self.SubmitFacialToDbButton.clicked.connect(self.gotoSubmitFacialToDbButton)
        self.Detectmyfacebutton.clicked.connect(self.gotoDetectmyfacebutton)
        #self.takeMyPic.clicked.connect(self.gotoTakeMyPicture)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.GoBack.clicked.connect(self.gotoGoBack)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))

        

        self.image = None

    def gotoGoBack (self):
        widget.setCurrentIndex(2)
        print(widget.count()) 
        
        
    def gotoSubmitFacialToDbButton(self):
        self.timer.stop()
        self.capture.release()
        # widget.addWidget(RegisterFingerStInDB(self.user))
        # widget.setCurrentIndex(widget.count()-1)  

        #widget.setCurrentIndex(7)

    def gotoExitLoadingFacial(self):
        widget.setCurrentIndex(0)
        self.ID.setText("")
        self.RegisterFaceDetect_Label.clear()


    def gotoDetectmyfacebutton(self):
        if  self.ID.text()=="":
            mbox=QMessageBox()
            mbox.information(self,"Warning!"," Please Input your ID ")
        else:
            webcam=True
            self.capture = cv2.VideoCapture(0)
            self.timer = QTimer(self)  # Create Timer
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(10) 
     
    def update_frame(self):
        ret, self.image = self.capture.read()
        self.displayImage(self.image, 1)
    
    def displayImage(self, image,window=1) :
        image = cv2.resize(image, (640, 480))
        #convert it using qt format
        qformat = QImage.Format_Indexed8
        if len(image.shape) == 3:
            if image.shape[2] == 4:
                qformat = QImage.Format_RGBA8888
            else:
                qformat = QImage.Format_RGB888
        outImage = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
        outImage = outImage.rgbSwapped()

        if window == 1:
            self.RegisterFaceDetect_Label.setPixmap(QPixmap.fromImage(outImage))
            self.RegisterFaceDetect_Label.setScaledContents(True)
            
            cv2.imwrite(f"C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\DatasetFacialRec\\{self.ID.text()}.jpg",image) 
######################################################################################
            
class Admin(QDialog):
    def __init__(self):
        super(Admin, self).__init__()
        loadUi("AdminLogin.ui",self) 
        self.Exit.clicked.connect(self.gotoExitLoginIAdmin)
        self.PmuPassAdmintButton.setEchoMode(QtWidgets.QLineEdit.Password)
        self.LoginAdminButto.clicked.connect(self.gotoAfterAdminLogin)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        
     #For the password 
    def gotoAfterAdminLogin(self):
        
        AdminID = self.PmuIDAdminButton.text()
        password = self.PmuPassAdmintButton.text()

        if len(AdminID)==0 or len(password)==0:
            self.InvalidAdminPass.setText("Please input all fields.")

        else:
                conn = sqlite3.connect("Cognito.db")
                cur = conn.cursor()
                queryID = 'SELECT AdminID FROM Admin WHERE AdminID =\''+AdminID+"\'"
            
                result=cur.execute(queryID).fetchall()

                if result:
                
                    #if self.user in y:
                        conn.commit()

                        conn = sqlite3.connect("Cognito.db")
                        cur  = conn.cursor()
                        query = 'SELECT AdminPass FROM Admin WHERE AdminID =\''+AdminID+"\'"
                        cur.execute(query)
                        conn.commit()

                        result_pass = cur.fetchone()[0] #to compare password 
                        if result_pass == password:
                            widget.setCurrentIndex(10)
                            self.PmuIDAdminButton.setText("")
                            self.PmuPassAdmintButton.setText("")
                            self.InvalidAdminPass.setText("")
                            #self.gotoAfterAdminLogin()
                
        
                        else:
                            self.InvalidAdminPass.setText("Invalid password")

                else:
                    self.InvalidAdminPass.setText("User does not exist")
        

        # if len(AdminID)==0 or len(Adminpassword)==0:
        #     self.InvalidAdminPass.setText("Please input all fields.")

        # else:
        #     conn = sqlite3.connect("Cognito.db")
        #     cur = conn.cursor()
        #     query = 'SELECT AdminPass FROM Admin WHERE AdminID =\''+AdminID+"\'"
        #     cur.execute(query)
        #     result_pass = cur.fetchone()[0] #to compare password 

        #     if result_pass == Adminpassword:
        #         widget.setCurrentIndex(9)
        #         self.PmuIDAdminButton.setText("")
        #         self.PmuPassAdmintButton.setText("")
        #         self.InvalidAdminPass.setText("")
        #         #self.gotoAfterAdminLogin()
                        
        #     else:
        #         self.InvalidPassLab.setText("Invalid username or password")
            

    def gotoExitLoginIAdmin(self):
            widget.setCurrentIndex(0)
    #Remove comment later
    # def gotoAfterAdminLogin(self):
    #     widget.setCurrentIndex(widget.currentIndex()+1)

#################################################################################################################################33
class AfterAdminLogin(QDialog):
    def __init__(self):
        super(AfterAdminLogin, self).__init__()
        loadUi("AfterAdminLogin.ui",self) 
        #self.AddInst.clicked.connect(self.gotoaddinst) #1
        self.InsertInstCourses.clicked.connect(self.gotoInsertInstCourses) #2 NOT WORKING
        self.InsertCourseStud.clicked.connect(self.gotoInsertCourseStud) #3
        # self.DeleteStu.clicked.connect(self.gotoDeleteStu) #4
        self.AllInstInDB.clicked.connect(self.gotoAllInstInDB)
        self.AllstudInDB.clicked.connect(self.gotoAllStuInDB)
        self.Exit.clicked.connect(self.gotoExitLoginIAdminServices)
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.GoBack.clicked.connect(self.gotoGoBack)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))

        admin="Cognito"

#changeIndex
    # def gotoaddinst(self):#1
    #     widget.addWidget(AddInstructor())
    #     widget.setCurrentIndex(widget.count()-1)

    def gotoInsertInstCourses(self):#2
        widget.addWidget(InsertCourseInst()) 
        widget.setCurrentIndex(widget.count()-1)

    def gotoInsertCourseStud(self): #3
        widget.addWidget(InsertStudCourses()) 
        widget.setCurrentIndex(widget.count()-1)

    # def gotoDeleteStu(self):#4
    #     widget.addWidget(DeleteStud()) 
    #     widget.setCurrentIndex(widget.count()-1)

    def gotoAllInstInDB(self):
        #conn = sqlite3.connect("Cognito.db")
        widget.addWidget(AllInstructorsInDB())
        widget.setCurrentIndex(widget.count()-1)
    
    def gotoAllStuInDB(self):
        #conn = sqlite3.connect("Cognito.db")
        widget.addWidget(AllStudentsInDB())
        widget.setCurrentIndex(widget.count()-1) 

    
    def gotoExitLoginIAdminServices(self):
        widget.setCurrentIndex(0)

    def gotoGoBack(self):
            widget.setCurrentIndex(widget.count()-2)
            print(widget.count()) 
            n=12
            for i in range(n):
                wid = widget.widget(n)
                widget.removeWidget(wid)   
            print(widget.count())     

##################################################################################################################################

# class AddInstructor(QDialog):
#     #not used
#     def __init__(self):
#         super(AddInstructor, self).__init__()
#         loadUi("AddInstructorO.ui",self) 

#         self.SumbintInstFromAdmin.clicked.connect(self.gotoSubmitInstButton)
#         self.passIns.setEchoMode(QtWidgets.QLineEdit.Password) #hiding pass
#         self.Exit.clicked.connect(self.gotoExitFromAdminInstReg)
#         self.GoBack.clicked.connect(self.gotoGoBackAddInsAdmin)
#         self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
#         self.GoBack.setIconSize(QSize(45,45))
#         self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
#         self.Exit.setIconSize(QSize(45,45))


#     def gotoSubmitInstButton(self):
#         fname = self.firstNameIns.text()
#         lname = self.lastNameIns.text()
#         pmu_id = self.pmuIDIns.text()
#         email = self.pmuEmailIns.text()
#         college = self.collegeIns.currentText()
#         dept = self.deptIns.text()
#         password = self.passIns.text()

# #Enter Courses
#         inputs=[self.Course1.text(), self.Course2.text(), self.Course3.text(), 
#         self.Course4.text(), self.Course5.text(), self.Course6.text(),
#         self.Course7.text(), self.Course8.text()]

#         courses=[]

#         for i in range(8):
#             if len(inputs[i]) != 0:
#                 courses.append(inputs[i])   
        

#         if len(fname)==0 or len(lname)==0 or len(pmu_id)==0 or len(email)==0 or len(college)==0 or len(dept)==0 or len(password)==0 or len(courses)==0 :
#             self.invalidMsg.setText("Please input all fields.")

#         else:    
#             conn = sqlite3.connect("Cognito.db")
#             with conn:
#                 cur=conn.cursor()
#                 cur.execute("INSERT INTO Instructor(First_name, Last_name, Instructor_id, Email, College, Department, Password)"
#                             "VALUES('%s', '%s', '%s', '%s', '%s', '%s', '%s')" % (''.join(fname),
#                                                     ''.join(lname),
#                                                     ''.join(pmu_id),
#                                                     ''.join(email),
#                                                     ''.join(college),
#                                                     ''.join(dept),
#                                                     ''.join(password)
#                                                     ))
#                 for i in range(len(courses)):
#                     cur.execute("INSERT INTO Course(Course_name, Instructor_id)"
#                             "VALUES('%s', '%s')" % (''.join(courses[i]),
#                                                     ''.join(pmu_id)
#                                                     ))
                                                        
#             self.validMsg.setText("Instructor has been successfully added")
#             #widget.setCurrentIndex(widget.currentIndex()-2) 
#     def gotoExitFromAdminInstReg(self):
#         #widget.setCurrentIndex(widget.currentIndex()-19)
#         widget.setCurrentIndex(0)
#         n=11
#         for i in range(n):
#             wid = widget.widget(n)
#             widget.removeWidget(wid)   
#         print(widget.count()) 

#     def gotoGoBackAddInsAdmin(self):
#         widget.setCurrentIndex(widget.currentIndex()-1)
#         n=11
#         for i in range(n):
#             wid = widget.widget(n)
#             widget.removeWidget(wid)   
#         print(widget.count()) 

################################################################################################################################
class InsertCourseInst(QDialog):
    #Replacment of InstDelete 
    def __init__(self):
        super(InsertCourseInst, self).__init__()
        loadUi("InsertCourseInst.ui",self) 
        #self.deleteBtn.clicked.connect(self.gotoDeleteInst)
        self.Exit.clicked.connect(self.gottoExitFromAdminInstRef)
        self.GoBack.clicked.connect(self.gottoGoBackDeleteInstAdmin)

        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.InstID()
        self.SubmitCourses.clicked.connect(self.SubmCourses)

        
       

    def InstID(self):
        
        

        conn = sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT DISTINCT Instructor_id FROM Instructor'
        cur.execute(query)
        final_result = [i[0] for i in cur.fetchall()]
        for i in range(len(final_result)):
           self.InstIDs.addItem(final_result[i])

    # def gotoDeleteInst(self):
    #     instid = self.instID.text()
    #     if len(instid)==0 :
    #         self.InputAllfIELDSINS.setText("Please input all fields.") 
    #     else:
    #         conn = sqlite3.connect("Cognito.db")
    #         cur = conn.cursor()
    #         cur.execute('DELETE FROM Course WHERE Instructor_id =\''+instid+"\'")
    #         cur.execute('DELETE FROM Instructor WHERE Instructor_id =\''+instid+"\'")
    #         conn.commit()
    #         self.DelteInstSucc.setText("Instructor has been successfully deleted")
    def SubmCourses(self):

        self.InstructorID=self.InstIDs.currentText()

        inputs=[self.Course1Inst.text(), self.Course2Inst.text(), self.Course3Inst.text(), 
        self.Course4Inst.text(), self.Course5Inst.text(), self.Course6Inst.text(),
        self.Course7Inst.text(), self.Course8Inst.text(),self.Course9Inst.text()]

        courses=[]

        for i in range(9):
            if len(inputs[i]) != 0:
                courses.append(inputs[i])   
        

        conn = sqlite3.connect("Cognito.db")
        with conn:
            cur=conn.cursor()

            for i in range(len(courses)):

                cur.execute("INSERT INTO Course(Course_name,Instructor_id)"
                        "VALUES('%s','%s')" % (''.join(courses[i]),
                                                ''.join(self.InstructorID),
                                                
                                                
                                                ))
        mbox=QMessageBox()

        mbox.information(self,"Success","Courses has been successfully added")


    def gottoExitFromAdminInstRef(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 
    def gottoGoBackDeleteInstAdmin(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 
#############################################################################################################################
class InsertStudCourses(QMainWindow):
    def __init__(self):
        super(InsertStudCourses, self).__init__()
        loadUi("InsertCourseStu.ui",self) 
        self.SubmitStuAdmin.clicked.connect(self.gotoSubmitStuAdmin)
        self.Exit.clicked.connect(self.gotoExitStRegAdmin)
        #self.passStuAdmin.setEchoMode(QtWidgets.QLineEdit.Password)
        self.GoBack.clicked.connect(self.gotoGoBackAddStuAdmin)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))

        # self.studentidname.activated.connect(self.gotoStID_NAME)
        # self.InstIDaddcourses1.activated.connect(self.gotoInstID)
        # self.course1.activated.connect(self.coursename)  
            
        self.coursename()
        self.gotoInstID()
        self.gotoStID_NAME()
        

    def gotoStID_NAME(self):
        conn = sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT DISTINCT Student_ID FROM StudentN'
        cur.execute(query)
        final_result = [i[0] for i in cur.fetchall()]
        for i in range(len(final_result)):
            self.studentidname.addItem(final_result[i])

    def gotoInstID(self):
        conn = sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT DISTINCT Instructor_id FROM Instructor'
        cur.execute(query)
        final_result = [i[0] for i in cur.fetchall()]
        for i in range(len(final_result)):
            self.InstIDaddcourses1.addItem(final_result[i])
        
    def coursename(self):
        
        conn = sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query = 'SELECT DISTINCT Course_name FROM Course'
        cur.execute(query)
        final_result = [i[0] for i in cur.fetchall()]
        for i in range(len(final_result)):
            self.course1.addItem(final_result[i])

    def gotoSubmitStuAdmin(self):
        self.studentidnamecurrent=self.studentidname.currentText()
        self.courses=self.course1.currentText()
        self.InstIDaddcoursess1=self.InstIDaddcourses1.currentText()

        conn = sqlite3.connect("Cognito.db")
        with conn:
            cur=conn.cursor()
            cur.execute("INSERT INTO Course(Course_name,Instructor_id,Student_id)"
                        "VALUES('%s','%s','%s')" % (''.join(self.courses),
                                                ''.join(self.InstIDaddcoursess1),
                                                ''.join(self.studentidnamecurrent)
                                                
                                                ))
        mbox=QMessageBox()

        mbox.information(self,"Success","Student has been successfully added")
        #mbox.setStyleSheet("QLabel{background-color: rgb(0, 0, 0, 0);} ")
        #self.validStu.setText("Student has been successfully added")                                      

    def gotoExitStRegAdmin(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 

    def gotoGoBackAddStuAdmin(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 
################################################################################################################################
# class DeleteStud(QDialog):
#     #not used
#     def __init__(self):
#         super(DeleteStud, self).__init__()
#         loadUi("DeleteStud.ui",self) 

#         self.deleteBtnStAdmin.clicked.connect(self.gotoDeleteST)
#         self.Exit.clicked.connect(self.gotoExitFromAdminInstReg2)
#         self.GoBack.clicked.connect(self.gottoGoBackDeleteStuAdmin)

#         self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
#         self.GoBack.setIconSize(QSize(45,45))
#         self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
#         self.Exit.setIconSize(QSize(45,45))

        

#     def gotoDeleteST(self):
#         StID = self.StudentIDadmin.text()


#         if len(StID)==0 :
#             self.InputallFields.setText("Please input all fields.")

#         else:


#             conn = sqlite3.connect("Cognito.db")
#             cur = conn.cursor()
#             cur.execute('DELETE FROM Course WHERE Student_ID =\''+StID+"\'")
#             cur.execute('DELETE FROM StudentN WHERE Student_ID =\''+StID+"\'")
#             conn.commit()

#             self.DeleteSuccessfSt.setText("Student has been successfully deleted")
           

#     def gotoExitFromAdminInstReg2(self):
#         #widget.setCurrentIndex(widget.currentIndex()-22)
#         widget.setCurrentIndex(0)
#         n=12
#         for i in range(n):
#             wid = widget.widget(n)
#             widget.removeWidget(wid)   
#         print(widget.count()) 
    
#     def gottoGoBackDeleteStuAdmin(self):
#         widget.setCurrentIndex(widget.currentIndex()-1)
#         n=12
#         for i in range(n):
#             wid = widget.widget(n)
#             widget.removeWidget(wid)   
#         print(widget.count()) 
###############################################################################################################################
class AllInstructorsInDB(QMainWindow):

    def __init__(self):
        
        super(AllInstructorsInDB, self).__init__()
        loadUi("AllInstructorsInDB.ui",self) 
        self.InstAdm.setHorizontalHeaderLabels(["Instructor_id", "First_name","Last_name","Email","College","Department","Password"]
        )
        self.DepartmentAndDepartment_2.setHorizontalHeaderLabels(["College","Department"])
        self.Exit_2.clicked.connect(self.gotoExitInsDBAdmin)
        self.GoBack_2.clicked.connect(self.gotoGoBackInsDBAdmin)
        self.GoBack_2.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack_2.setIconSize(QSize(45,45))
        self.Exit_2.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit_2.setIconSize(QSize(45,45))
        self.DELETEinst_2.clicked.connect(self.deleteInst)
        self.ADDBTNinst_2.clicked.connect(self.addInst)
        # self.combo=QComboBox(self)
        # self.combo.addItems(['College of Engineering', 'College of Computer Engineering and Sciences', 
        #                 'College of Business Administration', 'College of Law'
        #                 'College of Architecture and Design'])
        # self.InstAdm.setCellWidget(0,2, self.combo) 
        self.gotoAllInstInDB()
        self.COLLEGE_DEPARTMENT()
        

        

    def COLLEGE_DEPARTMENT(self):

        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query='SELECT * FROM CollegeAndDepartment'
        
        
        self.DepartmentAndDepartment_2.setRowCount(7)

        tablecount=0
        #cur.execute(query)
        results = cur.execute(query)
        
        for row in results:
            self.DepartmentAndDepartment_2.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.DepartmentAndDepartment_2.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
            # self.DepartmentAndDepartment.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
            # self.DepartmentAndDepartment.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
            # self.DepartmentAndDepartment.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4])) 
            # self.DepartmentAndDepartment.setItem(tablecount, 5, QtWidgets.QTableWidgetItem(row[5]))
            # self.DepartmentAndDepartment.setItem(tablecount, 6, QtWidgets.QTableWidgetItem(row[6])) 
 
            tablecount+=1


    def addInst(self):
        rowCount = self.InstAdm.rowCount()
        columnCount = self.InstAdm.columnCount()
        
    
        for row in range (rowCount): #10 rows
            rowData = []

            for column in range (columnCount):#7 columns
                widgetItem = self.InstAdm.item(row, column)
                if(widgetItem and widgetItem.text):
                    rowData.append(widgetItem.text())
                    
                
                else:
                    rowData.append('')
    
        self.msg(rowData)

     
    def msg(self, rowData):
        if(rowData[0]!='' and rowData[1]!='' and rowData[2]!='' and rowData[3]!=''and rowData[4]!=''and rowData[5]!=''and rowData[6]!=''
        ):
            conn = sqlite3.connect("Cognito.db")
            cur = conn.cursor()
            #cur.execute(f"INSERT INTO Exam(Student_FName, Student_LName, Student_ID, Student_Grade) VALUES('{rowData[0]}','{rowData[1]}','{rowData[2]}','{rowData[3]}' )")
            query=f"INSERT OR REPLACE INTO Instructor(Instructor_id,First_name,Last_name,Email,College,Department,Password) VALUES('{rowData[0]}','{rowData[1]}','{rowData[2]}','{rowData[3]}' , '{rowData[4]}', '{rowData[5]}', '{rowData[6]}')"
            
            cur.execute("SELECT COUNT(*) FROM Instructor")
            property_count = cur.fetchone()[0]
            self.InstAdm.setRowCount(property_count+1)
            tablecount=0
            result=cur.execute(query)
            


            for row in result:
                self.InstAdm.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.InstAdm.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.InstAdm.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.InstAdm.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.InstAdm.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4]))
                self.InstAdm.setItem(tablecount, 5, QtWidgets.QTableWidgetItem(row[5])) 
                self.InstAdm.setItem(tablecount, 6, QtWidgets.QTableWidgetItem(row[6])) 
                tablecount+=1
            conn.commit()
            mbox=QMessageBox()
            mbox.information(self,"Success","Instructor has been successfully added") 
            
            rowPosition = self.InstAdm.rowCount()
            self.InstAdm.insertRow(rowPosition)
            self.InstAdm.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(""))
            # self.InstAdm.setItem(rowPosition , 1, QtGui.QTableWidgetItem(""))
            # self.InstAdm.setItem(rowPosition , 2, QtGui.QTableWidgetItem(""))
            # self.InstAdm.setItem(rowPosition , 0, QtGui.QTableWidgetItem(""))
            # self.InstAdm.setItem(rowPosition , 1, QtGui.QTableWidgetItem(""))
            # self.InstAdm.setItem(rowPosition , 2, QtGui.QTableWidgetItem(""))
        

            #self.InstAdm.setCellWidget(0,2, self.combo)   
        
                #conn.commit()
            
            #self.Addsuccessfully.setText("Instructor has been successfully added")
            # mbox=QMessageBox()

            # mbox.information(self,"Success","Instructor has been successfully added") 
        else:
            mbox=QMessageBox()

            mbox.information(self,"Warning","Please Input all fields") 
    
    def getRowNumber(self, table, s):
        #result = table.findItems(s, QtCore.Qt.MatchFlag.MatchExactly)

        result = table.findItems(s, Qt.MatchExactly)
        

        rowNumber = result[0].row()
        return rowNumber

                   

    def deleteInst(self):
        InstID = self.InstIDadmin_2.text()
        if len(InstID)==0 :
            mbox=QMessageBox()
            mbox.information(self,"Warning","Please input all fields.")  
            #self.InputallFields.setText("Please input all fields.")

        else:
            conn = sqlite3.connect("Cognito.db")
            cur = conn.cursor()
            cur.execute('DELETE FROM Course WHERE Instructor_id =\''+InstID+"\'")
            cur.execute('DELETE FROM Instructor WHERE Instructor_id =\''+InstID+"\'")
            conn.commit()
            #self.DeleteSuccessfInst.setText("Instructor has been successfully deleted")
            self.InstAdm.removeRow(self.getRowNumber(self.InstAdm, InstID))
            self.InstIDadmin_2.setText("")
            mbox=QMessageBox()

            mbox.information(self,"Success","Instructor has been successfully deleted")

    def gotoAllInstInDB(self):
        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query='SELECT Instructor_id,First_name,Last_name,Email,College,Department,Password FROM Instructor'
        
        cur.execute("SELECT COUNT(*) FROM Instructor")
        property_count = cur.fetchone()[0]
        
        self.InstAdm.setRowCount(property_count+1)

        tablecount=0
        #cur.execute(query)
        results = cur.execute(query)
        
        for row in results:
            self.InstAdm.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.InstAdm.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.InstAdm.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.InstAdm.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.InstAdm.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4])) 
            self.InstAdm.setItem(tablecount, 5, QtWidgets.QTableWidgetItem(row[5]))
            self.InstAdm.setItem(tablecount, 6, QtWidgets.QTableWidgetItem(row[6])) 
 
            tablecount+=1
    def gotoExitInsDBAdmin(self):
        widget.setCurrentIndex(0)
        #n=widget.count()-1
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 
        

    def gotoGoBackInsDBAdmin(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
        print(widget.count()) 

################################################################################################################################
class AllStudentsInDB(QMainWindow):
    def __init__(self):
    
        
        super(AllStudentsInDB, self).__init__()
        loadUi("AllStudentsInDB.ui",self) 
        self.StuAdm.setHorizontalHeaderLabels(["Student_ID", "First_name","Middle_name", "Last_name","Email","Major","Level","Password"])
        self.majorsTable.setColumnWidth(0,300)
        #self.majorsTable.setHorizontalHeaderLabels(["Majors"])

       
        self.Exit.clicked.connect(self.gotoExitStuDBAdmin)
        self.GoBack.clicked.connect(self.gotoGoBackStuDBAdmin)
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))
        self.ADDBTN.clicked.connect(self.addstud)
        self.DELETESTU.clicked.connect(self.deletestud)
        self.gotoAllStuInDB()
        self.Majors()


    
    def Majors(self):

        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query='SELECT*FROM Majors'
        
        
        self.majorsTable.setRowCount(16)

        tablecount=0
        #cur.execute(query)
        results = cur.execute(query)
        
        for row in results:
            self.majorsTable.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            #self.DepartmentAndDepartment.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
            # self.DepartmentAndDepartment.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
            # self.DepartmentAndDepartment.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
            # self.DepartmentAndDepartment.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4])) 
            # self.DepartmentAndDepartment.setItem(tablecount, 5, QtWidgets.QTableWidgetItem(row[5]))
 
            tablecount+=1
                                      
    def addstud(self):
        rowCount = self.StuAdm.rowCount()
        columnCount = self.StuAdm.columnCount()

        for row in range (rowCount):
            rowData = []
            for column in range (columnCount):
                widgetItem = self.StuAdm.item(row, column)

                if(widgetItem and widgetItem.text):

                    rowData.append(widgetItem.text())
                else:
                    rowData.append('')
        self.msg(rowData)            
        
    
    def msg(self, rowData):
        if(rowData[0]!='' and rowData[1]!='' and rowData[2]!='' and rowData[3]!=''and rowData[4]!=''and rowData[5]!=''and rowData[6]!='' and rowData[7]!=''
        ):
            conn = sqlite3.connect("Cognito.db")
            cur = conn.cursor()
            #cur.execute(f"INSERT INTO Exam(Student_FName, Student_LName, Student_ID, Student_Grade) VALUES('{rowData[0]}','{rowData[1]}','{rowData[2]}','{rowData[3]}' )")
            #query=f"INSERT OR REPLACE INTO Instructor(Instructor_id,First_name,Last_name,Email,College,Department,Password) VALUES('{rowData[0]}','{rowData[1]}','{rowData[2]}','{rowData[3]}' , '{rowData[4]}', '{rowData[5]}', '{rowData[6]}')"
            query=f"INSERT OR REPLACE INTO StudentN(Student_ID, First_Name, Middle_Name, Last_Name, Email, Major,Level, Password) VALUES('{rowData[0]}','{rowData[1]}','{rowData[2]}','{rowData[3]}' , '{rowData[4]}', '{rowData[5]}', '{rowData[6]}','{rowData[7]}')"

            cur.execute("SELECT COUNT(*) FROM StudentN")
            property_count = cur.fetchone()[0]
            self.StuAdm.setRowCount(property_count+1)
            tablecount=0
            result=cur.execute(query)
            


            for row in result:
                self.StuAdm.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
                self.StuAdm.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
                self.StuAdm.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
                self.StuAdm.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
                self.StuAdm.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4]))
                self.StuAdm.setItem(tablecount, 5, QtWidgets.QTableWidgetItem(row[5])) 
                self.StuAdm.setItem(tablecount, 6, QtWidgets.QTableWidgetItem(row[6])) 
                self.StuAdm.setItem(tablecount, 7, QtWidgets.QTableWidgetItem(row[7])) 
                tablecount+=1
            conn.commit()
            mbox=QMessageBox()
            mbox.information(self,"Success","Student has been successfully added") 
            
            rowPosition = self.StuAdm.rowCount()
            self.StuAdm.insertRow(rowPosition)
            self.StuAdm.setItem(rowPosition , 0, QtWidgets.QTableWidgetItem(""))
            
        else:
            mbox=QMessageBox()

            mbox.information(self,"Warning","Please Input all fields") 
                
        
    
    def getRowNumber(self, table, s):
        #result = table.findItems(s, QtCore.Qt.MatchFlag.MatchExactly)

        result = table.findItems(s, Qt.MatchExactly)
        

        rowNumber = result[0].row()
        return rowNumber    


    def deletestud(self):
        StID = self.StudentIDadmin.text()
        if len(StID)==0 :
            
            mbox=QMessageBox()

            mbox.information(self,"Warning","Please input all fields.")                                        

        else:
            conn = sqlite3.connect("Cognito.db")
            cur = conn.cursor()
            cur.execute('DELETE FROM Course WHERE Student_ID =\''+StID+"\'")
            cur.execute('DELETE FROM StudentN WHERE Student_ID =\''+StID+"\'")
            conn.commit() 
            self.StudentIDadmin.setText("")
            self.StuAdm.removeRow(self.getRowNumber(self.StuAdm, StID))
            mbox=QMessageBox()
            mbox.information(self,"Success","Student has been successfully deleted")



            
               


    def gotoAllStuInDB(self):
       
        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query='SELECT Student_ID,First_name,Middle_name, Last_name,Email,Major,Level,Password FROM StudentN'

        cur.execute("SELECT COUNT(*) FROM StudentN")
        property_count = cur.fetchone()[0]
        
        self.StuAdm.setRowCount(property_count+1)
        tablecount=0
        #cur.execute(query)
        results = cur.execute(query)
        
        for row in results:
            self.StuAdm.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.StuAdm.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.StuAdm.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.StuAdm.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.StuAdm.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4])) 
            self.StuAdm.setItem(tablecount, 5, QtWidgets.QTableWidgetItem(row[5])) 
            self.StuAdm.setItem(tablecount, 6, QtWidgets.QTableWidgetItem(row[6])) 
            self.StuAdm.setItem(tablecount, 7, QtWidgets.QTableWidgetItem(row[7])) 
            tablecount+=1

    def gotoExitStuDBAdmin(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
    def gotoGoBackStuDBAdmin(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
##################################################################################

class ViewGrades(QDialog):

    def __init__(self, user, course):
        self.user=user
        self.course=course
        super(ViewGrades, self).__init__()
        loadUi("ViewGrade.ui",self) 
        self.username.setText(self.user)
        self.crs.setText(self.course)
        self.GoBack.clicked.connect(self.goBack)
        self.Exit.clicked.connect(self.gotoExit)
        self.ViewGradeTable.setHorizontalHeaderLabels(["Exam Name","First Name", "Last Name","Student ID","Grade"])
        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))



        conn=sqlite3.connect('Cognito.db')
        cur = conn.cursor()
        query=f"""SELECT Exam_name, Student_FName, Student_LName, Student_ID, Student_Grade FROM Exam 
        WHERE Instructor_id ='{self.user}' AND Course = '{self.course}'"""
        
        
        self.ViewGradeTable.setRowCount(5)

        tablecount=0
        results = cur.execute(query)
        
        for row in results:
            self.ViewGradeTable.setItem(tablecount, 0, QtWidgets.QTableWidgetItem(row[0]))
            self.ViewGradeTable.setItem(tablecount, 1, QtWidgets.QTableWidgetItem(row[1]))
            self.ViewGradeTable.setItem(tablecount, 2, QtWidgets.QTableWidgetItem(row[2]))
            self.ViewGradeTable.setItem(tablecount, 3, QtWidgets.QTableWidgetItem(row[3]))
            self.ViewGradeTable.setItem(tablecount, 4, QtWidgets.QTableWidgetItem(row[4])) 
            tablecount+=1

    def gotoExit(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        n=13
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid) 
################################################################################
class RecordLectureInst(QDialog):

    def __init__(self, user, course):
        self.user=user
        self.course=course
        super(RecordLectureInst, self).__init__()
        loadUi("RecordLecture.ui",self) 
        self.username.setText(self.user)
        self.crs.setText(self.course)
        self.GoBack.clicked.connect(self.goBack)
        self.Exit.clicked.connect(self.gotoExit) 
        self.startrecordlec.clicked.connect(self.gotoStartRecordLect)

        self.GoBack.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\back.png"))
        self.GoBack.setIconSize(QSize(45,45))
        self.Exit.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\ExitButt.png"))
        self.Exit.setIconSize(QSize(45,45))

        self.startrecordlec.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\recordinglec.png"))
        self.startrecordlec.setIconSize(QSize(60,60))
        # self.stoprecordlec.setIcon(QIcon("C:\\Users\\USER\\Desktop\\TeachingAssistantRobotCognito\\ImagesForDesignSystem\\stoprecording.png"))
        # self.stoprecordlec.setIconSize(QSize(65,65))

        self.worker = None
        self.go_on = False 


    def gotoExit(self):
        widget.setCurrentIndex(0)
        n=11
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid)   
    def goBack(self):
        widget.setCurrentIndex(widget.currentIndex()-1)
        n=13
        for i in range(n):
            wid = widget.widget(n)
            widget.removeWidget(wid) 

    def gotoStartRecordLect(self):

        global r
        global audio
        global source
        global transcript
        r = sr.Recognizer()
        #QApplication.processEvents()
        with sr.Microphone() as source:

            r.adjust_for_ambient_noise(source)
            self.RecordingMode.setText("Recording Now.. ")
            QtWidgets.qApp.processEvents()
            

            audio = r.listen(source)
            #QApplication.processEvents()
            transcript=r.recognize_google(audio)
           
            self.gotoStopRecordLect()

        #QApplication.processEvents()
        #self.stoprecordlec.clicked.connect(self.gotoStopRecordLect)
        #self.gotoStopRecordLect()


    def gotoStopRecordLect(self):
        self.RecordingMode.setText(" ")
        QtWidgets.qApp.processEvents()
     

        self.DoneRecor.setText("Audio Recorded Successfully \n ")
        QtWidgets.qApp.processEvents()#to show text in GUI
        QApplication.processEvents()
       
        
        with open("notes.txt", "a") as f:
                f.write(transcript)
                f.close()  
        

        with open("recorded.wav", "wb") as ff:
            ff.write(audio.get_wav_data())
            ff.close()   

         
        conn=sqlite3.connect('Cognito.db')
        with conn:
            cur=conn.cursor()
            
            cur.execute("INSERT INTO Notes_Instructor(Instructor_id, Content, Course_name)"
                        "VALUES('%s', '%s', '%s')" % (
                                                ''.join(self.user), 
                                                ''.join(transcript.replace("'", "''")),''.join(self.course), ))
            
            
    
        
###############################################################################################################################
app=QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
##################################################################################################################################
#Screens/Interfaces:
welcomeScreen= WelcomeScreen() #1
instrctorLogin=InstructorLogin() #2
studentlogin=StudentLogin()#3
studentregistration=StudentRegister()#4
instructorReg=InstructorRegister()#5
#classNoteInstr=ClassNoteIns()#7
#examSetup=ExamSetup()#9
#studentClassNote=StudentClassNote()#12
takeATTthroughFPP=TakeATTthroughFPP()#14 
facialRecSt=FacialRecSt()#13
registerFingerStInDB=RegisterFingerStInDB()#15
registerFacialStInDB=RegisterFacialStInDB()#16
admin=Admin()#18FF
afteradminlogin=AfterAdminLogin()#19
# addInstructor=AddInstructor()#20
# deleteInstructor=DeleteInstructor()#21
# addStudr=AddStudr()#22
# deleteStud=DeleteStud()#23
#allInstructorsInDB=AllInstructorsInDB()#25
# allStudentsInDB=AllStudentsInDB()#26
###This is for Choose Course Instructor deal with it instead of 17 ##27
#################STUDENT COURSE 28 
#############AFTER INST 29
#############ATTENDANCE INST 30
##########AFTER ST LOG 31
##########ATTENDANCE STU 32
##################################################################################################################################
#add widget:
widget.addWidget(welcomeScreen)#1
widget.addWidget(instrctorLogin)#2
widget.addWidget(studentregistration)
widget.addWidget(instructorReg)
widget.addWidget(studentlogin)
#widget.addWidget(afterInstructorLogin)
#widget.addWidget(classNoteInstr)
#widget.addWidget(attendanceIns)
#widget.addWidget(examSetup)
#widget.addWidget(afterLoginStudent)
#widget.addWidget(studentAttendanceRecord)
#widget.addWidget(studentClassNote)
widget.addWidget(takeATTthroughFPP)
widget.addWidget(facialRecSt)
widget.addWidget(registerFingerStInDB)
widget.addWidget(registerFacialStInDB)
#widget.addWidget(chooseCourseInst)
widget.addWidget(admin)
widget.addWidget(afteradminlogin)
#widget.addWidget(addInstructor)
#widget.addWidget(deleteInstructor)
#widget.addWidget(addStudr)
#widget.addWidget(deleteStud)
#widget.addWidget(choseCourseStudent)
#widget.addWidget(allInstructorsInDB)
#widget.addWidget(allStudentsInDB)


##################################################################################################################################
#size of window:
widget.setFixedHeight(600)
widget.setFixedWidth(1024)
widget.show()
##################################################################################################################################

########################################################################################################################
#Run application:
try:
    

    sys.exit(app.exec())
    
except:
    print("Exit") 



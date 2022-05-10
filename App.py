from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from PyQt5.uic import loadUiType

import sys
import MySQLdb
import webbrowser
import pyqrcode
from pyqrcode import QRCode
from xlsxwriter.workbook import Workbook
from datetime import datetime


ui,_ = loadUiType('Payment Gateway.ui')
LoginUi,_ = loadUiType('Login_PG.ui')



class LoginApp(QMainWindow, LoginUi):

    def __init__(self):

        QMainWindow.__init__(self)
        self.setupUi(self)
        self.handleButton()
        self.setTheme()



    def handleButton(self):

        self.pushButton_22.clicked.connect(sys.exit)
        self.pushButton_21.clicked.connect(self.LoginUser)

        self.pushButton_5.clicked.connect(self.dev_Vishwa_Linkedin)
        self.pushButton_6.clicked.connect(self.dev_Vishwa_Insta)
        self.pushButton_7.clicked.connect(self.dev_raghav_Linkedin)
        self.pushButton_8.clicked.connect(self.dev_raghav_Insta)


    def setTheme(self):

        file = open('Themes/ThemeConfig.txt', 'r')
        x = file.read()
        x = x.split(' ')
        ThemeVariable = ('Themes/' + x[-1])

        style = open(ThemeVariable)
        style = style.read()
        self.setStyleSheet(style)

    def LoginUser(self):

        uName = self.lineEdit_10.text()
        uPass = self.lineEdit_7.text()
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='YOUR_PASSWORD', db='payment')
        self.cur = self.db.cursor()

        try:

            self.cur.execute('''select uName, uPass from users''')
            uData = self.cur.fetchall()
            print(uData)
            for i in uData:
                if uName == i[0] and uPass == i[1]:
                    self.MainObj = MainApp()
                    self.MainObj.show()
                    self.hide()
                    break
                else:
                    self.label_18.setText('Incorrect credentials !')

        except:

            self.statusBar().showMessage('Unable to login !')

    def dev_Vishwa_Linkedin(self):
        webbrowser.open('https://www.linkedin.com/in/vishwa-h-a47b6852/')

    def dev_Vishwa_Insta(self):
        webbrowser.open('https://www.instagram.com/vishwa_karthik_/?hl=en')

    def dev_raghav_Linkedin(self):
        webbrowser.open('https://www.linkedin.com/in/raghavendra-vasista-l-a6384b27/')

    def dev_raghav_Insta(self):
        webbrowser.open('https://www.instagram.com/raghav_vasishta/?hl=en')


class MainApp(QMainWindow, ui):

    def __init__(self):

        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setTheme()
        self.Handle_Buttons()
        self.Handle_UI_Changes()
        self.Show_Participant()
        self.Show_Events_ComboBox()
        self.Show_Event()






    def Handle_UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)


    def Handle_Buttons(self):
        self.pushButton_3.clicked.connect(self.Open_Day_Transactions) # Side buttons#
        self.pushButton_5.clicked.connect(self.Events)
        self.pushButton_4.clicked.connect(self.Users)
        self.pushButton_6.clicked.connect(self.View_Participants)
        self.pushButton_7.clicked.connect(self.Themes)

        self.pushButton_2.clicked.connect(self.Add_New_Event)
        self.pushButton.clicked.connect(self.Add_Participant)

        self.pushButton_17.clicked.connect(self.setDarkBlue)          # Theme Buttons#
        self.pushButton_8.clicked.connect(self.setDarkOrange)
        self.pushButton_9.clicked.connect(self.setDarkGray)
        self.pushButton_18.clicked.connect(self.Combinear)

        self.pushButton_12.clicked.connect(self.Search_Event)
        self.pushButton_16.clicked.connect(self.Search_Participant)

        self.pushButton_11.clicked.connect(self.Edit_Event)
        self.pushButton_10.clicked.connect(self.Delete_Event)

        self.pushButton_13.clicked.connect(self.Add_New_User)
        self.pushButton_14.clicked.connect(self.Login)
        self.pushButton_15.clicked.connect(self.Edit_User)

        self.pushButton_19.clicked.connect(self.Logout)
        self.pushButton_20.clicked.connect(self.Excel_Export)

        self.pushButton_21.clicked.connect(self.Display_Qr)

    ############################ Trigger #######
    def showTrigger(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        try :
            self.cur.execute('''select uTotal from users''')
            data = self.cur.fetchone()
            print(data)
            self.label_39.setText(str(data[0]))
            self.lineEdit_34.setText(str(data[0]))
        except:
            pass

    ############################## download excel ########

    def Excel_Export(self):

        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        try:
            self.cur.execute('''select name, event, phone,amount from participants''')
            bill = self.cur.fetchall()
            x = datetime.now()
            xlName = 'Details-' + str(x.day) + '-' + str(x.month) + '-' + str(x.year) + '-' + str(x.hour) + '-' + str(
                x.minute) + '-' + str(x.second)
            xlDate = str(x.day) + '-' + str(x.month) + '-' + str(x.year)
            XL = Workbook(xlName + '.xlsx')
            S1 = XL.add_worksheet()

            S1.write(1, 0, 'Details' + xlDate)
            S1.write(3, 0, 'Participant Name')
            S1.write(3, 1, 'Event Name')
            S1.write(3, 2, 'Participant Phone No')
            S1.write(3, 3, 'Paid')

            rowPos = 5
            for row in bill:
                colPos = 0
                for i in row:
                    S1.write(rowPos, colPos, str(i))
                    colPos += 1
                rowPos += 1

            self.statusBar().showMessage('Participant exported')
            XL.close()

        except:
            self.statusBar().showMessage('Unable to export to excel')

    ############################### QR Code ##############

    def Display_Qr(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        try:
            Participant_Name = self.lineEdit_31.text()
            Participant_Phone = self.lineEdit_33.text()
            self.cur.execute('''select name,event,phone from participants where name=%s and phone=%s''',(Participant_Name,Participant_Phone))
            s = self.cur.fetchone()
            print(s)
            text = ('Scan QR code To view info')
            qrr = pyqrcode.create(text)
            qrr.png('QRCode/qrcode1.png', scale=5.5)
            self.label_18.setStyleSheet("background-image: url(QRCode/qrcode1.png);")

            #Execute m

        except:
            print('din happen !')


    ################################## OPENING BUTTONS #########

    def Open_Day_Transactions(self):
        self.tabWidget.setCurrentIndex(0)

    def Add_Participant(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        Participant_Name = self.lineEdit.text()
        Participant_Event = self.comboBox.currentText()
        Participant_Amount = self.lineEdit_2.text()
        Participant_PhoneNo = self.lineEdit_9.text()
        phn = Participant_PhoneNo
        lenp = len(phn)
        if lenp == 10:
            if phn.isdigit():
                self.cur.execute('''INSERT INTO participants (name,event,phone,amount) VALUES (%s,%s,%s,%s)''',(Participant_Name, Participant_Event, Participant_PhoneNo, Participant_Amount))
                self.db.commit()
                self.statusBar().showMessage(" PARTICIPANT ADDED !")
        else:
            self.statusBar().showMessage('Enter valid phone number')

        self.Show_Participant()
        self.showTrigger()


    def Show_Participant(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT name, event ,phone ,amount FROM participants''')
        data_1 = self.cur.fetchall()


        if data_1:
            self.tableWidget.setRowCount(0)
            self.tableWidget.insertRow(0)
            for row, form in enumerate(data_1):
                for column, item in enumerate(form):
                    self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                    column += 1

                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position)




    def Events(self):
        self.tabWidget.setCurrentIndex(1)

    def Users(self):
        self.tabWidget.setCurrentIndex(2)

    def View_Participants(self):
        self.tabWidget.setCurrentIndex(3)

    def Themes(self):
        self.tabWidget.setCurrentIndex(4)

    ##########################################  EVENTS ##############

    def Add_New_Event(self):
        self.db = MySQLdb.connect(host='127.0.0.1',user='root',password='vishwaH22*',db='payment')
        self.cur = self.db.cursor()

        Event_Name = self.lineEdit_3.text()
        Event_Price = self.lineEdit_5.text()
        Event_Venue = self.lineEdit_6.text()
        Event_Time = self.lineEdit_11.text()

        try:
            self.cur.execute('''INSERT INTO event (eName,eTime,ePrice,eVenue) VALUES (%s,%s,%s,%s)''',(Event_Name,Event_Time,Event_Price,Event_Venue))
            self.db.commit()
            self.statusBar().showMessage(" EVENT ADDED !")

            self.lineEdit_3.setText('')  # clear record after 1st Iteration
            self.lineEdit_5.setText('')
            self.lineEdit_6.setText('')
            self.lineEdit_11.setText('')

            self.Show_Event()
            self.Show_Events_ComboBox()


        except :
            warning = QMessageBox.warning(self, 'Event Clashed ', "Your New Event gets Clashed ! ",QMessageBox.Yes)
            if warning == QMessageBox.Yes:
                pass


    def Show_Event(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        self.cur.execute('''SELECT eName, ePrice FROM Event''')
        data = self.cur.fetchall()


        if data:
            self.tableWidget_2.setRowCount(0)
            self.tableWidget_2.insertRow(0)
            for row, form in enumerate(data):
                for column , item in enumerate(form):
                    self.tableWidget_2.setItem(row , column, QTableWidgetItem(str(item)))
                    column+=1

                row_position = self.tableWidget_2.rowCount()
                self.tableWidget_2.insertRow(row_position)





    def Search_Event(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        Event_Name = self.lineEdit_20.text()

        self.cur.execute('''SELECT eName ,eTime,ePrice,eVenue FROM event WHERE eName = %s''' , [(Event_Name)] )

        data1 = self.cur.fetchone()



        self.lineEdit_4.setText(data1[0])
        self.lineEdit_32.setText(str(data1[1]))
        self.lineEdit_8.setText(str(data1[2]))
        self.lineEdit_12.setText(data1[3])


    def Edit_Event(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        Event_Name = self.lineEdit_4.text()
        Event_Time = self.lineEdit_32.text()
        Event_Price = self.lineEdit_8.text()
        Event_Venue = self.lineEdit_12.text()

        Search_Event_Title = self.lineEdit_20.text()

        self.cur.execute('''UPDATE event SET eName=%s ,eTime=%s, eVenue=%s, ePrice=%s   WHERE eName=%s ''',(Event_Name,Event_Time,Event_Venue,Event_Price,Search_Event_Title))
        self.db.commit()
        self.statusBar().showMessage("EVENT MODIFIED !")



    def Delete_Event(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        Search_Event_Title = self.lineEdit_20.text()

        warning = QMessageBox.warning(self , 'Delete Event ? ' , "Are you Sure of Deleting this ? ", QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes :
            self.cur.execute('''DELETE FROM event WHERE eName=%s''',[(Search_Event_Title)])
            self.db.commit()
            self.statusBar().showMessage("EVENT DELETED !")

        self.Show_Event()


    ########################################## USERS #################

    def Add_New_User(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()


        UserName = self.lineEdit_22.text()
        password = self.lineEdit_23.text()
        Email = self.lineEdit_21.text()
        ConPassword = self.lineEdit_24.text()
        try:
            if password == ConPassword :
                self.cur.execute('''INSERT INTO users(uName,uPass,uMail) VALUES (%s ,%s,%s) ''',(UserName,password,Email))
                self.db.commit()
                self.statusBar().showMessage("NEW USER ADDED !")
            else:
                self.label_9.setText("PASSWORD DONT MATCH ! RECHECK .")
        except:
            self.statusBar().showMessage('User Name Exists !')




    def Login(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        Username = self.lineEdit_26.text()
        Password = self.lineEdit_25.text()

        sql = '''SELECT * FROM users'''
        self.cur.execute(sql)
        data = self.cur.fetchall()
        for row in data:
            if Username == row[1] and Password == row[2]:
                self.statusBar().showMessage("Valid Client !")
                self.groupBox_4.setEnabled(True)
                self.label_3.setText(Username)

                self.lineEdit_30.setText(row[1])
                self.lineEdit_29.setText(row[3])


    def Edit_User(self):


        Email = self.lineEdit_29.text()
        Username = self.lineEdit_30.text()
        tempUsername = self.lineEdit_26.text()
        Password = self.lineEdit_28.text()
        ConPassword = self.lineEdit_27.text()
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()


        if Password == ConPassword :


            self.cur.execute('''UPDATE users SET uName=%s,uPass=%s,uMail=%s WHERE uName=%s ''',(Username,Password,Email,tempUsername))
            self.db.commit()
            self.statusBar().showMessage("Credentials Modified !")

        else:
            self.statusBar().showMessage("Password Dont Match !")



    ########################################## VIEW PARTICIPANT #######################

    def View_Participant(self):
        pass

    def Search_Participant(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        Participant_Name = self.lineEdit_31.text()
        Participant_Phone = self.lineEdit_33.text()


        self.cur.execute('''call fetchParticipant(%s,%s)''',(Participant_Name,Participant_Phone))

        data2 = self.cur.fetchone()
        print(data2)



        self.label_35.setText(data2[0])
        self.label_37.setText(data2[1])
        self.label_42.setText(str(data2[2]))




    ############################################## THEMES TAB ##########


    def setTheme(self):

        file = open('Themes/ThemeConfig.txt', 'r')
        x = file.read()
        x = x.split(' ')
        ThemeVariable = ('Themes/' + x[-1])

        style = open(ThemeVariable)
        style = style.read()
        self.setStyleSheet(style)

    def setDarkBlue(self):

        file = open('Themes/ThemeConfig.txt', 'w')
        file.write('Default theme: darkstyle.css')
        file.close()
        self.setTheme()

    def setDarkOrange(self):

        file = open('Themes/ThemeConfig.txt', 'w')
        file.write('Default theme: darkorange.css')
        file.close()
        self.setTheme()

    def setDarkGray(self):

        file = open('Themes/ThemeConfig.txt', 'w')
        file.write('Default theme: darkgray.css')
        file.close()
        self.setTheme()

    def Combinear(self):

        file = open('Themes/ThemeConfig.txt', 'w')
        file.write('Default theme: Combinear.css')
        file.close()
        self.setTheme()

################# combo box ######
    def Show_Events_ComboBox(self):
        self.db = MySQLdb.connect(host='127.0.0.1', user='root', password='vishwaH22*', db='payment')
        self.cur = self.db.cursor()

        self.cur.execute(''' SELECT eName from event''')
        data_2 = self.cur.fetchall()
        self.comboBox.clear()

        for eName in data_2:
            self.comboBox.addItem(eName[0])

    def Logout(self):

        warning = QMessageBox.warning(self, 'Sure to sign out ?', "Are you Sure you wanna logout  !",
                                      QMessageBox.Yes | QMessageBox.No)

        if warning == QMessageBox.Yes:

            self.LoopObj = LoginApp()
            self.LoopObj.show()
            self.hide()


def main():

    Final = QApplication(sys.argv)
    Windows = LoginApp()
    Windows.show()
    Final.exec_()

if __name__ == '__main__':

    main()

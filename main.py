from pymodbus.client import ModbusTcpClient
from PyQt5.QtWidgets import *
from PyQt5 import uic

import time
import urControlModbus
import threading

form_class=uic.loadUiType(f"./ui_main.ui")[0]


class MainUi(QMainWindow,form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.robot=None


        self.pb_connect.clicked.connect(self.connect)
        self.thread_tcp=threading.Thread(target=self.checkingTCP,daemon=True)

        self.pb_send.clicked.connect(self.move)



    def closeEvent(self,evt):
        if self.client != None:
            self.client.close()
            self.client=None


    def connect(self):
        if self.robot != None:
            try:
                self.robot = None
                self.gbox_control.setDisabled(True)
            except:
                self.label_network.setText("Network : close error!, do retry")
        try:
            self.robot=urControlModbus.UrModbusController(self.lineEdit_ip.text())
            self.robot.client.connect()
            self.label_network.setText(f"Network : success({self.lineEdit_ip.text()}:502)")
            self.gbox_control.setEnabled(True)
            self.thread_tcp.start()

        except:
            self.label_network.setText("Network : connecting error!, do retry")

    def closeEvent(self):
        self.robot.client.close()


    def checkingTCP(self):
        tcp = self.robot.func_checkTCP()
        self.lbl_tcpCurrent.setText(f"TCP current :\n [x:{tcp[0]}] [y:{tcp[1]}] [z:{tcp[2]}] [rx:{tcp[3]}] [ry:{tcp[4]}] [rz:{tcp[5]}]")
        time.sleep(0.05)
        

    def move(self):
        self.robot.func_moveTCP([float(self.lineEdit_1.text()),float(self.lineEdit_2.text()),float(self.lineEdit_3.text()),float(self.lineEdit_4.text()),float(self.lineEdit_5.text()),float(self.lineEdit_6.text())])


   

if __name__=="__main__":
    app=QApplication([])
    w=MainUi()
    w.show()
    app.exec()
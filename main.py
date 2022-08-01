from PyQt6 import QtWidgets, uic
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QIODeviceBase
from pyqtgraph import PlotWidget
import pyqtgraph as pg
import sys
import numpy as np

app = QtWidgets.QApplication([])
window = uic.loadUi('untitled.ui')
serial = QSerialPort()
serial.setBaudRate(9600)
portlist = []
ports = QSerialPortInfo.availablePorts()
for port in ports:
    portlist.append(port.portName())
window.comL.addItems(portlist)


#window.graph.setBackground('w')

chanell_list = [[True, 102], [True, 102], [True, 102]]

list_graf_x = []
for i in range(100):
    list_graf_x.append(i)
list_graf_y = []
for i in range(100):
    list_graf_y.append(0)


def Calibration():
    global data_save
    count = 0
    for data_ in data_save:
        if count == 3:
            break
        elif int(data_)<103 and int(data_)>91:
            chanell_list[count][0] = True
            chanell_list[count][1] = int(data_)
        else:
            chanell_list[count][0] = False
        count+=1

def Calculation_voltage(analog, index):
    if chanell_list[index][0]:
        voltage = (int(analog)*5)/1024
        voltage=round(voltage,3)
        return voltage
    else:
        return 'NULL'

def Calculation_pressure(analog, index):
    if chanell_list[index][0]:
        pressure =int(analog)-chanell_list[index][1]
        pressure = pressure/13
        pressure = round(pressure,2)
        return pressure
    else:
        return 'NULL'

def Open_port():
    try:
        serial.setPortName(window.comL.currentText())
        serial.close()
        serial.open(QIODeviceBase.OpenModeFlag.ReadWrite)
        if serial.isOpen():
            window.label_.setText("Порт открыт")
        else:
            window.label_.setText(serial.error())
    except:
        print(serial.error())


def Close_port():
    serial.close()
    if not serial.isOpen():
        window.label_.setText("Порт закрыт")
    else:
        window.label_.setText(serial.error())

def Read_():
    global list_graf_x
    global list_graf_y
    try:
        global data_save
        line_ = str(serial.readLine(), 'utf-8')
        data = line_.split(',')
        data_save=data
        window.sensor_1.setText(str(Calculation_pressure(data[0], 0)))
        window.sensor_11.setText(str(Calculation_voltage(data[0], 0)))

        window.sensor_2.setText(str(Calculation_pressure(data[1], 1)))
        window.sensor_21.setText(str(Calculation_voltage(data[1], 1)))

        window.sensor_3.setText(str(Calculation_pressure(data[2], 2)))
        window.sensor_31.setText(str(Calculation_voltage(data[2], 2)))
    except Exception as exc:
        print(exc)


    list_graf_y.append(Calculation_pressure(data[0], 0))
    list_graf_y.pop(0)
    window.graph.clear()
    pen = pg.mkPen(color=(255, 0, 0))
    window.graph.plot(list_graf_x, list_graf_y, pen = pen)
    window.graph.plot([0,1,2,3,4,5,6,7,8,9,10,11,12], [0,1,2,3,4,5,6,7,8,9,10,11,12])


window.openB.clicked.connect(Open_port)
window.closeB.clicked.connect(Close_port)
window.resetB.clicked.connect(Calibration)
serial.readyRead.connect(Read_)

window.show()
app.exec()
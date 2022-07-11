from PyQt6 import QtWidgets, uic
from PyQt6.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt6.QtCore import QIODeviceBase


app = QtWidgets.QApplication([])
window = uic.loadUi('untitled.ui')
serial = QSerialPort()
serial.setBaudRate(9600)
portlist = []
ports = QSerialPortInfo.availablePorts()
for port in ports:
    portlist.append(port.portName())
window.comL.addItems(portlist)

chanell_list = [[True, 102], [True, 102], [True, 102]]

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
    serial.setPortName(window.comL.currentText())
    serial.close()
    serial.open(QIODeviceBase.OpenModeFlag.ReadWrite)
    if serial.isOpen():
        window.label_.setText("Порт открыт")
    else:
        window.label_.setText(serial.error())
    print(serial.error())
    print(serial.isOpen())

def Close_port():
    serial.close()
    if not serial.isOpen():
        window.label_.setText("Порт закрыт")
    else:
        window.label_.setText(serial.error())

def Read_():
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


window.openB.clicked.connect(Open_port)
window.closeB.clicked.connect(Close_port)
window.resetB.clicked.connect(Calibration)
serial.readyRead.connect(Read_)

window.show()
app.exec()
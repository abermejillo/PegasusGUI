import sys, os
import traceback

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QPushButton, QMessageBox
from ui_Drummer_ANC350_v2 import Ui_Drummer_ANC350
from make_status_message import make_status_message

from PyANC350v4 import Positioner
import time

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_Drummer_ANC350()
        self.ui.setupUi(self)

        # Set the title:
        self.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.setWindowTitle("Drummer - ANC350")
        self.status_message = make_status_message()
        self.ui.statusbar.showMessage(self.status_message)

        # Set the connections:
        self.ui.actionAbout.triggered.connect(self.about)
        self.ui.b_connect.clicked.connect(self.connectInstrument)
        self.ui.b_disconnect.clicked.connect(self.disconnectInstrument)

        self.ui.b_minus_x.pressed.connect(self.b_minus_x_func)
        self.ui.b_minus_y.pressed.connect(self.b_minus_y_func)
        self.ui.b_minus_z.pressed.connect(self.b_minus_z_func)

        self.ui.b_minus_x.released.connect(self.b_minus_x_func_released)
        self.ui.b_minus_y.released.connect(self.b_minus_y_func_released)
        self.ui.b_minus_z.released.connect(self.b_minus_z_func_released)

        self.ui.b_plus_x.pressed.connect(self.b_plus_x_func)
        self.ui.b_plus_y.pressed.connect(self.b_plus_y_func)
        self.ui.b_plus_z.pressed.connect(self.b_plus_z_func)
        
        self.ui.b_plus_x.released.connect(self.b_plus_x_func_released)
        self.ui.b_plus_y.released.connect(self.b_plus_y_func_released)
        self.ui.b_plus_z.released.connect(self.b_plus_z_func_released)

        self.ui.sb_freq_x.valueChanged.connect(self.sb_freq_x_func)
        self.ui.sb_freq_y.valueChanged.connect(self.sb_freq_y_func)
        self.ui.sb_freq_z.valueChanged.connect(self.sb_freq_z_func)

        self.ui.sb_amp_x.valueChanged.connect(self.sb_amp_x_func)
        self.ui.sb_amp_y.valueChanged.connect(self.sb_amp_y_func)
        self.ui.sb_amp_z.valueChanged.connect(self.sb_amp_z_func)

        self.ui.slider_x.valueChanged.connect(self.slider_x_func)
        self.ui.slider_y.valueChanged.connect(self.slider_y_func)
        self.ui.slider_z.valueChanged.connect(self.slider_z_func)

        # Set initial settings:

        self.refresh_time_ms = 200
        
        self.ui.b_connect.setEnabled(1)
        self.ui.b_disconnect.setEnabled(0)
        self.ui.groupBox_X.setEnabled(0)
        self.ui.groupBox_Y.setEnabled(0)
        self.ui.groupBox_Z.setEnabled(0)

        # my_bound = [None,None]
        # self.ui.sb_freq_x.setOpts(bounds=my_bound, siPrefix=True, dec=True, compactHeight=False, step = 10)
        # self.ui.sb_freq_x.setValue(float(start))

        self.timer1=QtCore.QTimer() # timer1 for graph updates
        self.timer1.timeout.connect(self.updateReading)


    def connectInstrument(self):
        try:

            self.ax = {'x':0,'y':1,'z':2}
            self.anc = Positioner()

            self.timer1.start(self.refresh_time_ms)
            self.time0=time.time()
            
            value = self.anc.getAmplitude(self.ax['x'])
            self.ui.sb_amp_x.setValue(value)
            value = self.anc.getAmplitude(self.ax['y'])
            self.ui.sb_amp_y.setValue(value)
            value = self.anc.getAmplitude(self.ax['z'])
            self.ui.sb_amp_z.setValue(value)
            
            value = self.anc.getFrequency(self.ax['x'])
            self.ui.sb_freq_x.setValue(value)
            value = self.anc.getFrequency(self.ax['y'])
            self.ui.sb_freq_y.setValue(value)
            value = self.anc.getFrequency(self.ax['z'])
            self.ui.sb_freq_z.setValue(value)
            
            self.ui.b_connect.setEnabled(0)
            self.ui.b_disconnect.setEnabled(1)
            self.ui.groupBox_X.setEnabled(1)
            self.ui.groupBox_Y.setEnabled(1)
            self.ui.groupBox_Z.setEnabled(1)
            
        except Exception as exception:
            message = "An exception occurred!\n"
            message += f"\n\t{exception.args[0]}\n"
            message += f"\nType:\t{type(exception).__name__}\n"
            message += f"\nTraceback:\n{traceback.format_exc()}"
            print(message)
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setText(f"{type(exception).__name__}!")
            msgBox.setInformativeText(f"{exception.args[0]}")
            msgBox.setDetailedText(message)
            msgBox.setWindowTitle("An exception occurred!")
            try:
                msgBox.setWindowIcon(QtGui.QIcon('icon.ico'))
            except:
                pass
            msgBox.exec_()


    def disconnectInstrument(self):
        self.anc.disconnect()
        self.ui.b_connect.setEnabled(1)
        self.ui.b_disconnect.setEnabled(0)
        self.ui.groupBox_X.setEnabled(0)
        self.ui.groupBox_Y.setEnabled(0)
        self.ui.groupBox_Z.setEnabled(0)

    def b_minus_x_func(self):
        if(self.anc.getPosition(self.ax['x']) >=0):
            if(self.ui.slider_x.value() == 0):
                self.anc.startSingleStep(0, 1)
            else:
                self.anc.startContinuousMove(0, 1, 1)
        else:
            if(self.ui.slider_x.value() == 0):
                self.anc.startSingleStep(0, 0)
            else:
                self.anc.startContinuousMove(0, 1, 0)
        # print('getActuatorName',self.anc.getActuatorName(self.ax['x']))
        # print('getActuatorType',self.anc.getActuatorType(self.ax['x']))
        # print('getAmplitude',self.anc.getAmplitude(self.ax['x']))
        # print('getAxisStatus',self.anc.getAxisStatus(self.ax['x']))
        # print('getDeviceConfig',self.anc.getDeviceConfig())
        # print('getDeviceInfo',self.anc.getDeviceInfo())
        # print('getFirmwareVersion',self.anc.getFirmwareVersion())
        # print('getFrequency',self.anc.getFrequency(self.ax['x']))
        # print('getPosition',self.anc.getPosition(self.ax['x']))

    def b_minus_y_func(self):
        if(self.anc.getPosition(self.ax['y']) >=0):
            if(self.ui.slider_y.value() == 0):
                self.anc.startSingleStep(1, 0)
            else:
                self.anc.startContinuousMove(1, 1, 0)
        else:
            if(self.ui.slider_y.value() == 0):
                self.anc.startSingleStep(1, 1)
            else:
                self.anc.startContinuousMove(1, 1, 1)

    def b_minus_z_func(self):
        if(self.anc.getPosition(self.ax['z']) >=0):
            if(self.ui.slider_z.value() == 0):
                self.anc.startSingleStep(2, 1)
            else:
                self.anc.startContinuousMove(2, 1, 1)
        else:
            if(self.ui.slider_z.value() == 0):
                self.anc.startSingleStep(2, 0)
            else:
                self.anc.startContinuousMove(2, 1, 0)

    def b_minus_x_func_released(self):
        if(self.anc.getPosition(self.ax['x']) >=0):
            if(self.ui.slider_x.value() == 1):
                self.anc.startContinuousMove(0, 0, 1)
            else:
                pass
        else:
            if(self.ui.slider_x.value() == 1):
                self.anc.startContinuousMove(0, 0, 0)
            else:
                pass
    
    def b_minus_y_func_released(self):
        if(self.anc.getPosition(self.ax['y']) >=0):
            if(self.ui.slider_y.value() == 1):
                self.anc.startContinuousMove(1, 0, 0)
            else:
                pass
        else:
            if(self.ui.slider_y.value() == 1):
                self.anc.startContinuousMove(1, 0, 1)
            else:
                pass
            
    def b_minus_z_func_released(self):
        if(self.anc.getPosition(self.ax['z']) >=0):
            if(self.ui.slider_z.value() == 1):
                self.anc.startContinuousMove(2, 0, 1)
            else:
                pass
        else:
            if(self.ui.slider_z.value() == 1):
                self.anc.startContinuousMove(2, 0, 0)
            else:
                pass

    def b_plus_x_func(self):
        if(self.anc.getPosition(self.ax['x']) >=0):
            if(self.ui.slider_x.value() == 0):
                self.anc.startSingleStep(0, 0)
            else:
                self.anc.startContinuousMove(0, 1, 0)
        else:
            if(self.ui.slider_x.value() == 0):
                self.anc.startSingleStep(0, 1)
            else:
                self.anc.startContinuousMove(0, 1, 1)

    def b_plus_y_func(self):
        if(self.anc.getPosition(self.ax['y']) >=0):
            if(self.ui.slider_y.value() == 0):
                self.anc.startSingleStep(1, 1)
            else:
                self.anc.startContinuousMove(1, 1, 1)
        else:
            if(self.ui.slider_y.value() == 0):
                self.anc.startSingleStep(1, 0)
            else:
                self.anc.startContinuousMove(1, 1, 0)

    def b_plus_z_func(self):
        if(self.anc.getPosition(self.ax['z']) >=0):
            if(self.ui.slider_z.value() == 0):
                self.anc.startSingleStep(2, 0)
            else:
                self.anc.startContinuousMove(2, 1, 0)
        else:
            if(self.ui.slider_z.value() == 0):
                self.anc.startSingleStep(2, 1)
            else:
                self.anc.startContinuousMove(2, 1, 1)

    def b_plus_x_func_released(self):
        if(self.anc.getPosition(self.ax['x']) >=0):
            if(self.ui.slider_x.value() == 1):
                self.anc.startContinuousMove(0, 0, 0)
            else:
                pass
        else:
            if(self.ui.slider_x.value() == 1):
                self.anc.startContinuousMove(0, 0, 1)
            else:
                pass
    
    def b_plus_y_func_released(self):
        if(self.anc.getPosition(self.ax['y']) >=0):
            if(self.ui.slider_y.value() == 1):
                self.anc.startContinuousMove(1, 0, 1)
            else:
                pass
        else:
            if(self.ui.slider_y.value() == 1):
                self.anc.startContinuousMove(1, 0, 0)
            else:
                pass
            
    def b_plus_z_func_released(self):
        if(self.anc.getPosition(self.ax['z']) >=0):
            if(self.ui.slider_z.value() == 1):
                self.anc.startContinuousMove(2, 0, 0)
            else:
                pass
        else:
            if(self.ui.slider_z.value() == 1):
                self.anc.startContinuousMove(2, 0, 1)
            else:
                pass
    
    def sb_freq_x_func(self, value):
        self.anc.setFrequency(self.ax['x'],value)

    def sb_freq_y_func(self, value):
        self.anc.setFrequency(self.ax['y'],value)

    def sb_freq_z_func(self, value):
        self.anc.setFrequency(self.ax['z'],value)

    def sb_amp_x_func(self, value):
        self.anc.setAmplitude(self.ax['x'],value)

    def sb_amp_y_func(self, value):
        self.anc.setAmplitude(self.ax['y'],value)

    def sb_amp_z_func(self, value):
        self.anc.setAmplitude(self.ax['z'],value)

    def slider_x_func(self):
        print(self.ui.slider_x.value())

    def slider_y_func(self):
        print(self.ui.slider_y.value())

    def slider_z_func(self):
        print(self.ui.slider_z.value())

    def event(self, e):
        if e.type() == QtCore.QEvent.StatusTip:
            if e.tip() == '':
                e = QtGui.QStatusTipEvent(self.status_message)  # Set this to whatever you like
        return super().event(e)

    """
    Close event
    """
    def closeEvent(self, event):

        reply = QtWidgets.QMessageBox.warning(self, 'Quit', 'Do you really want to close?',
                                               QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if reply == QtWidgets.QMessageBox.Yes:
            self.disconnectInstrument()
            event.accept()
        else:
            event.ignore()

    def about(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Information)
        msgBox.setWindowTitle("About Drummer - ANC350!")
        msgBox.setText(f"Drummer is created using Python 3.9. (PyQt5).\nIcons by Yusuke Kamiyamane.")
        msgBox.setInformativeText(f"In case of doubts, please contact\nsamuel.manas@uv.es\nSMV - 2022")
        text = f"\nPython: \thttps://www.python.org/"
        text += f"\r\nPyQt5: \thttps://pypi.org/project/PyQt5/"
        text += f"\r\nIcons: \thttps://p.yusukekamiyamane.com/\n\tp.yusukekamiyamane\n\tFugue Icons (fugue-icons-3.5.6)"
        msgBox.setDetailedText(text)
        try:
            msgBox.setWindowIcon(QtGui.QIcon('icon.ico'))
        except:
            pass
        msgBox.exec_()

    def updateReading(self):
        value = (self.anc.getPosition(self.ax['x']))/1e-6  # From m to um.
        self.ui.l_pos_x.setText("%.4f"%value)

        value = (self.anc.getPosition(self.ax['y']))/1e-6  # From m to um.
        self.ui.l_pos_y.setText("%.4f"%value)

        value = (self.anc.getPosition(self.ax['z']))/1e-6  # From m to um.
        self.ui.l_pos_z.setText("%.4f"%value)


app = QtWidgets.QApplication([])
application = MainWindow()
application.show()
sys.exit(app.exec())

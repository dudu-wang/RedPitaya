"""GUI for controlling PID commands"""

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import rp_pid as rp

class MainWindow(QtWidgets.QMainWindow):
    """Main application class"""

    def __init__(self):
        super().__init__()
        self.left = 20
        self.top = 50
        self.width = 640
        self.height = 480

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_grid_layout()

        red_pitaya = rp.RedPitaya(sys.argv[1])

        self.show()

    def create_grid_layout(self):
        self.horizontalGroupBox = QtWidgets.QGroupBox("Grid")
        layout = QtWidgets.QGridLayout()

        layout.addWidget(QtWidgets.QLabel('Input 1, Output 1'),0,0)
        rs_11 = layout.addWidget(QtWidgets.QCheckBox('Integrator reset'),1,0)
        rs_11.stateChanged.connect(self.reset_state(1,2))


        layout.addWidget(QtWidgets.QLabel('Input 1, Output 2'),0,2)




        layout.addWidget(QtWidgets.QLabel('Input 2, Output 1'),0,3)




        layout.addWidget(QtWidgets.QLabel('Input 2, Output 2'),0,4)





        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)

        wid.setLayout(layout)

    def reset_state(self, num_in, num_out, state):
        
        if state == QtCore.Qt.Checked:
            red_pitaya.set_setpoint(num_in, num_out, True)
        else:
            red_pitaya.set_setpoint(num_in, num_out, False)
            
        
if __name__ == '__main__':
    qt_app = QtWidgets.QApplication(sys.argv)

    Main_Window = MainWindow()

    sys.exit(qt_app.exec_())

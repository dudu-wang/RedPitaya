"""GUI for controlling PID commands"""

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import rp_pid as rp

class MainWindow(QtWidgets.QMainWindow):
    """Main application class"""

    def __init__(self):
        super().__init__()
        self.red_pitaya = rp.RedPitaya(sys.argv[1])

        self.title = 'RedPitaya PID commands'
        self.left = 20
        self.top = 50
        self.width = 640
        self.height = 480

        self.setGeometry(self.left, self.top, self.width, self.height)

        self.create_grid_layout()

        self.show()

    def create_grid_layout(self):
        """Creates grid of controls"""
        self.horizontalGroupBox = QtWidgets.QGroupBox("Grid")
        layout = QtWidgets.QGridLayout()


        layout.addWidget(QtWidgets.QLabel('Input 1, Output 1'), 0, 0)

        os_1 = QtWidgets.QCheckBox('Fast analog output')
        os_1.stateChanged.connect(lambda state: self.output_state(state, 1))
        layout.addWidget(os_1, 1, 0)

        rs_11 = QtWidgets.QCheckBox('Integrator reset')
        rs_11.stateChanged.connect(lambda state: self.reset_state(state, 1, 1))
        layout.addWidget(rs_11, 2, 0)

        hs_11 = QtWidgets.QCheckBox('Integrator hold')
        hs_11.stateChanged.connect(lambda state: self.hold_state(state, 1, 1))
        layout.addWidget(hs_11, 3, 0)

        as_11 = QtWidgets.QCheckBox('Automatic integrator reset')
        as_11.stateChanged.connect(lambda state: self.auto_state(state, 1, 1))
        layout.addWidget(as_11, 4, 0)

        is_11 = QtWidgets.QCheckBox('Invert sign of output')
        is_11.stateChanged.connect(lambda state: self.auto_state(state, 1, 1))
        layout.addWidget(is_11, 5, 0)

        rel_11 = QtWidgets.QCheckBox('PID relock')
        rel_11.stateChanged.connect(lambda state: self.relock_state(state, 1, 1))
        layout.addWidget(rel_11, 6, 0)


        layout.addWidget(QtWidgets.QLabel('Input 1, Output 2'), 0, 1)

        rs_12 = QtWidgets.QCheckBox('Integrator reset')
        rs_12.stateChanged.connect(lambda state: self.reset_state(state, 1, 2))
        layout.addWidget(rs_12, 2, 1)

        hs_12 = QtWidgets.QCheckBox('Integrator hold')
        hs_12.stateChanged.connect(lambda state: self.hold_state(state, 1, 2))
        layout.addWidget(hs_12, 3, 1)

        as_12 = QtWidgets.QCheckBox('Automatic integrator reset')
        as_12.stateChanged.connect(lambda state: self.auto_state(state, 1, 2))
        layout.addWidget(as_12, 4, 1)

        is_12 = QtWidgets.QCheckBox('Invert sign of output')
        is_12.stateChanged.connect(lambda state: self.auto_state(state, 1, 2))
        layout.addWidget(is_12, 5, 1)

        rel_12 = QtWidgets.QCheckBox('PID relock')
        rel_12.stateChanged.connect(lambda state: self.relock_state(state, 1, 2))
        layout.addWidget(rel_12, 6, 1)

        layout.addWidget(QtWidgets.QLabel('Input 2, Output 1'), 0, 2)
        
        os_2 = QtWidgets.QCheckBox('Fast analog output')
        os_2.stateChanged.connect(lambda state: self.output_state(state, 2))
        layout.addWidget(os_2, 1, 2)

        rs_21 = QtWidgets.QCheckBox('Integrator reset')
        rs_21.stateChanged.connect(lambda state: self.reset_state(state, 2, 1))
        layout.addWidget(rs_21, 2, 2)

        hs_21 = QtWidgets.QCheckBox('Integrator hold')
        hs_21.stateChanged.connect(lambda state: self.hold_state(state, 2, 1))
        layout.addWidget(hs_21, 3, 2)

        as_21 = QtWidgets.QCheckBox('Automatic integrator reset')
        as_21.stateChanged.connect(lambda state: self.auto_state(state, 2, 1))
        layout.addWidget(as_21, 4, 2)

        is_21 = QtWidgets.QCheckBox('Invert sign of output')
        is_21.stateChanged.connect(lambda state: self.auto_state(state, 2, 1))
        layout.addWidget(is_21, 5, 2)

        rel_21 = QtWidgets.QCheckBox('PID relock')
        rel_21.stateChanged.connect(lambda state: self.relock_state(state, 2, 1))
        layout.addWidget(rel_21, 6, 2)

        layout.addWidget(QtWidgets.QLabel('Input 2, Output 2'), 0, 3)
        
        rs_22 = QtWidgets.QCheckBox('Integrator reset')
        rs_22.stateChanged.connect(lambda state: self.reset_state(state, 2, 2))
        layout.addWidget(rs_22, 2, 3)

        hs_22 = QtWidgets.QCheckBox('Integrator hold')
        hs_22.stateChanged.connect(lambda state: self.hold_state(state, 2, 2))
        layout.addWidget(hs_22, 3, 3)

        as_22 = QtWidgets.QCheckBox('Automatic integrator reset')
        as_22.stateChanged.connect(lambda state: self.auto_state(state, 2, 2))
        layout.addWidget(as_22, 4, 3)

        is_22 = QtWidgets.QCheckBox('Invert sign of output')
        is_22.stateChanged.connect(lambda state: self.auto_state(state, 2, 2))
        layout.addWidget(is_22, 5, 3)

        rel_22 = QtWidgets.QCheckBox('PID relock')
        rel_22.stateChanged.connect(lambda state: self.relock_state(state, 2, 2))
        layout.addWidget(rel_22, 6, 3)

        wid = QtWidgets.QWidget(self)
        self.setCentralWidget(wid)

        wid.setLayout(layout)

    def output_state(self, state, num_out):
        """Disable or enable fast analog outputs."""
        if state == QtCore.Qt.Checked:
            self.red_pitaya.set_output_state(num_out, True)
        else:
            self.red_pitaya.set_output_state(num_out, False)     

    def reset_state(self, state, num_in, num_out):
        """Reset the integrator register."""
        if state == QtCore.Qt.Checked:
            self.red_pitaya.set_int_reset_state(num_in, num_out, True)
        else:
            self.red_pitaya.set_int_reset_state(num_in, num_out, False)

    def hold_state(self, state, num_in, num_out):
        """Hold the status of the integrator register."""
        if state == QtCore.Qt.Checked:
            self.red_pitaya.set_int_hold_state(num_in, num_out, True)
        else:
            self.red_pitaya.set_int_hold_state(num_in, num_out, False)

    def auto_state(self, state, num_in, num_out):
        """If enabled, the integrator register is reset when the PID output hits the configured
        limit."""
        if state == QtCore.Qt.Checked:
            self.red_pitaya.set_int_auto_state(num_in, num_out, True)
        else:
            self.red_pitaya.set_int_auto_state(num_in, num_out, False)

    def inv_state(self, state, num_in, num_out):
        """Invert the sign of the PID output."""
        if state == QtCore.Qt.Checked:
            self.red_pitaya.set_inv_state(num_in, num_out, True)
        else:
            self.red_pitaya.set_inv_state(num_in, num_out, False)

    def relock_state(self, state, num_in, num_out):
        """Enable or disable the PID relock feature. (See rp_pid.py for further details)"""
        if state == QtCore.Qt.Checked:
            self.red_pitaya.set_relock_state(num_in, num_out, True)
        else:
            self.red_pitaya.set_relock_state(num_in, num_out, False)

if __name__ == '__main__':
    qt_app = QtWidgets.QApplication(sys.argv)

    Main_Window = MainWindow()

    sys.exit(qt_app.exec_())
    

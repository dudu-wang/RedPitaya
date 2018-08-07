"""This module contains drivers for the Red Pitaya."""

import socket

# pylint: disable=R0904
class RedPitaya(object):
    """Class that represents the Red Pitaya. 
    
    :num_int: Input 1 or 2

    :num_out: Output 1 or 2
    """
    delimiter = '\r\n'

    def __init__(self, host, timeout=None, port=5000):
        """Initialize object and open IP connection.
        Host IP should be a string in parentheses, like '192.168.1.100'.
        """
        self.host = host
        self.port = port
        self.timeout = timeout

        try:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            if timeout is not None:
                self._socket.settimeout(timeout)

            self._socket.connect((host, port))

        except socket.error as e:
            print('SCPI >> connect({:s}:{:d}) failed: {:s}'.format(host, port, e))

    def __del__(self):
        if self._socket is not None:
            self._socket.close()
        self._socket = None

    def close(self):
        """Close IP connection."""
        self.__del__()

    def rx_txt(self, chunksize=4096):
        """Receive text string and return it after removing the delimiter."""
        msg = ''
        while 1:
            chunk = self._socket.recv(chunksize + len(self.delimiter)).decode('utf-8')
            # Receive chunk size of 2^n preferably
            msg += chunk
            if (len(chunk) and chunk[-2:] == self.delimiter):
                break
        return msg[:-2]

    def tx_txt(self, msg):
        """Send text string ending and append delimiter."""
        return self._socket.send((msg + self.delimiter).encode('utf-8'))

    def txrx_txt(self, msg):
        """Send/receive text string."""
        self.tx_txt(msg)
        return self.rx_txt()

    def set_output_state(self, num_out, state):
        """Disable or enable fast analog outputs.

        :state: True to enable fast analog outputs, False to disable fast analog outputs
        """
        return self.tx_txt('OUTPUT{}:STATE {}'.format(num_out, int(state)))

    def get_output_state(self, num_out):
        """Return whether fast analog outputs are enabled or disabled

        :returns: True if fast analog outputs are enabled, False if fast analog outputs are disabled
        """
        response = self.txrx_txt('OUTPUT{}:STATE?'.format(num_out))
        test = (response == "ON")
        return bool(test)

    def set_generator_frequency(self, num_out, frequency):
        """Set the frequency of fast analog outputs

        :frequency: the frequency to set in Hz
        """
        return self.tx_txt('SOUR{}:FREQ:FIX {}'.format(num_out, frequency))

    def get_generator_frequency(self, num_out):
        """Return the frequency of fast analog outputs

        :returns: the frequency in Hz
        """
        return float(self.txrx_txt('SOUR{}:FREQ:FIX?'.format(num_out)))

    def set_generator_waveform(self, num_out, form):
        """Set the waveform of fast analog outputs

        :form: Form to set (SINE, SQUARE, TRIANGLE, SAWU, SAWD, PWM, ARBITRARY)
        """
        return self.tx_txt('SOUR{}:FUNC {}'.format(num_out, form))

    def get_generator_waveform(self, num_out):
        """Return the waveform of fast analog outputs

        :returns: the waveform of fast analog outputs
        """
        return self.txrx_txt('SOUR{}:FUNC?'.format(num_out))

    def set_generator_amplitude(self, num_out, amplitude):
        """Set the amplitude voltage of fast analog outputs.
        Amplitude + offset value must be less than maximum output range ± 1V

        :amplitude: the amplitude to set in V
        """
        return self.tx_txt('SOUR{}:VOLT {}'.format(num_out, amplitude))

    def get_generator_amplitude(self, num_out):
        """Return the amplitude voltage of fast analog outputs.

        :returns: the amplitude voltage in V
        """
        return float(self.txrx_txt('SOUR{}:VOLT?'.format(num_out)))

    def set_generator_offset(self, num_out, offset):
        """Set the offset voltage of fast analog outputs.
        Amplitude + offset value must be less than maximum output range ± 1V

        :offset: the offset voltage to set in V
        """
        return self.tx_txt('SOUR{}:VOLT:OFFS {}'.format(num_out, offset))

    def get_generator_offset(self, num_out):
        """Return the offset voltage of fast analog outputs.

        :returns: the offset voltage in V
        """
        return float(self.txrx_txt('SOUR{}:VOLT:OFFS?'.format(num_out)))

    def set_setpoint(self, num_in, num_out, value):
        """Set the PID setpoint

        :value: the value to set in V
        """
        return self.tx_txt('PID:IN{}:OUT{}:SETPoint {}'.format(num_in, num_out, value))

    def get_setpoint(self, num_in, num_out):
        """Return the PID setpoint

        :returns: the setpoint in V
        """
        return float(self.txrx_txt('PID:IN{}:OUT{}:SETPoint?'.format(num_in, num_out)))

    def set_kp(self, num_in, num_out, gain):
        """Set the P gain

        :gain: the gain to set (0 to 4096)
        """
        return self.tx_txt('PID:IN{}:OUT{}:KP {}'.format(num_in, num_out, gain))

    def get_kp(self, num_in, num_out):
        """Return the P gain

        :returns: the P gain
        """
        return float(self.txrx_txt('PID:IN{}:OUT{}:KP?'.format(num_in, num_out)))

    def set_ki(self, num_in, num_out, gain):
        """Set the I gain

        :gain: the gain to set in 1/s. The unity gain frequency is ki/(2 pi)."""
        return self.tx_txt('PID:IN{}:OUT{}:KI {}'.format(num_in, num_out, gain))

    def get_ki(self, num_in, num_out):
        """Return the I gain

        :returns: the I gain in 1/s. The unity gain frequency is ki/(2 pi)."""
        return float(self.txrx_txt('PID:IN{}:OUT{}:KI?'.format(num_in, num_out)))

    def set_kd(self, num_in, num_out, gain):
        """Set the D gain

        :gain: the gain to set
        """
        return self.tx_txt('PID:IN{}:OUT{}:KD {}'.format(num_in, num_out, gain))

    def get_kd(self, num_in, num_out):
        """Return the D gain

        :returns: the D gain
        """
        return float(self.txrx_txt('PID:IN{}:OUT{}:KD?'.format(num_in, num_out)))

    def set_int_reset_state(self, num_in, num_out, state):
        """Reset the integrator register

        :state: True to enable the integrator reset, False to disable the integrator reset
        """
        return self.tx_txt('PID:IN{}:OUT{}:INT:RES {}'.format(num_in, num_out, int(state)))

    def get_int_reset_state(self, num_in, num_out):
        """Return whether the integrator reset is enabled or disabled

        :returns: True if the integrator reset is enabled, False if the integrator reset is disabled
        """
        response = self.txrx_txt('PID:IN{}:OUT{}:INT:RES?'.format(num_in, num_out))
        test = (response == "ON")
        return bool(test)

    def set_int_hold_state(self, num_in, num_out, state):
        """Hold the status of the integrator register

        :state: True to enable the integrator hold, False to disable the integrator hold
        """
        return self.tx_txt('PID:IN{}:OUT{}:INT:HOLD {}'.format(num_in, num_out, int(state)))

    def get_int_hold_state(self, num_in, num_out):
        """Return whether the integrator hold is enabled or disabled

        :returns: True if the integrator hold is enabled, False if the integrator hold is disabled
        """
        response = self.txrx_txt('PID:IN{}:OUT{}:INT:HOLD?'.format(num_in, num_out))
        test = (response == "ON")
        return bool(test)

    def set_int_auto_state(self, num_in, num_out, state):
        """If enabled, the integrator register is reset when the PID output hits the configured
        limit

        :state: True to enable the automatic integrator reset, False to disable the automatic
                integrator reset
        """
        return self.tx_txt('PID:IN{}:OUT{}:INT:AUTO {}'.format(num_in, num_out, int(state)))

    def get_int_auto_state(self, num_in, num_out):
        """Return whether the automatic integrator reset is enabled or disabled

        :returns: True if the automatic integrator reset is enabled, False if the automatic
                  integrator reset is disabled
        """
        response = self.txrx_txt('PID:IN{}:OUT{}:INT:AUTO?'.format(num_in, num_out))
        test = (response == "ON")
        return bool(test)

    def set_inv_state(self, num_in, num_out, state):
        """Invert the sign of the PID output

        :state: True to enable the inversion, False to disable the inversion
        """
        return self.tx_txt('PID:IN{}:OUT{}:INV {}'.format(num_in, num_out, int(state)))

    def get_inv_state(self, num_in, num_out):
        """Return whether the sign of the PID output is inverted or not

        :returns: True if the inversion is enabled, False if the inversion is disabled
        """
        response = self.txrx_txt('PID:IN{}:OUT{}:INV?'.format(num_in, num_out))
        test = (response == "ON")
        return bool(test)

    def set_relock_state(self, num_in, num_out, state):
        """Enable or disable the PID relock feature. If enabled, the input not used by the PID is
        monitored. If the value falls outside the configured minimum and maximum values, the
        integrator is frozen and the output is ramped with the specified slew rate in order to
        re-acquire the lock. Once the value is inside the bounds, the integrator is turned on
        again.

        :state: True to enable the relock feature, False to disable the relock feature
        """
        return self.tx_txt('PID:IN{}:OUT{}:REL {}'.format(num_in, num_out, int(state)))

    def get_relock_state(self, num_in, num_out):
        """Return whether the PID relock feature is enabled or disabled

        :returns: True if the relock feature is enabled, False if the relock feature is disabled
        """
        response = self.tx_txt('PID:IN{}:OUT{}:REL?'.format(num_in, num_out))
        test = (response == "ON")
        return bool(test)

    def set_relock_stepsize(self, num_in, num_out, stepsize):
        """Set the step size (slew rate) of the relock

        :stepsize: the stepsize to set in V/s
        """
        return self.tx_txt('PID:IN{}:OUT{}:REL:STEP {}'.format(num_in, num_out, stepsize))

    def get_relock_stepsize(self, num_in, num_out):
        """Return the step size (slew rate) of the relock

        :returns: the stepsize in V/s
        """
        return float(self.txrx_txt('PID:IN{}:OUT{}:REL:STEP?'.format(num_in, num_out)))

    def set_relock_minimum(self, num_in, num_out, minimum):
        """Set the minimum input voltage for which the PID is considered locked

        :minimum: the minimum input voltage to set
        """
        return self.tx_txt('PID:IN{}:OUT{}:REL:MIN {}'.format(num_in, num_out, minimum))

    def get_relock_minimum(self, num_in, num_out):
        """Return the minimum input voltage for which the PID is considered locked

        :returns: the minimum input voltage
        """
        return float(self.txrx_txt('PID:IN{}:OUT{}:REL:MIN?'.format(num_in, num_out)))

    def set_relock_maximum(self, num_in, num_out, maximum):
        """Set the maximum input voltage for which the PID is considered locked

        :maximum: the maximum input voltage to set
        """
        return self.tx_txt('PID:IN{}:OUT{}:REL:MAX {}'.format(num_in, num_out, maximum))

    def get_relock_maximum(self, num_in, num_out):
        """Return the maximum input voltage for which the PID is considered locked

        :returns: the maximum input voltage
        """
        return float(self.txrx_txt('PID:IN{}:OUT{}:REL:MAX?'.format(num_in, num_out)))

    def set_output_minimum(self, num_out, minimum):
        """Set the minimum output voltage for the specified channel.

        :num_out: the output channel (1 or 2)
        :minimum: the minimum voltage in V
        """
        self.tx_txt("OUT{}:LIM:MIN {}".format(num_out, minimum))

    def get_output_minimum(self, num_out):
        """Get the minimum output voltage for the specified channel.

        :num_out: the output channel (1 or 2)
        :returns: the minimum output voltage
        """
        return float(self.txrx_txt("OUT{}:LIM:MIN?".format(num_out)))

    def set_output_maximum(self, num_out, maximum):
        """Set the maximum output voltage for the specified channel.

        :num_out: the output channel (1 or 2)
        :maximum: the maximum voltage in V
        """
        self.tx_txt("OUT{}:LIM:MAX {}".format(num_out, maximum))

    def get_output_maximum(self, num_out):
        """Get the maximum output voltage for the specified channel.

        :num_out: the output channel (1 or 2)
        :returns: the maximum output voltage
        """
        return float(self.txrx_txt("OUT{}:LIM:MAX?".format(num_out)))

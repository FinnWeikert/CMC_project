
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
import os
import numpy as np
import farms_pylog as pylog


# How to do it: change Wave_controller so in pars it check for controller type "sin" "square_sig" or "square_arctan"
def exercise2():

    pylog.info("Ex 2")
    pylog.info("Implement exercise 2")
    log_path = './logs/exercise2/'
    os.makedirs(log_path, exist_ok=True)


if __name__ == '__main__':
    exercise2()

############## sigmoid gain functions ##############

def sigmoid(x, a):
    return 1 / (1 + np.exp(-a * x))

def sin_square_wave(input_signal, gain):
    # Apply sigmoidal function
    sigmoid_output = sigmoid(input_signal, gain)
    # Scale and shift the output to range [-1, 1]
    output_signal = 2 * sigmoid_output - 1
    return output_signal

############## arctan gain functions ##############

def arctan_gain(x, gain):
    return np.arctan(gain * x) / np.pi # Normalize to range [0, 1]

def arcta_square_wave(input_signal, gain):
    # Apply arctan gain function
    output_signal = arctan_gain(input_signal, gain)
    # Scale the output to range [-1, 1]
    output_signal = 2 * output_signal - 1
    return output_signal
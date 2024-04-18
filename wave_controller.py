"""Network controller"""

import numpy as np
import farms_pylog as pylog


class WaveController:

    """Test controller"""

    def __init__(self, pars):
        self.pars = pars
        self.timestep = pars.timestep
        self.times = np.linspace(
            0,
            pars.n_iterations *
            pars.timestep,
            pars.n_iterations)
        self.n_joints = pars.n_joints

        # state array for recording all the variables
        self.state = np.zeros((pars.n_iterations, 2*self.n_joints))

        # indexes of the left muscle activations (optional)
        self.muscle_l = 2*np.arange(15)
        # indexes of the right muscle activations (optional)
        self.muscle_r = self.muscle_l+1

        # added
        self.square_controller = pars.square_controller

    def step(self, iteration, time, timestep, pos=None):
        """
        Step function. This function passes the activation functions of the muscle model
        Inputs:
        - iteration - iteration index
        - time - time vector
        - timestep - integration timestep
        - pos (not used) - joint angle positions

        Implement here the control step function,
        it should return an array of 2*n_joint=30 elements,
        even indexes (0,2,4,...) = left muscle activations
        odd indexes (1,3,5,...) = right muscle activations

        In addition to returning the activation functions, store
        them in self.state for later use offline
        """

        # Changed this may not be the optimal place to do so
        # Ask about this: ipls = wavefreq / freq
        # clarify what wave freq and ipls is?

        A = self.pars.amp if hasattr(self.pars, 'amp') else 0.48        
        eps = self.pars.wavefrequency if hasattr(self.pars, 'wavefrequency') else 0.48
        freq = self.pars.frequency if hasattr(self.pars, 'frequency') else 2.5

        activations = np.zeros(30)
        i = np.arange(self.n_joints)

        sin_signal = np.sin(2 * np.pi * (freq * time - eps * i / self.n_joints))
                      
        if self.square_controller == None:
            activations[self.muscle_l] = 0.5 * A / 2 * np.sin(2 * np.pi * (freq * time - eps * i / self.n_joints))
            activations[self.muscle_r] = 0.5 * (-A) / 2 * np.sin(2 * np.pi * (freq * time - eps * i / self.n_joints))
            # Proj 1 part 3 gain functions
        elif self.square_controller == "sigmoid":
            activations[self.muscle_l] = 0.5 * A / 2 * sigmoid_gain(sin_signal, gain=5)
            activations[self.muscle_r] = 0.5 * (-A) / 2 * sigmoid_gain(sin_signal, gain=5)
        elif self.square_controller == "arctan":
            activations[self.muscle_l] = 0.5 * A / 2 * arctan_gain(sin_signal, gain=5)
            activations[self.muscle_r] = 0.5 * (-A) / 2 * arctan_gain(sin_signal, gain=5)
        else:
            raise ValueError("Invalid controller type. Supported types are 'sine', 'square_sig', and 'square_arctan'.")

        self.state[iteration] = activations

        return activations

# Move these function somewhere else later ?
############## sigmoid gain functions ##############

def sigmoid_gain(input_signal, gain):
    # Scale and shift the output to range [-1, 1]
    return 2 * (1 / (1 + np.exp(-gain * input_signal))) - 1

############## arctan gain functions ##############

def arctan_gain(input_signal, gain):
    return 2/np.pi * np.arctan(gain * input_signal) # scale to range [-1, 1]
    

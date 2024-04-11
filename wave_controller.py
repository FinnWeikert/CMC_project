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

        pylog.warning(
            "Implement below the step function following the instructions here and in the report")

        # indexes of the left muscle activations (optional)
        self.muscle_l = 2*np.arange(15)
        # indexes of the right muscle activations (optional)
        self.muscle_r = self.muscle_l+1

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

        A = 0.8
        eps = 1
        freq = 4

        activations = np.zeros(30)
        i = np.arange(self.n_joints)

        activations[self.muscle_l] = 0.5 * A / 2 * np.sin(2 * np.pi * (freq * time - eps * i / self.n_joints))
        activations[self.muscle_r] = 0.5 * (-A) / 2 * np.sin(2 * np.pi * (freq * time - eps * i / self.n_joints))

        self.state[iteration] = activations

        return activations

#  where to add the paramters A, eps ,and freq   QUESTION
# "It also contains the metrics dictionary ???"  QUESTION
#  should the differential equation be implemented here??  QUESTION
    

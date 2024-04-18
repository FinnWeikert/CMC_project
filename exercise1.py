
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import numpy as np
import farms_pylog as pylog
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows

def exercise1(**kwargs):

    pylog.info("Ex 1")
    pylog.info("Implement exercise 1")
    log_path = './logs/exercise1/'
    os.makedirs(log_path, exist_ok=True)


    nsim = 2
    # Lists to store amplitudes and wave frequencies per sim
    amps = []
    wave_freqs = []

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    pars_list = [
        SimulationParameters(
            simulation_i=i*nsim+j,
            n_iterations=3001,
            log_path=log_path,
            video_record=False,
            compute_metrics=3, # changed
            amp=amp,
            wavefrequency=wavefrequency,
            headless=True,
            print_metrics=False,
            return_network=True # added
        )
        for i, amp in enumerate(np.linspace(0.05, 1, nsim))
        for j, wavefrequency in enumerate(np.linspace(0., 0.1, nsim))
        for _ in (amps.append(amp), wave_freqs.append(wavefrequency))
    ][::2] # remove every second because the line above makes doubles the params otherwise


    controllers = run_multiple(pars_list, num_process=4)
    d = 1 # debug

    speed_metric_dict = {
        "max_fspeed_PCA": [0, None, None, None], # [speed, opti_amp, opti_wavefreq, sim_index]
        "max_lspeed_PCA": [0, None, None, None],
        "max_fspeed_cycle": [0, None, None, None],
        "max_lspeed_cycle": [0, None, None, None]
    }

    # parameter search for highest amp and wavefrequency with highest speed
    for controller in controllers:

        # fspeed PCA
        if np.abs(controller.metrics['fspeed_PCA']) > speed_metric_dict["max_fspeed_PCA"][0]:
            speed_metric_dict["max_fspeed_PCA"][0] = controller.metrics['fspeed_PCA'] # update fspeed
            speed_metric_dict["max_fspeed_PCA"][1] = amps[controller.pars.simulation_i] # update opti amp
            speed_metric_dict["max_fspeed_PCA"][2] = wave_freqs[controller.pars.simulation_i] # update opti wavefreq
            speed_metric_dict["max_fspeed_PCA"][3] = controller.pars.simulation_i # update simulaiton inde

        # lspeed PCA (probably not needed)
        if np.abs(controller.metrics['lspeed_PCA']) > speed_metric_dict["max_lspeed_PCA"][0]:
            speed_metric_dict["max_lspeed_PCA"][0] = controller.metrics['lspeed_PCA'] # update lspeed
            speed_metric_dict["max_lspeed_PCA"][1] = amps[controller.pars.simulation_i]
            speed_metric_dict["max_lspeed_PCA"][2] = wave_freqs[controller.pars.simulation_i]
            speed_metric_dict["max_lspeed_PCA"][3] = controller.pars.simulation_i

        # fspeed cycle
        if np.abs(controller.metrics['fspeed_cycle']) > speed_metric_dict["max_fspeed_cycle"][0]:
            speed_metric_dict["max_fspeed_cycle"][0] = controller.metrics['fspeed_cycle']
            speed_metric_dict["max_fspeed_cycle"][1] = amps[controller.pars.simulation_i]
            speed_metric_dict["max_fspeed_cycle"][2] = wave_freqs[controller.pars.simulation_i]
            speed_metric_dict["max_fspeed_cycle"][3] = controller.pars.simulation_i 

        # lspeed cycle (probalby not needed)
        if np.abs(controller.metrics['lspeed_cycle']) > speed_metric_dict["max_lspeed_cycle"][0]:
            speed_metric_dict["max_lspeed_cycle"][0] = controller.metrics['lspeed_cycle']
            speed_metric_dict["max_lspeed_cycle"][1] = amps[controller.pars.simulation_i]
            speed_metric_dict["max_lspeed_cycle"][2] = wave_freqs[controller.pars.simulation_i]
            speed_metric_dict["max_lspeed_cycle"][3] = controller.pars.simulation_i    
        
    d = 1 # debug

    # TO DO: Keep track of all the speed values, so plots can be made where the optimum is clearly visible => see plot_2d
    # maybe look for library that does 2d grid search faster?

    # should we consider any other metrics than the speed?

    # goal code parameter search for largest speed 
if __name__ == '__main__':
    exercise1()


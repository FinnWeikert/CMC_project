
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
from util.rw import load_object
import os
import numpy as np
import farms_pylog as pylog
from plotting_common import plot_2d

def exercise1(**kwargs):

    pylog.info("Ex 1")
    pylog.info("Implement exercise 1")
    log_path = './logs/exercise1/'
    os.makedirs(log_path, exist_ok=True)


    nsim = 10
    # Lists to store amplitudes and wave frequencies per sim
    amps = []
    wave_freqs = []

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    pars_list = [
        SimulationParameters(
            simulation_i=i*nsim+j,
            n_iterations=3001, # maybe this should be a bit larger to make sure intitial cond effect vanish
            log_path=log_path,
            video_record=False,
            compute_metrics=3, # changed
            amp=amp,
            wavefrequency=wavefrequency,
            headless=True,
            print_metrics=False,
            return_network=True # added
        )
        for i, amp in enumerate(np.linspace(0.05, 2, nsim))
        for j, wavefrequency in enumerate(np.linspace(0.05, 2, nsim))
        for _ in (amps.append(amp), wave_freqs.append(wavefrequency))
    ][::2] # remove every second because the line above makes doubles the params otherwise

    # check if this aprameter search was run before if so acces log
    log_controlers = os.listdir("logs/exercise1/")
    # Count the number of files
    num_files = len(log_controlers)

    # if not corresponding number of simulations stored in logs, run the simulations
    if num_files != nsim**2:
        controllers = run_multiple(pars_list, num_process=16)
    else: # load the simulations from logs
        controllers = []
        for i in range(nsim**2):
            controllers.append(load_object("logs/exercise1/controller"+str(i)))
    d = 1 # debug

    # dict to store opti params
    speed_metric_dict = {
        "max_fspeed_PCA": [0, None, None, None], # [speed, opti_amp, opti_wavefreq, sim_index]
        "max_lspeed_PCA": [0, None, None, None],
        "max_fspeed_cycle": [0, None, None, None],
        "max_lspeed_cycle": [0, None, None, None]
    }

    # 2d array of dimension [N, 3], N = number of controllers
    # first col: amps, second: wavefreq, and last: speed
    para_search_results_PCA = np.zeros((len(controllers), 3))
    para_search_results_cycle = np.zeros((len(controllers), 3))

    # parameter search for highest amp and wavefrequency with highest speed
    for i, controller in enumerate(controllers):

        # extract metrics for current controller
        amp = amps[controller.pars.simulation_i]
        wave_freq = wave_freqs[controller.pars.simulation_i]
        fspeed_PCA = controller.metrics['fspeed_PCA']
        fspeed_cycle = controller.metrics['fspeed_cycle']

        # store the parameters and corresponding speed in results array
        para_search_results_PCA[i][0] = amp
        para_search_results_PCA[i][1] = wave_freq
        para_search_results_PCA[i][2] = fspeed_PCA

        para_search_results_cycle[i][0] = amp
        para_search_results_cycle[i][1] = wave_freq
        para_search_results_cycle[i][2] = fspeed_cycle

        # fspeed PCA
        if np.abs(fspeed_PCA) > speed_metric_dict["max_fspeed_PCA"][0]:
            speed_metric_dict["max_fspeed_PCA"][0] = fspeed_PCA # update fspeed
            speed_metric_dict["max_fspeed_PCA"][1] = amp # update opti amp
            speed_metric_dict["max_fspeed_PCA"][2] = wave_freq # update opti wavefreq
            speed_metric_dict["max_fspeed_PCA"][3] = controller.pars.simulation_i # update simulaiton inde

        # fspeed cycle
        if np.abs(fspeed_cycle) > speed_metric_dict["max_fspeed_cycle"][0]:
            speed_metric_dict["max_fspeed_cycle"][0] = fspeed_cycle
            speed_metric_dict["max_fspeed_cycle"][1] = amp
            speed_metric_dict["max_fspeed_cycle"][2] = wave_freq
            speed_metric_dict["max_fspeed_cycle"][3] = controller.pars.simulation_i 

        """# lspeed PCA (probably not needed)
        if np.abs(controller.metrics['lspeed_PCA']) > speed_metric_dict["max_lspeed_PCA"][0]:
            speed_metric_dict["max_lspeed_PCA"][0] = controller.metrics['lspeed_PCA'] # update lspeed
            speed_metric_dict["max_lspeed_PCA"][1] = amp
            speed_metric_dict["max_lspeed_PCA"][2] = wave_freq
            speed_metric_dict["max_lspeed_PCA"][3] = controller.pars.simulation_i

        # lspeed cycle (probalby not needed)
        if np.abs(controller.metrics['lspeed_cycle']) > speed_metric_dict["max_lspeed_cycle"][0]:
            speed_metric_dict["max_lspeed_cycle"][0] = controller.metrics['lspeed_cycle']
            speed_metric_dict["max_lspeed_cycle"][1] = amp
            speed_metric_dict["max_lspeed_cycle"][2] = wave_freq
            speed_metric_dict["max_lspeed_cycle"][3] = controller.pars.simulation_i""" 
        
    d = 1 # debug

    print("Results of the 2D parameter search for combinations of", str(nsim),
           "amplitudes and wavefrequencies in [0.05, 2]") 
    print("Optimal Amplitude of: ", round(speed_metric_dict["max_fspeed_PCA"][1], 3), 
          "and wavefrequency of: ", round(speed_metric_dict["max_fspeed_PCA"][2], 3),
          "gives PCA Fspeed: ", round(speed_metric_dict["max_fspeed_PCA"][0], 5))
    print("Optimal Amplitude of: ", round(speed_metric_dict["max_fspeed_cycle"][1], 3), 
          "and wavefrequency of: ", round(speed_metric_dict["max_fspeed_cycle"][2], 3),
          "gives cycle Fspeed: ", round(speed_metric_dict["max_fspeed_cycle"][0], 5))

    ### THE PLOTTING COULD ALSO BE MOVED (see test_file.py plots using plot_results fun)

    # Plot the heat map of the parameter search (uisng plot2d)
    labels = ['Amplitude [Hz]', 'Wave frequency [Hz]', 'Forward speed [m/s]']

    plt.figure('2D Parameter Search PCA Fspeed', figsize=[10, 10])
    plot_2d(para_search_results_PCA, labels) # to change to nicest color map
    plt.title('2D Parameter Search PCA Fspeed')
    plt.show()

    plt.figure('2D Parameter Search cycle Fspeed', figsize=[10, 10])
    plot_2d(para_search_results_cycle, labels, cmap='nipy_spectral')
    plt.title('2D Parameter Search cycle Fspeed')
    plt.show()

    d = 1 # debug

if __name__ == '__main__':
    exercise1()


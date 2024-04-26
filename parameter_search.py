import numpy as np
import matplotlib.pyplot as plt
from plotting_common import plot_2d

def param_search(controllers, amps, wave_freqs, 
                 plot_results=True, cmap='nipy_spectral'):
    """
    Perform parameter optimization of amplitude and wavefrequency 
    for forward speed and optionally plot the results.

    Args:
        controllers (list): A list of controllers.
        amps (list): A list of amplitudes.
        wave_freqs (list): A list of wavefrequencies.
        plot_results (bool, optional): Whether to plot the results. Defaults to True.
        cmap (string, optional): Defines what heatmap to use for plotting 

    Returns:
        None
    """

    # dict to store opti params
    speed_metric_dict = {
        "max_fspeed_PCA": [0, None, None, None],  # [speed, opti_amp, opti_wavefreq, sim_index]
        "max_fspeed_cycle": [0, None, None, None],
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
            speed_metric_dict["max_fspeed_PCA"][0] = fspeed_PCA  # update fspeed
            speed_metric_dict["max_fspeed_PCA"][1] = amp  # update opti amp
            speed_metric_dict["max_fspeed_PCA"][2] = wave_freq  # update opti wavefreq
            speed_metric_dict["max_fspeed_PCA"][3] = controller.pars.simulation_i  # update simulation index

        # fspeed cycle
        if np.abs(fspeed_cycle) > speed_metric_dict["max_fspeed_cycle"][0]:
            speed_metric_dict["max_fspeed_cycle"][0] = fspeed_cycle
            speed_metric_dict["max_fspeed_cycle"][1] = amp
            speed_metric_dict["max_fspeed_cycle"][2] = wave_freq
            speed_metric_dict["max_fspeed_cycle"][3] = controller.pars.simulation_i

    # Print debug info
    d = 1  # debug

    nsim=np.sqrt(len(controllers))
    # Print results
    print("Results of the 2D parameter search for combinations of", str(nsim),
          "amplitudes and wavefrequencies in [0.05, 2]")
    print("Optimal Amplitude of: ", round(speed_metric_dict["max_fspeed_PCA"][1], 3),
          "and wavefrequency of: ", round(speed_metric_dict["max_fspeed_PCA"][2], 3),
          "gives PCA Fspeed: ", round(speed_metric_dict["max_fspeed_PCA"][0], 5))
    print("Optimal Amplitude of: ", round(speed_metric_dict["max_fspeed_cycle"][1], 3),
          "and wavefrequency of: ", round(speed_metric_dict["max_fspeed_cycle"][2], 3),
          "gives cycle Fspeed: ", round(speed_metric_dict["max_fspeed_cycle"][0], 5))

    # Plot the results if required
    if plot_results:
        # Plot the heat map of the parameter search (using plot2d)
        labels = ['Amplitude', 'Wave frequency [Hz]', 'Forward speed']

        plt.figure('2D Parameter Search PCA Fspeed', figsize=[10, 10])
        plot_2d(para_search_results_PCA, labels, cmap=cmap)  # to change to nicest color map
        plt.title('2D Parameter Search PCA Fspeed')
        plt.show()

        plt.figure('2D Parameter Search cycle Fspeed', figsize=[10, 10])
        plot_2d(para_search_results_cycle, labels, cmap=cmap)
        plt.title('2D Parameter Search cycle Fspeed')
        plt.show()


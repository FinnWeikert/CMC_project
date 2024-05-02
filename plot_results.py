"""Plot results"""

import farms_pylog as pylog
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from util.rw import load_object
from plotting_common import plot_2d, save_figures, plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows
import numpy as np
import matplotlib
import os
matplotlib.rc('font', **{"size": 20})


def plot_speed_param_search(n_simulations, logdir, speed_metric="fspeed_PCA"):
    """
    This function can also be used for the parameter search heat map plotting
    """
    pylog.info(
        "Example showing how to load the simulation file and use the plot2d function")
    fspeeds = np.zeros([n_simulations, 3])
    for i in range(n_simulations):
        # load controller
        controller = load_object(logdir+"controller"+str(i))
        fspeeds[i] = [
            controller.pars.amp,
            controller.pars.wavefrequency,
            np.mean(controller.metrics[speed_metric])
        ]

    plt.figure('2D Parameter Search '+speed_metric, figsize=[10, 10])
    plot_2d(
        fspeeds,
        ['Amp', 'wavefrequency', 'Forward Speed [m/s]'],
        cmap='nipy_spectral'
    )

def plot_metric_for_steepness(steepness_list, metrics_dict, ylabel='Speed',speed=True, torque=False):
    """
    Plot multiple metrics as a function of steepness.

    Parameters:
        steepness_list (list): A list of steepness values.
        metrics_dict (dict): A dictionary where keys are labels for different curves, and values are lists of metric values.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    if speed: plt.axhline(y=0.0325, color='r', linestyle='--', label='Sinusoid fspeed')  # Add horizontal line at y=0.033
    if torque: plt.axhline(y=0.00590, color='g', linestyle='--', label='Sinusoid torque')  # Add horizontal line at y=0.01154
    
    for label, metric_list in metrics_dict.items():
        plt.plot(steepness_list, metric_list, label=label, linewidth=2)
    
    plt.xlabel('Steepness')
    plt.ylabel(ylabel)
    plt.title(ylabel+' as function of Steepness')
    plt.legend(fontsize=10)  # Adjust legend size
    plt.grid(True)
    plt.show()

    
def main(plot=True):
    """Main"""

    pylog.info(
        "Here is an example to show how you can load a single simulation and which data you can load")
    controller = load_object("logs/example_single/controller0")

    # neural data
    state = controller.state
    metrics = controller.metrics

    # mechanical data
    links_positions = controller.links_positions  # the link positions
    links_velocities = controller.links_velocities  # the link velocities
    joints_active_torques = controller.joints_active_torques  # the joint active torques
    joints_velocities = controller.joints_velocities  # the joint velocities
    joints_positions = controller.joints_positions  # the joint positions


if __name__ == '__main__':
    main(plot=True)


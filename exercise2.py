
from util.run_closed_loop import run_multiple, run_single
from simulation_parameters import SimulationParameters
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows
from util.rw import load_object
import os
import numpy as np
import farms_pylog as pylog
from parameter_search import param_search
import matplotlib.pyplot as plt


# global parameters to defines what to run
SINGLE_SIM = False
PARAM_SEARCH = True

# Note: changes mostly made in wave_controller not here
def exercise2(**kwargs):

    pylog.info("Ex 2")
    pylog.info("Implement exercise 2")
    log_path = './logs/exercise2/'
    os.makedirs(log_path, exist_ok=True)

    if SINGLE_SIM:
        all_pars = SimulationParameters(
            n_iterations=3001,
            controller="sine",
            square_controller="sigmoid", # added
            log_path=log_path,
            compute_metrics=3,
            return_network=True,
            wavefrequency=1,
            amp=0.5, # added
            **kwargs
        )

        pylog.info("Running the simulation")
        controller = run_single(
            all_pars
        )

        pylog.info("Plotting the result")

        left_idx = controller.muscle_l
        right_idx = controller.muscle_r

        # plot using plot_left_right
        plot_left_right(
            controller.times,
            controller.state,
            left_idx,
            right_idx,
            cm="green",
            offset=0.1)

        # plot using plot_trajectory
        plt.figure("trajectory")
        plot_trajectory(controller)

        # plot using plot_time_histories_multiple_windows
        plt.figure("joint positions")
        plot_time_histories_multiple_windows(
            controller.times,
            controller.joints_positions,
            offset=-0.4,
            colors="green",
            ylabel="joint positions",
            lw=1
        )

        # plot using plot_time_histories
        plt.figure("link y-velocities")
        plot_time_histories(
            controller.times,
            controller.links_velocities[:, :, 1],
            offset=-0.,
            colors="green",
            ylabel="link y-velocities",
            lw=1
        )

    if PARAM_SEARCH:
        nsim = 1
        # Lists to store amplitudes and wave frequencies per sim
        amps = []
        wave_freqs = []

        pylog.info(
            "Running multiple simulations in parallel from a list of SimulationParameters")
        pars_list = [
            SimulationParameters(
                simulation_i=i*nsim+j,
                n_iterations=4001, # maybe this should be a bit larger to make sure intitial cond effect vanish
                square_controller=None, # added
                gain_steepness=5,
                log_path=log_path,
                video_record=False,
                compute_metrics=3, # changed
                amp=amp,
                wavefrequency=wavefrequency,
                freq = 1.5,
                headless=True,
                print_metrics=False,
                return_network=True # added
            )
            for i, amp in enumerate(np.linspace(0.05, 2, nsim))
            for j, wavefrequency in enumerate(np.linspace(0.05, 2, nsim))
            for _ in (amps.append(amp), wave_freqs.append(wavefrequency))
        ][::2] # remove every second because the line above makes doubles the params otherwise

        # check if this aprameter search was run before if so acces log
        log_controlers = os.listdir("logs/exercise2/")
        # Count the number of file
        num_files = len(log_controlers)

        # if not corresponding number of simulations stored in logs, run the simulations
        if num_files != nsim**2:
            controllers = run_multiple(pars_list, num_process=8)
        else: # load the simulations from logs
            controllers = []
            for i in range(nsim**2):
                controllers.append(load_object("logs/exercise2/controller"+str(i)))
        d = 1 # debug

    # perform the parameter search
    param_search(controllers, amps, wave_freqs, nsim)



if __name__ == '__main__':
    exercise2(headless=False)
    plt.show()

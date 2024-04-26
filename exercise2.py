
from util.run_closed_loop import run_multiple, run_single
from simulation_parameters import SimulationParameters
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows
from plot_results import plot_metric_for_steepness
from util.rw import load_object
import os
import numpy as np
import farms_pylog as pylog
from parameter_search import param_search
import matplotlib.pyplot as plt

# WHAT to plot?
# show that the actiations are square waves,
# plot the fspeed as a function of steepness
# plot the torque consumption as a function of steepness

# global parameters to defines what to run
SINGLE_SIM = False
PARAM_SEARCH = True
STEEPNESS = False

# Note: changes mostly made in wave_controller not here
def exercise2():

    pylog.info("Ex 2")
    pylog.info("Implement exercise 2")

    if SINGLE_SIM:
        log_path = './logs/exercise2/single/'
        os.makedirs(log_path, exist_ok=True)

        all_pars = SimulationParameters(
            n_iterations=10001,
            controller="sine",
            square_controller="sigmoid", # added
            gain_steepness=20,
            log_path=log_path,
            compute_metrics=3,
            return_network=True,
            headless=True # change if want to see sim
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

##############################################################################################################
        
    if PARAM_SEARCH:
        log_path = './logs/exercise2/para_search/'
        os.makedirs(log_path, exist_ok=True)
    
        nsim = 7
        # Lists to store amplitudes and wave frequencies per sim
        amps = []
        wave_freqs = []

        pylog.info(
            "Running multiple simulations in parallel from a list of SimulationParameters")
        pars_list = [
            SimulationParameters(
                simulation_i=i*nsim+j,
                n_iterations=5001, # maybe this should be a bit larger to make sure intitial cond effect vanish
                square_controller="sigmoid", # added
                gain_steepness=10,
                log_path=log_path,
                video_record=False,
                compute_metrics=3, # changed
                amp=amp,
                wavefrequency=wavefrequency,
                freq = 2.5,
                headless=True,
                print_metrics=False,
                return_network=True # added
            )
            for i, amp in enumerate(np.linspace(0.05, 2, nsim))
            for j, wavefrequency in enumerate(np.linspace(0.05, 2, nsim))
            for _ in (amps.append(amp), wave_freqs.append(wavefrequency))
        ][::2] # remove every second because the line above makes doubles the params otherwise

        # check if this aprameter search was run before if so acces log
        log_controlers = os.listdir("logs/exercise2/para_search")
        # Count the number of file
        num_files = len(log_controlers)

        # if not corresponding number of simulations stored in logs, run the simulations
        if num_files != nsim**2:
            controllers = run_multiple(pars_list, num_process=8)
        else: # load the simulations from logs
            controllers = []
            for i in range(nsim**2):
                controllers.append(load_object("logs/exercise2/para_search/controller"+str(i)))
        d = 1 # debug

        # perform the parameter search
        param_search(controllers, amps, wave_freqs, nsim)

        d = 1 # debzg

##############################################################################################################
    if STEEPNESS:

        log_path = './logs/exercise2/steepness/'
        os.makedirs(log_path, exist_ok=True)
    
        nsim = 20  # Number of samples
        base = 2  # Logarithmic base

        steepnesses = np.logspace(np.log2(0.1), np.log2(100), nsim, base=base)
        #steepnesses = np.linspace(0.1, 100, nsim)

        pylog.info(
            "Running multiple simulations in parallel from a list of SimulationParameters")
        pars_list = [
            SimulationParameters(
                simulation_i=i,
                n_iterations=7001, 
                square_controller="sigmoid", # added
                gain_steepness=steepness,
                log_path=log_path,
                video_record=False,
                compute_metrics=3, # changed
                headless=True,
                print_metrics=False,
                return_network=True # added
            )
            for i, steepness in enumerate(steepnesses)
        ]
                # check if this aprameter search was run before if so acces log
        log_controlers = os.listdir("logs/exercise2/steepness")
        # Count the number of file
        num_files = len(log_controlers)

        # if not corresponding number of simulations stored in logs, run the simulations
        if num_files != nsim:
            controllers = run_multiple(pars_list, num_process=8)
        else: # load the simulations from logs
            controllers = []
            for i in range(nsim):
                controllers.append(load_object("logs/exercise2/steepness/controller"+str(i)))

        d = 1 # debug

        fspeed_cycle_list = []
        fspeed_PCA_list = []
        lspeed_cycle_list = []
        lspeed_PCA_list = []
        torques_list = []
        amp_list = []
        #ptcc_list = []

        for i, controller in enumerate(controllers):
            fspeed_cycle_list.append(controller.metrics['fspeed_cycle'])
            fspeed_PCA_list.append(controller.metrics['fspeed_PCA'])
            lspeed_cycle_list.append(controller.metrics['lspeed_cycle'])
            lspeed_PCA_list.append(controller.metrics['lspeed_PCA'])
            torques_list.append(controller.metrics['torque'])
            amp_list.append(controller.metrics['amp'])
            #ptcc_list.append(controller.metrics['ptcc'])

        combined_metrics = {
            'Fspeed PCA': fspeed_PCA_list,
            'Fspeed cycle': fspeed_cycle_list,
            'Lspeed_PCA': lspeed_PCA_list,
            'Lspeed_cycle': lspeed_cycle_list,
            'Total torque': torques_list,
            'Amplitude': amp_list
            #'Ptcc': ptcc_list
        }

        speed_metrics = {
            'Fspeed PCA': fspeed_PCA_list,
            'Fspeed cycle': fspeed_cycle_list,
            'Lspeed_PCA': lspeed_PCA_list,
            'Lspeed_cycle': lspeed_cycle_list
        }

        torque_metric = {
            'Total torque': torques_list,
        }

        amplitude_metric = {
            'Amplitude': amp_list
        }

        plot_metric_for_steepness(steepnesses, speed_metrics)
        plot_metric_for_steepness(steepnesses, torque_metric, ylabel='Torque', speed=False, torque=True)
        plot_metric_for_steepness(steepnesses, amplitude_metric, ylabel='Amplitude', speed=False)

        d = 1

if __name__ == '__main__':
    exercise2()



# plot example waves & head movement + comment on deviation reason
# plot param search ?
# plot Fspeed as function of step
# amplitude as function of step 
# Torque consumption as funciton of step
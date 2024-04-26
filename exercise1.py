
from util.run_closed_loop import run_multiple
from simulation_parameters import SimulationParameters
from util.rw import load_object
import os
import numpy as np
import farms_pylog as pylog
from parameter_search import param_search

def exercise1(**kwargs):

    pylog.info("Ex 1")
    pylog.info("Implement exercise 1")
    log_path = './logs/exercise1/'
    os.makedirs(log_path, exist_ok=True)


    nsim = 6
    # Lists to store amplitudes and wave frequencies per sim
    amps = []
    wave_freqs = []

    pylog.info(
        "Running multiple simulations in parallel from a list of SimulationParameters")
    pars_list = [
        SimulationParameters(
            simulation_i=i*nsim+j,
            n_iterations=10001, # maybe this should be a bit larger to make sure intitial cond effect vanish
            log_path=log_path,
            video_record=False,
            compute_metrics=3, # changed
            amp=amp,
            wavefrequency=wavefrequency,
            frequency=2.5,
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

    # perform the parameter search
    param_search(controllers,amps, wave_freqs, nsim)

    d = 1 # debug

if __name__ == '__main__':
    exercise1()


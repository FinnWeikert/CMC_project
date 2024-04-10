
from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
import farms_pylog as pylog
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows


def exercise0(**kwargs):

    pylog.info("Ex 0")
    pylog.info("Implement exercise 0")
    log_path = './logs/exercise0/'
    os.makedirs(log_path, exist_ok=True)
    
    all_pars = SimulationParameters(
        n_iterations=3001,
        log_path=log_path,
        compute_metrics=3,
        return_network=True,
        **kwargs
    )

    pylog.info("Running la simulation")
    controller = run_single(all_pars)
    left_idx = controller.muscle_l
    right_idx = controller.muscle_r

    plot_left_right(
        controller.times,
        controller.state,
        left_idx,
        right_idx,
        cm="green",
        offset=0.1
    )
    plt.figure("Trajectory")
    plot_trajectory(controller)

if __name__ == '__main__':
    exercise0()
    plt.show()

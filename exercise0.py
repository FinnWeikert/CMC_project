# from util.run_closed_loop import run_multiple
# from simulation_parameters import SimulationParameters
# import os
# import numpy as np
# import farms_pylog as pylog


# def exercise_0_multiple():

#     log_path = './logs/example_multiple/'
#     os.makedirs(log_path, exist_ok=True)

#     nsim = 2

#     pylog.info(
#         "Running multiple simulations in parallel from a list of SimulationParameters")
#     pars_list = [
#         SimulationParameters(
#             simulation_i=i*nsim+j,
#             n_iterations=3001,
#             log_path=log_path,
#             video_record=False,
#             compute_metrics=2,
#             amp=amp,
#             wavefrequency=wavefrequency,
#             headless=True,
#             print_metrics=True
#         )
#         for i, amp in enumerate(np.linspace(1, 3, nsim))
#         for j, wavefrequency in enumerate(np.linspace(1, 3, nsim))
#     ]

#     run_multiple(pars_list, num_process=16)


# if __name__ == '__main__':
#     exercise_0_multiple()



from util.run_closed_loop import run_single
from simulation_parameters import SimulationParameters
import matplotlib.pyplot as plt
import os
from plotting_common import plot_left_right, plot_trajectory, plot_time_histories, plot_time_histories_multiple_windows
import farms_pylog as pylog


def exercise0(**kwargs):

    # declare fixed values of amplitude, frequency, and epsilon
    A = 0.5
    eps = 2
    freq = 2

    pylog.info("Ex 0")
    pylog.info("Implement exercise 0")
    log_path = './logs/exercise0/'
    os.makedirs(log_path, exist_ok=True)

    all_pars = SimulationParameters(
        n_iterations=3001,
        controller="sine",
        log_path=log_path,
        compute_metrics=3,
        return_network=True,
        **kwargs
    )

    pylog.info("Running the simulation")
    controller = run_single(
        all_pars
    )

    ########################################
    #from metrics import sum_torques
    #sum_torques()

    #######################################3

    pylog.info("Plotting the result")

    left_idx = controller.muscle_l
    right_idx = controller.muscle_r

    # plot using plot_left_right
    plt.figure("left right", figsize=(8, 6))
    plot_left_right(
        controller.times,
        controller.state,
        left_idx,
        right_idx,
        cm="green",
        offset=0.1)
    plt.subplots_adjust(left=0.25, bottom=0.2)  # Adjust as needed
    plt.suptitle("Left and right muscle activations")

    # plot using plot_trajectory
    plt.figure("trajectory", figsize=(8, 6))
    plot_trajectory(controller)
    # Adjust the position of the figure within the window
    plt.subplots_adjust(left=0.25, bottom=0.2)  # Adjust as needed
    #add a title
    plt.title("Trajectory")
    

    # # plot using plot_time_histories_multiple_windows
    # plt.figure("joint positions", figsize=(8, 6))
    # plot_time_histories_multiple_windows(
    #     controller.times,
    #     controller.joints_positions,
    #     offset=-0.4,
    #     colors="green",
    #     lw=1
    # )
    # plt.ylabel("joint positions")
    # # Adjust the position of the figure within the window
    # plt.subplots_adjust(left=0.25, bottom=0.2)  # Adjust as needed
    # plt.suptitle("Joint positions")

    plt.figure("joint positions", figsize=(12, 18))  # Increase the figure size to accommodate all subplots
    plot_time_histories_multiple_windows(
        controller.times,
        controller.joints_positions,
        offset=-0.4,
        colors="green",
        lw=1
    )

    # Adjust the spacing between subplots
    plt.subplots_adjust(top=0.95, bottom=0.05, left=0.2, right=0.9, hspace=1, wspace=0.3)
    plt.suptitle("Joint positions")




    # plot using plot_time_histories
    plt.figure("link y-velocities", figsize=(8, 6))
    plot_time_histories(
        controller.times,
        controller.links_velocities[:, :, 1],
        offset=-0.,
        colors="green",
        ylabel="link y-velocities",
        lw=1
    )
    # Adjust the position of the figure within the window
    plt.subplots_adjust(left=0.25, bottom=0.2)  # Adjust as needed
    #add a title
    plt.title("Link y-velocities")


    # # Save each open figure separately
    # for i in range(plt.gcf().number):
    #     plt.figure(i+1)
    #     plt.savefig(f"ex0_figs\\figure_alt_{i+1}.png")  # Save each figure with a unique filename

    




if __name__ == '__main__':
    exercise0(headless=False)
    plt.show()

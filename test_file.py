from plot_results import plot_speed_param_search
import matplotlib.pyplot as plt
import numpy as np

"""plot_speed_param_search(100, "logs/exercise1/", speed_metric="fspeed_PCA")
plt.show()

plot_speed_param_search(100, "logs/exercise1/", speed_metric="fspeed_cycle")
plt.show()"""

nsim = 10  # Number of samples
base = 2  # Logarithmic base

steepnesses = np.logspace(np.log2(1), np.log2(100), nsim, base=base)
d = 1
from plot_results import plot_speed_param_search
import matplotlib.pyplot as plt

plot_speed_param_search(100, "logs/exercise1/", speed_metric="fspeed_PCA")
plt.show()

plot_speed_param_search(100, "logs/exercise1/", speed_metric="fspeed_cycle")
plt.show()
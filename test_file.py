import numpy as np

def sigmoid(x, a):
    return 1 / (1 + np.exp(-a * x))

def square_wave_controller(input_signal, gain):
    # Normalize input to range [-1, 1]
    normalized_input = input_signal / np.max(np.abs(input_signal))
    # Apply sigmoidal function
    sigmoid_output = sigmoid(normalized_input, gain)
    # Scale and shift the output to range [-1, 1]
    output_signal = 2 * sigmoid_output - 1
    return output_signal

# Example usage
input_signal = np.sin(np.linspace(0, 10, 100))  # Example sinusoidal input
gain = 10  # Adjust gain to control steepness of transition
output_signal = square_wave_controller(input_signal, gain)

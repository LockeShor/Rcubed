import numpy as np
from scipy.optimize import curve_fit, minimize
import pandas as pd
import matplotlib.pyplot as plt

# Load roadrunner test data
data = pd.read_csv('data.csv')

# Extract columns
Kv = data['Kv'].values
Ka = data['Ka'].values
Ks = data['Ks'].values
Error = np.abs(data['Error'].values)

# Normalize data
Kv_normalized = (Kv - np.min(Kv)) / (np.max(Kv) - np.min(Kv))
Ka_normalized = (Ka - np.min(Ka)) / (np.max(Ka) - np.min(Ka))
Ks_normalized = (Ks - np.min(Ks)) / (np.max(Ks) - np.min(Ks))

# Print normalized data for verification
print("Normalized Kv:", Kv_normalized)
print("Normalized Ka:", Ka_normalized)
print("Normalized Ks:", Ks_normalized)

# Prepare each row into the inputs and outputs of the function to fit
inputs = np.array([Kv_normalized, Ka_normalized, Ks_normalized])
outputs = Error

# Used for printing only
varnames = ['a', 'm', 'h', 'n', 'j', 'k', 'o', 'p']

# Function to fit
def f(x, a, m, h, n, j, k, o, p):
    return a * np.sqrt(m * ((x[0] - h)**2) + n * ((x[1] - j)**2) + o * ((x[2] - p)**2)) + k

# Fit and print results for each independent variable
initial_guess = [1, 1, 0.5, 1, 0.5, 0.5, 1, 0.5]
bounds = (0, np.inf)

popt, pcov = curve_fit(f, inputs, outputs, p0=initial_guess, bounds=bounds, maxfev=10000)

for i in range(len(popt)):
    print(f'{varnames[i]} = {popt[i]:f}')

# Give the whole equation for use in desmos or other
print("Final Equation: z = {0}sqrt({1}((x-{2})^2) + {3}((y-{4})^2) + {6}((w-{7})^2)) + {5}".format(popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7]))

# Fitted function
def fitted(x):
    return abs(f(x, *popt))

# Find the minimum point of the function - lowest error
min_optimized = minimize(fitted, [0.5, 0.5, 0.5], method="Nelder-Mead")

min_input_vector = min_optimized.x
min_output = fitted(min_input_vector)

print("Minimum Point: {0} at {1}".format(min_output, min_input_vector))

# Print relevant results in a more readable format
print("\n-------------------\nBest Fit for Roadrunner:\nKv = {0}\nKa = {1}\nKs = {2}\nError = {3}".format(min_input_vector[0], min_input_vector[1], min_input_vector[2], min_output))

# Plot data and fit
plt.figure(figsize=(10, 6))
plt.scatter(Kv_normalized, outputs, label='Data')
plt.plot(Kv_normalized, f(inputs, *popt), label='Fit', color='red')
plt.xlabel('Kv (normalized)')
plt.ylabel('Error')
plt.legend()
plt.title('Curve Fit')
plt.show()

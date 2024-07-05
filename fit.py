import numpy as np
from scipy.optimize import curve_fit, minimize

#import roadrunner test data
data = open('data.csv', 'r').read().splitlines()[1:]

#parse csv
Kv, Ka, Ks, Error = [], [], [], []
for line in data:
    values = line.split(',')
    Kv.append(float(values[0]))
    Ka.append(float(values[1]))
    Ks.append(float(values[2]))
    Error.append(abs(float(values[3])))

#prepare each row into the inputs and outputs of the function to fit
inputs = [
    Kv,
    Ka,
    Ks
]
outputs = Error

#used for printing only
varnames = ['a', 'm', 'h', 'n', 'j', 'k', 'o', 'p']
# 
# a: overall steepness, around 810 (may be redundant with n2 & m2)
# m: steepness in Kv direction, around 0.4
# h: center of Kv direction, around 0.016
# n: steepness in Ka direction, around 1.13
# j: center of Ka direction, around 0.002
# k: center of Output/Error direction, around 0.195
# o: steepness in Ks direction, around 1
# p: center of Ks direction, around 0.001

#function to fit (maybe put abs around it because error can be negative?)
def f(x, a, m, h, n, j, k, o, p):
    return a * np.sqrt(m*((x[0] - h)**2) + n*((x[1] - j)**2) + o*((x[2] - p)**2)) + k

#fit and print results for each independent variable
popt, pcov, infodict, mesg, ier = curve_fit(f, inputs, outputs, p0=[810, 0.4, 0.016, 1.13, 0.002, 0.195, 1, 0.004], full_output=True, maxfev=10000)
for i in range(len(popt)):
    print('{0} = {1:f}'.format(varnames[i], popt[i]))

#give the whole equation for use in desmos or other
# print("Final Equation: z = {0}sqrt({1}((x-{2})^2) + {3}((y-{4})^2)) + {5}".format(popt[0], popt[1], popt[2], popt[3], popt[4], popt[5]))
print("Final Equation: z = {0}sqrt({1}((x-{2})^2) + {3}((y-{4})^2) + {6}((w-{7})^2)) + {5}".format(popt[0], popt[1], popt[2], popt[3], popt[4], popt[5], popt[6], popt[7]))
#print(pcov)
# print(infodict)
# print(mesg)
# print(ier)

#fitted = the final regressed function
def fitted(x):
    return abs(f(x, *popt))

#find the minimum point of the function - lowest error
min_optimized = minimize(fitted, [0,0,0], method="Nelder-Mead")

min_input_vector = min_optimized.x
min_output = fitted(min_input_vector)

print("Minimum Point: {0} at {1}".format(min_output, min_input_vector))

#print relevant results in a more readable format
print("\n-------------------\nBest Fit for Roadrunner:\nKv = {0}\nKa = {1}\nKs = {2}\nError = {3}".format(min_input_vector[0], min_input_vector[1], min_input_vector[2], min_output))

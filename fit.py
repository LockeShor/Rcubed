import numpy as np
from scipy.optimize import curve_fit

data = open('data.csv', 'r').read().splitlines()[1:]

Kv, Ka, Ks, Error = [], [], [], []
for line in data:
    values = line.split(',')
    Kv.append(float(values[0]))
    Ka.append(float(values[1]))
    Ks.append(float(values[2]))
    Error.append(float(values[3]))

inputs = [
    Kv,
    Ka
]


outputs = Error

varnames = ['m', 'h', 'n', 'j', 'k']
def f(x, m, h, n, j, k):
    return m*abs(x[0]-h) + n*abs(x[1]-j) + k

popt, pcov, infodict, mesg, ier = curve_fit(f, inputs, outputs, p0=[1500,0.016,577,0.002,0.5], full_output=True)
for i in range(len(popt)):
    print('{0} = {1:f}'.format(varnames[i], popt[i]))


print("Final Equation: z = {0}abs(x-{1}) + {2}abs(y-{3}) + {4}".format(popt[0], popt[1], popt[2], popt[3], popt[4]))
# print(pcov)
# print(infodict)
# print(mesg)
# print(ier)

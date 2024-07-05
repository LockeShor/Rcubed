import numpy as np
from scipy.optimize import curve_fit, minimize

#import roadrunner test data
kvkadata = open('kv&ka.csv', 'r').read().splitlines()[1:]

#parse csv
Kv, Ka, Stdev = [], [], []
for line in kvkadata:
    values = line.split(',')
    Kv.append(float(values[0]))
    Ka.append(float(values[1]))
    Stdev.append(float(values[2]))

#prepare each row into the inputs and outputs of the function to fit
inputs = [
    Kv,
    Ka
]
output = Stdev

#used for printing only
varnames = ['a', 'h', 'b', 'k', 'c']
# a: steepness in x direction, around 0.4
# h: center of x direction, around 0.016
# b: steepness in y direction, around 1.13
# k: center of y direction, around 0.002
# c: center of z direction, around 0.195

#function to fit (maybe put abs around it because error can be negative?)
def f1(xy, a, h, b, k, c):
    x,y = xy
    return (a*np.abs(x-h))+(b*np.abs(y-k))+c

#fit and print results for each independent variable
popt, pcov, infodict, mesg, ier = curve_fit(f1, inputs, output, p0=[1500, 0.016, 577, 0.002, 0.5], full_output=True)

finalKv = popt[1]
finalKa = popt[3]

# for i in range(len(popt)):
#     print('{0} = {1:f}'.format(varnames[i], popt[i]))

#give the whole equation for use in desmos or other
print("First Equation: stdev = {0}|Kv-{1}|+{2}|Ka-{3}|+{4}".format(popt[0], popt[1], popt[2], popt[3], popt[4]))
# print(pcov)
# print(infodict)
# print(mesg)
# print(ier)

#print("Minimum Point: {0} at {1}".format(popt[1],popt[3]))

ksdata = open('ks.csv', 'r').read().splitlines()[1:]

#parse csv
Ks, Error = [], []
for line in ksdata:
    values = line.split(',')
    Ks.append(float(values[0]))
    Error.append(float(values[1]))

def f2(x,m,b):
    return m*(x-b)

popt2, pcov2 = curve_fit(f2, Ks, Error)
print("Second Equation: error = {0}(Ks-{1})".format(popt2[0], popt2[1]))

finalKs = popt2[1]

print("Final Values: Kv = {0}, Ka = {1}, Ks = {2}".format(round(finalKv,6), round(finalKa,6), round(finalKs,6)))



#print relevant results in a more readable format
#print("\n-------------------\nBest Fit for Roadrunner:\nKv = {0}\nKa = {1}\nKs = {2}\nError = {3}".format(min_input_vector[0], min_input_vector[1], "Not Implemented", min_output))

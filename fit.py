import numpy as np
from scipy.optimize import curve_fit

#import roadrunner test data
kvkadata = open('kv&ka.csv', 'r').read().splitlines()[1:]

#parse csv
Kv, Ka, Stdev = [], [], []
for line in kvkadata:
    values = line.split(',')
    Kv.append(float(values[0]))
    Ka.append(float(values[1]))
    Stdev.append(float(values[2]))

#prepare each row into the inputs and outputs of the first function to fit
inputs = [
    Kv,
    Ka
]
output = Stdev


# a: steepness in x direction, around 1500
# h: center of x direction, around 0.016
# b: steepness in y direction, around 577
# k: center of y direction, around 0.002
# c: center of z direction, around 0.5
#first function to fit - returns best Ka and Kv values
def f1(xy, a, h, b, k, c):
    x,y = xy
    return (a*np.abs(x-h))+(b*np.abs(y-k))+c
#TODO: implement conical fitting function (as long as that better aligns to the additional data we gather)

#fit the data and get the best values for Ka and Kv, along with extra info
popt, pcov, infodict, mesg, ier = curve_fit(f1, inputs, output, p0=[1500, 0.016, 577, 0.002, 0.5], full_output=True)

finalKv = popt[1] #index 1 = h value = best Kv
finalKa = popt[3] #index 3 = k value = best Ka

#give the whole equation for use in desmos or other
print("Kv and Ka Equation: stdev = {0}|Kv-{1}|+{2}|Ka-{3}|+{4}".format(popt[0], popt[1], popt[2], popt[3], popt[4]))


# TODO:
# We need to stop at this point and output the optimal Kv and Ka, so that the user can gather the Ks data using those values
# Not sure exactly how we want to do this, we may just want two scripts

ksdata = open('ks.csv', 'r').read().splitlines()[1:]

#parse csv
Ks, Error = [], []
for line in ksdata:
    values = line.split(',')
    Ks.append(float(values[0]))
    Error.append(float(values[1]))

#second function to fit - returns best Ks value (simple linear regression)
def f2(x,m,b):
    return m*(x-b)

#fit and print the equation for Ks
popt2, pcov2 = curve_fit(f2, Ks, Error)
print("Ks Equation: Error = {0}(Ks-{1})".format(popt2[0], popt2[1]))

finalKs = popt2[1] #index 1 = b value = best Ks

#print results in a more readable format
print("{3}\nOptimal Values for RoadRunner:\nKv = {0}\nKa = {1}\nKs = {2}".format(finalKv, finalKa, finalKs, "-"*40))

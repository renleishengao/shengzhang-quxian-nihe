#!/usr/bin/env
# -*- coding: UTF-8 -*-

import CurveFit
import numpy as np
import matplotlib.pyplot as plt
import csv
import random
import math

def readData(fileAddress):
    with open(fileAddress, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
        dataList = list(data)
    ages = dataList[0]
    heights = dataList[1]
    if (len(dataList) >= 3):
        sampleSizes = dataList[2]
        stdDeviations = dataList[3]
        return CurveFit.Data(ages, heights, stdDeviations/np.sqrt(sampleSizes), system_error=0.1/np.sqrt(3))
    else:
        return CurveFit.Data(ages, heights, np.array([1.] * len(ages)))

def generateChiSquare(dof):
    num = 0
    for i in range(dof):
        num += random.gauss(0, 1)**2
    return num

def addRandomError(data, sigma, sampleSize, minAge, maxAge):
    new_x_arr = []
    new_y_arr = []
    new_variance_arr = []
    for index in range(len(data.x_array)):
        age = data.x_array[index]
        if (age >= minAge and age <= maxAge and not age.is_integer()):
            new_x_arr.append(age)
            new_y_arr.append(random.gauss(data.y_array[index], sigma / np.sqrt(sampleSize)))
            new_variance_arr.append(sigma * generateChiSquare(sampleSize-1)/sampleSize)
    return CurveFit.Data(new_x_arr, new_y_arr, new_variance_arr / np.sqrt(sampleSize))

if __name__ == "__main__":
    WHOstd = readData("csv/WHOnan.csv")
    sampleSizes = [50, 100, 150, 300, 1000, 4000]
    trialTime = 1000
    variance = 6
    #print("sample size,fitted height")
    for sampleSize in sampleSizes:
        firstOrder = 0
        secondOrder = 0
        fourthOrder = 0
        for trial in range(trialTime):
            realData = addRandomError(WHOstd, variance, sampleSize, 7.5, 17.5)
            fit = realData.fit_by(WHOstd.get_linear_interpolation(), fix_scaling='').get_fit()
            #print("{},{}".format(sampleSize, fit.fitted_curve(19.0)))
            firstOrder  += np.abs(fit.fitted_curve(17.5) - 175.77)
            secondOrder += (fit.fitted_curve(17.5) - 175.77)**2
            fourthOrder += (fit.fitted_curve(17.5) - 175.77)**4
            #np.abs(fit.fitted_curve(19.0) - 176.54)
        print("Sample size:", sampleSize)
        print(firstOrder/trialTime, variance*np.sqrt(2/(math.pi*sampleSize)))
        print(secondOrder/trialTime, variance**2/sampleSize)
        print(fourthOrder/trialTime, 3*variance**4/sampleSize**2)
        print("---")
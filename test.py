#!/usr/bin/env
# -*- coding: UTF-8 -*-

import CurveFit
import numpy as np
import matplotlib.pyplot as plt
import csv

def readData(fileAddress):
    with open(fileAddress, newline='') as csvfile:
        data = csv.reader(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_NONNUMERIC)
        dataList = list(data)
    ages = dataList[0]
    heights = dataList[1]
    if (len(dataList) >= 3):
        sampleSizes = dataList[2]
        stdDeviations = dataList[3]
        return CurveFit.Data(ages, heights, stdDeviations/np.sqrt(sampleSizes))
    else:
        return CurveFit.Data(ages, heights, np.array([1.] * len(ages)))

if __name__ == "__main__":

    # Data
    zg05nan = readData("csv/zhongguo05nan.csv")
    zg05nv  = readData("csv/zhongguo05nv.csv")
    cdch16nan = readData("csv/chengduchenghua16nan.csv").truncate(12)
    cdch16nv  = readData("csv/chengduchenghua16nv.csv").truncate(12)

    # Fit
    '''fit = CurveFit.multiple_fit([cd14chengnan,cd14chengnv], 
                              [zg05nan.linear_interpolation, zg05nv.linear_interpolation],
                              fix_scaling="x")'''
    fit_nan = CurveFit.fit(cdch16nan, zg05nan.get_linear_interpolation(),fix_scaling='')
    fit_nv  = CurveFit.fit(cdch16nv , zg05nv.get_linear_interpolation() ,fix_scaling='')

    #cd14chengnan_curve, cd14chengnv_curve = fit[1]
    nan_curve, nv_curve = fit_nan[1], fit_nv[1]
    
    nan_curve = np.vectorize(nan_curve)
    nv_curve  = np.vectorize(nv_curve)

    print(fit_nan[2], fit_nv[2])

    # Set up plot
    x = np.linspace(6, 18, 100)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # Plot 
    ax.errorbar(cdch16nan.x_array, cdch16nan.y_array,2*cdch16nan.std_deviations, fmt='xr', label='cd14-chengnan')
    ax.errorbar(cdch16nv.x_array , cdch16nv.y_array ,2*cdch16nv.std_deviations , fmt='xb', label='cd14-chengnv')
    ax.plot(x, nan_curve(x), color='tab:pink', label="cd14-chengnan-nihe")
    ax.plot(x, nv_curve(x) , color='tab:cyan', label="cd14-chengnv-nihe")

    ax.legend()
    ax.grid(True)
    plt.show()
    
    # 配色方案
    # bj14 = r/tab:pink, bj01 = b/tab:cyan, jpn = g:tab:olive
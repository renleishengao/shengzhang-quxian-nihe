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
    cd14chengnan = readData("csv/chengdu14chengnan.csv").truncate(11)
    cd14chengnv  = readData("csv/chengdu14chengnv.csv").truncate(11)

    # Fit
    fit = CurveFit.multiple_fit([cd14chengnan,cd14chengnv], 
                              [zg05nan.linear_interpolation, zg05nv.linear_interpolation],
                              fix_scaling="x")

    cd14chengnan_curve, cd14chengnv_curve = fit[1]
    print(fit[2])
    
    vcd14chengnan_curve = np.vectorize(cd14chengnan_curve)
    vcd14chengnv_curve  = np.vectorize(cd14chengnv_curve)

    # Set up plot
    x = np.linspace(7, 18, 100)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    # Plot 
    #ax.scatter(shxh2014diaoyan.x_array, shxh2014diaoyan.y_array, color='r')
    ax.errorbar(cd14chengnan.x_array, cd14chengnan.y_array,2*cd14chengnan.std_deviations, fmt='xr', label='cd14-chengnan')
    ax.errorbar(cd14chengnv.x_array , cd14chengnv.y_array ,2*cd14chengnv.std_deviations , fmt='xb', label='cd14-chengnv')
    ax.plot(x, vcd14chengnan_curve(x), color='tab:pink', label="cd14-chengnan-nihe")
    ax.plot(x, vcd14chengnv_curve(x) , color='tab:cyan', label="cd14-chengnv-nihe")

    ax.legend()
    ax.grid(True)
    plt.show()
    
    # 配色方案
    # bj14 = r/tab:pink, bj01 = b/tab:cyan, jpn = g:tab:olive
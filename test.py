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
    chn2005 = readData("csv/chn2005.csv")
    std_rectangle = [6.5,17.5,120.7,172.5]
    
    qingdao2014urban = readData("csv/qingdao2014urban.csv")
    jpn = readData("csv/jpn.csv")
    kor = readData("csv/kor.csv")
    WHO = readData("csv/WHO.csv")
    bjhd2010 = readData("csv/bjhd2010.csv").truncate(11)
    beijing2001cohort = readData("csv/beijing2001cohort.csv")
    beijing2014diaoyan = readData("csv/beijing2014diaoyan.csv")
    cd2014urban = readData("csv/cd2014urban.csv")
    shxh2014diaoyan = readData("csv/shxh2014diaoyan.csv")

    # Fit
    cd2014urban_curve_new = CurveFit.fit_new(cd2014urban, chn2005.linear_interpolation)[1]
    cd2014urban_curve = CurveFit.fit(cd2014urban, chn2005.linear_interpolation, std_rectangle)[1]
    print(cd2014urban_curve(18.0))
    print(cd2014urban_curve_new(18.0))

    # Set up plot
    #x = np.linspace(6, 18, 100)
    #fig = plt.figure()
    #ax = fig.add_subplot(1, 1, 1)
    # Plot 
    #ax.scatter(shxh2014diaoyan.x_array, shxh2014diaoyan.y_array, color='r')
    #ax.errorbar(cd2014urban.x_array, cd2014urban.y_array,2*cd2014urban.std_deviations, fmt='xr', label='cd2014-chengshi-diaoyan')
    #ax.plot(x, shxh2014_curve(x), color='tab:pink', label="cd2014-chengshi-diaoyan-nihe")

    # bj14 = r/tab:pink, bj01 = b/tab:cyan, jpn = g:tab:olive
    '''ax.errorbar(beijing2014diaoyan.x_array, beijing2014diaoyan.y_array,2*beijing2014diaoyan.std_deviations, fmt='xr', label='bj2014-diaoyan')
    ax.plot(x, bj14_curve(x), color='tab:pink', label="bj2014-diaoyan-nihe")
    ax.scatter(beijing2001cohort.x_array, beijing2001cohort.y_array, color = 'b', label='bj2001-chusheng')
    ax.plot(x, bj01cohort_curve(x), color='tab:cyan', label='bj2001-chusheng-nihe')
    ax.scatter(jpn.x_array, jpn.y_array, color='g', label='riben')
    ax.plot(x, jpn_curve(x), color='tab:olive', label='riben-nihe')'''

    #ax.legend()
    #ax.grid(True)
    #plt.show()
    
    # Use Leave-One-Out to test the fit's stablity

    '''for n in range(0,11):
        qingdao2014urban_truncated = qingdao2014urban.truncate(n)
        curve_truncated = CurveFit.fit(qingdao2014urban_truncated,
                    chn2005.linear_interpolation, chn2005_rectangle, 
                    show=True)
        z = curve_truncated(x)
        print(n+7, " yr old omitted")
        plt.errorbar(qingdao2014urban.x_array, qingdao2014urban.y_array, 2*qingdao2014urban.std_deviations, 
                     fmt='x')
        plt.plot(x,y,'r', label="original curve")
        plt.plot(x,z,'b', label="curve fitted with one age group left out")
        plt.show()'''
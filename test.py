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
    chn2005_rectangle = [6.5, 17.5, 120.7, 172.5]
    chn2005 = readData("csv/chn2005.csv")
    
    qingdao2014urban = readData("csv/qingdao2014urban.csv")
    jpn = readData("csv/jpn.csv")
    kor = readData("csv/kor.csv")
    WHO = readData("csv/WHO.csv")

    # Set up plot
    x = np.linspace(6, 18, 100)
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    #ax.spines['left'].set_position('center')
    #ax.spines['bottom'].set_position('center')
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Fit and plot
    curve = CurveFit.fit(kor,
                         chn2005.linear_interpolation, chn2005_rectangle,
                         showResidual=False)
    y = curve(x)
    print("18 year old prediction", curve(18.0))
    #plt.errorbar(qingdao2014urban.x_array, qingdao2014urban.y_array, 2*qingdao2014urban.std_deviations, fmt='x')
    plt.plot(kor.x_array, kor.y_array, 'x')
    plt.plot(x,y,'r', label="Fitted curve")
    plt.savefig('kor_chn2005.png', dpi=600)
    
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
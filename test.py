#!/usr/bin/env
# -*- coding: UTF-8 -*-

import CurveFit
import numpy as np

import matplotlib.pyplot as plt

if __name__ == "__main__":

    # Data
    if True:
        chn2005_ages = np.array([4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0,16.5,17.0,17.5,18.0])
        chn2005_heights = np.array([104.1,107.7,111.3,114.7,117.7,120.7,124.0,127.1,130.0,132.7,135.4,137.9,140.2,142.6,145.3,148.4,151.9,155.6,159.5,163.0,165.9,168.2,169.8,171.0,171.6,172.1,172.3,172.5,172.7])
        chn2005_rectangle = [6.5, 17.5, 120.7, 172.5]
        chn2005 = CurveFit.Data(chn2005_ages, chn2005_heights, [1]*29)
        #chn2005_curve = chn2005.linear_interpolate()

        '''jpn_ages = np.arange(6.5,18,1)
        jpn_heights = [116.62,122.44,128.33,133.50,138.80,145.53,152.81,160.75,165.96,168.37,169.59,170.46]
        WHO_ages = np.arange(7,17.5,1)
        WHO_heights = [121.7,127.3,132.6,137.8,143.1,149.1,156.0,163.2,169.0,172.9,175.2]'''

        qingdao2014urban_ages = np.arange(7.5,18,1)
        qingdao2014urban_heights = np.array([130.0,136.4,140.6,145.4,151.4,159.9,167.2,173.5,175.6,176.2,177.0])
        qingdao2014urban_N = np.array([99,144,100,99,99,109,102,100,100,102,112])
        qingdao2014urban_sample_std_deviation = np.array([5.3,5.7,5.3,5.3,7.6,8.1,8.2,6.2,5.9,5.9,6.2])
        qingdao2014urban_std_deviation = qingdao2014urban_sample_std_deviation / np.sqrt(qingdao2014urban_N)
        qingdao2014urban = CurveFit.Data(qingdao2014urban_ages, qingdao2014urban_heights, qingdao2014urban_std_deviation)

    # Set up plot
    if True:
        x = np.linspace(6, 18, 100)
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1)
        #ax.spines['left'].set_position('center')
        #ax.spines['bottom'].set_position('center')
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.yaxis.set_ticks_position('left')

    curve = CurveFit.fit(qingdao2014urban,
                         chn2005.linear_interpolation, chn2005_rectangle, 
                         show=True)
    y = curve(x)
    plt.errorbar(qingdao2014urban.x_array, qingdao2014urban.y_array, 2*qingdao2014urban.std_deviations, 
                fmt='x')
    plt.plot(x,y,'r', label="Fitted curve")
    plt.show()
    
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
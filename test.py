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
        return CurveFit.Data(ages, heights, stdDeviations/np.sqrt(sampleSizes), system_error=0.1/np.sqrt(3))
    else:
        return CurveFit.Data(ages, heights, np.array([1.] * len(ages)))

if __name__ == "__main__":

    # 环渤海：北京、天津、青岛
    # Data
    # Ref data
    zg05nan = readData("csv/zhongguo05nan.csv")
    zg05nv  = readData("csv/zhongguo05nv.csv")

    cities = ['beijing', 'tianjin', 'qingdao']

    # Cities' data
    datas_nan = {city: readData("csv/{}14chengnan.csv".format(city)).truncate(11) for city in cities}
    datas_nv  = {city: readData("csv/{}14chengnv.csv".format(city)).truncate(11)  for city in cities}

    # Fit
    fits_nan = {city: CurveFit.fit(datas_nan[city], zg05nan.get_linear_interpolation()) for city in cities}
    fits_nv  = {city: CurveFit.fit(datas_nv[city] , zg05nv.get_linear_interpolation() ) for city in cities}

    # Set up plot
    x = np.linspace(7, 18, 100)
    
    # 配色方案
    # bj14 = r/tab:pink, bj01 = b/tab:cyan, jpn = g:tab:olive
    color_data = {'beijing': 'r', 'tianjin': 'g', 'qingdao': 'b'}
    color_fit = {'beijing': 'tab:pink', 'tianjin':'tab:olive', 'qingdao':'tab:cyan'}
    # Plot 
    # Plot nan
    fig_nan = plt.figure()
    ax_nan = fig_nan.add_subplot(1, 1, 1)
    for city in cities:
        ax_nan.errorbar(datas_nan[city].x_array, datas_nan[city].y_array, 2*datas_nan[city].std_deviations, 
                    fmt='x{}'.format(color_data[city]), label='{}-nan'.format(city))
        ax_nan.plot(x, np.vectorize(fits_nan[city][1])(x),
                    color=color_fit[city], label='{}-nan-nihe'.format(city))
    ax_nan.legend()
    ax_nan.grid(True)
    plt.savefig("fit_nan.png",dpi=600)
    # Plot nv
    fig_nv = plt.figure()
    ax_nv = fig_nv.add_subplot(1, 1, 1)
    for city in cities:
        ax_nv.errorbar(datas_nv[city].x_array, datas_nv[city].y_array, 2*datas_nv[city].std_deviations, 
                    fmt='x{}'.format(color_data[city]), label='{}-nv'.format(city))
        ax_nv.plot(x, np.vectorize(fits_nv[city][1])(x),
                    color=color_fit[city], label='{}-nv-nihe'.format(city))
    ax_nv.legend()
    ax_nv.grid(True)
    plt.savefig("fit_nv.png",dpi=600)
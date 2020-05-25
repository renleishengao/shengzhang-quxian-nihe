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

def analyze(address, age, action = 'plot', delete_18_yo = False):
    std_ref = readData("csv/zhongguo2005nan.csv").get_linear_interpolation()
    data = readData(address)
    if (delete_18_yo == True):
        data.delete_age_group(18.5)
    data.fit_by(std_ref)
    fit = data.get_fit()
    #print(fit.residual)
    #print(fit.ltransform)

    # Plot
    if (action == 'plot'):
        x = np.linspace(3.5, 20, 100)
        图 = plt.figure()
        坐标轴 = 图.add_subplot(1, 1, 1)
        坐标轴.errorbar(data.x_array, data.y_array, 2*data.std_deviations, fmt="xr", label="Shice")
        坐标轴.plot(x, np.vectorize(fit.fitted_curve)(x),color="tab:pink", label="Nihe")
        坐标轴.legend()
        坐标轴.grid(True)
        plt.show()

    if (action == 'print'):
        print(fit.fitted_curve(18.5))

if __name__ == "__main__":
    places = {1991: ["shijiazhuang", "taiyuan", "hohhot","changchun","harbin", "zhengzhou", "xian", "lanzhou", "xining", "yinchuan", "urumqi"],
              1979: ["taiyuan", "harbin","xian", "lanzhou"]}
    for year, placeList in places.items():
        if (year == 1991):
            age = 18.5
            print("城市,18.5岁城市汉族男性平均身高")
        if (year == 1979):
            age = 17.5
            print("城市,17.5岁城市汉族男性平均身高")
        for place in placeList:
            print(place + ",", end="")
            #print(year, place)
            analyze("csv/{}{}chengnan.csv".format(place, year),age,action="print")
            #if (year == 1979 and place == "taiyuan"):
            #    analyze("csv/{}{}chengnan.csv".format(place, year),age,action="plot")
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
    # Ref data
    cn2005std = readData("csv/zhongguo2005nan.csv")
    data_address = {
        "北京城": "beijing2010chengnan.csv",
        "北京乡": "beijing2010xiangnan.csv",
        "上海城": "shanghai2010chengnan.csv",
        "上海乡": "shanghai2010xiangnan.csv",
        "天津城": "tianjin2010chengnan.csv",
        "天津乡": "tianjin2010xiangnan.csv",
        "烟台": "yantai2010nan.csv",
        "乌鲁木齐城": "urumqi2010chengnan.csv",
        "乌鲁木齐乡": "urumqi2010xiangnan.csv",
        "青岛城": "qingdao2010chengnan.csv",
        "太原城": "taiyuan2010chengnan.csv",
        "太原乡": "taiyuan2010xiangnan.csv"
    }

    np.set_printoptions(precision=1)
    for place in data_address:
        fit = readData("csv/" + data_address[place]).truncate(11).fit_by(cn2005std.get_linear_interpolation()).get_fit()
        print(place)
        print("残差      : {0:.1f}".format(fit.residual))
        print("18.0岁身高: {0:.1f}".format(fit.fitted_curve(18.0)))
        print("19.0岁身高: {0:.1f}".format(fit.fitted_curve(19.0)))
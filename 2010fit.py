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
    WHOstd    = readData("csv/WHOnan.csv")
    data_address = {
        "北京城市汉族": "beijing2010chengnan.csv",
        "北京乡村汉族": "beijing2010xiangnan.csv",
        "上海城市汉族": "shanghai2010chengnan.csv",
        "上海乡村汉族": "shanghai2010xiangnan.csv",
        "天津城市汉族": "tianjin2010chengnan.csv",
        "天津乡村汉族": "tianjin2010xiangnan.csv",
        "烟台汉族": "yantai2010nan.csv",
        "乌鲁木齐城市汉族": "urumqi2010chengnan.csv",
        "乌鲁木齐乡村汉族": "urumqi2010xiangnan.csv",
        "青岛城市汉族": "qingdao2010chengnan.csv",
        "太原城市汉族": "taiyuan2010chengnan.csv",
        "太原乡村汉族": "taiyuan2010xiangnan.csv",
        "南京城市汉族": "nanjing2010chengnan.csv",
        "南京乡村汉族": "nanjing2010xiangnan.csv",
        "兰州汉族": "lanzhou2010nan.csv",
        "杭州城市汉族": "hangzhou2010chengnan.csv",
        "杭州乡村汉族": "hangzhou2010xiangnan.csv",
        "福州汉族": "fuzhou2010nan.csv",
        "通辽城市蒙古族": "tongliaomenggu2010chengnan.csv",
        "通辽乡村蒙古族": "tongliaomenggu2010xiangnan.csv",
        "延边城市朝鲜族": "yanbianchaoxian2010chengnan.csv",
        "延边乡村朝鲜族": "yanbianchaoxian2010xiangnan.csv",
        "阿勒泰哈萨克族": "altaihasake2010nan.csv",
        "喀什城市维吾尔族": "kashgaruyghur2010chengnan.csv",
        "喀什乡村维吾尔族": "kashgaruyghur2010xiangnan.csv",
        "广州城市汉族": "guangzhou2010chengnan.csv",
        "广州乡村汉族": "guangzhou2010xiangnan.csv"
    }

    '''
    print("地点,中国拟合17.5岁身高,中国拟合残差,世卫17.5岁身高,世卫拟合残差")
    for place in data_address:
        data = readData("csv/" + data_address[place]).delete_age_group(18.5)
        fit_cn = data.fit_by(cn2005std.get_linear_interpolation(),fix_scaling='').get_fit()
        fit_WHO = data.fit_by(WHOstd.get_linear_interpolation(),fix_scaling='').get_fit()
        print(place + ",{},{},{},{}".format(fit_cn.fitted_curve(17.5),fit_cn.residual,
                                                  fit_WHO.fitted_curve(17.5),fit_WHO.residual))
    '''
    ## 喀什乡村维吾尔族分析
    place = "北京城市汉族"
    data = readData("csv/" + data_address[place]).delete_age_group([7.5,18.5])
    fit_cn = data.fit_by(cn2005std.get_linear_interpolation(),fix_scaling='').get_fit()
    fit_WHO = data.fit_by(WHOstd.get_linear_interpolation(),fix_scaling='').get_fit()

    x = np.linspace(2, 22, 100)
    图 = plt.figure()
    坐标轴 = 图.add_subplot(1, 1, 1)
    坐标轴.errorbar(data.x_array, data.y_array, 2*data.std_deviations, fmt="xr", label="Shice")
    坐标轴.plot(x, np.vectorize(fit_cn.fitted_curve)(x),color="tab:pink", label="Nihe")
    坐标轴.legend()
    坐标轴.grid(True)

    print(fit_cn.residual)
    print(fit_WHO.residual)
    plt.show()
  
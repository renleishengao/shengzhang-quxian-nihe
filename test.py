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
        return CurveFit.Data(ages, heights, stdDeviations/np.sqrt(sampleSizes), system_error=0.5/np.sqrt(3))
    else:
        return CurveFit.Data(ages, heights, np.array([1.] * len(ages)))

if __name__ == "__main__":

    # Ref data
    中国05男数据 = readData("csv/zhongguo05nan.csv")
    中国05女数据  = readData("csv/zhongguo05nv.csv")

    # 分析成都市成华区2016年健康体检数据
    成都男数据 = readData("csv/chengduchenghua2016nan.csv").truncate(12).fit_by(中国05男数据.get_linear_interpolation())
    成都女数据 = readData("csv/chengduchenghua2016nv.csv").truncate(12).fit_by(中国05女数据.get_linear_interpolation())

    # 打印残差
    print(成都男数据.get_fit().residual)
    print(成都女数据.get_fit().residual)

    x = np.linspace(6, 19, 100)
    图 = plt.figure()
    坐标轴 = 图.add_subplot(1, 1, 1)

    坐标轴.errorbar(成都男数据.x_array, 成都男数据.y_array, 2*成都男数据.std_deviations, fmt="xr", label="CDCH-Nan-Shice")
    坐标轴.plot(x, np.vectorize(成都男数据.get_fit().fitted_curve)(x),color="tab:pink", label="CDCH-Nan-Nihe")
    坐标轴.errorbar(成都女数据.x_array, 成都女数据.y_array, 2*成都女数据.std_deviations, fmt="xg", label="CDCH-Nü-Shice")
    坐标轴.plot(x, np.vectorize(成都女数据.get_fit().fitted_curve)(x),color="tab:olive", label="CDCH-Nü-Nihe")

    坐标轴.legend()
    坐标轴.grid(True)

    plt.show()
    #plt.savefig("chengdu-analysis.png",dpi=600)

    '''
    # 分析青岛2002和2014年城男数据
    年份组 = [2002, 2014]
    地址映射 = {2002: "csv/qingdao02chengnan.csv", 2014: "csv/qingdao14chengnan.csv"}

    # 分析残差
    for 年龄 in np.arange(7.5,19.5,1):
        青岛数据 = {年份: readData(地址映射[年份]).truncate(年龄-7.5) for 年份 in 年份组}
        for 年份 in 年份组:
            青岛数据[年份].fit_by(中国05男数据.get_linear_interpolation())
        for 年份 in 年份组:
            print(年龄, 年份, 青岛数据[年份].get_fit().residual)

    # 配色方案
    数据颜色 = {2002: 'r', 2014: 'g'}
    拟合颜色 = {2002: 'tab:pink', 2014:'tab:olive'}

    # 准备画图
    '''
    '''
    x = np.linspace(7, 18, 100)
    图 = plt.figure()
    坐标轴 = 图.add_subplot(1, 1, 1)

    for 年份 in 年份组:
        坐标轴.errorbar(青岛数据[年份].x_array, 青岛数据[年份].y_array, 2*青岛数据[年份].std_deviations, 
                    fmt='x{}'.format(数据颜色[年份]), label='{}-shice'.format(年份))
        坐标轴.plot(x, np.vectorize(青岛数据[年份].get_fit().fitted_curve)(x),
                    color=拟合颜色[年份], label='{}-nihe'.format(年份))
    
    坐标轴.legend()
    坐标轴.grid(True)
    plt.show()
    '''

    '''
    # 环渤海——北京、天津、青岛——生长曲线拟合
    # Data

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
    '''
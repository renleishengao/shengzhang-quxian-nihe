# 只对 7~17 岁数据拟合

import numpy as np
from scipy import optimize

def rescale(func, x, rectangle_old, rectangle_new):
    # 想象一个矩形 rectangle_old 把 func 的正好框住，
    # 现在通过线性变换把 rectangle_old 变成 rectangle_new
    # 返回线性变换后的函数
    alpha = (x - rectangle_new[0])/(rectangle_new[1] - rectangle_new[0])
    y = func((1-alpha) * rectangle_old[0] + alpha * rectangle_old[1])
    beta = (y - rectangle_old[2])/(rectangle_old[3] - rectangle_old[2])
    y_new = (1-beta) * rectangle_new[2] + beta * rectangle_new[3]
    return y_new

def log_likelyhood(ages, heights, std_deviations, ref):
    vref = np.vectorize(ref)
    ref_heights = vref(ages)
    return np.sum(((heights - ref_heights)/std_deviations)**2)

def fit(ages, heights, std_deviations, std_curve, std_rectangle, show = False):
    def obj_func(rectangle):
        def rescaled_func(x):
            return rescale(std_curve, x, std_rectangle, rectangle)
        return log_likelyhood(ages, heights, std_deviations, rescaled_func)
    result = optimize.minimize(obj_func, std_rectangle)
    if show == True:
        result_rectangle = result.x
        def fitted_curve(age):
            return rescale(std_curve, age, std_rectangle, result_rectangle)
        vfitted_curve = np.vectorize(fitted_curve)
        fitted_heights = vfitted_curve(ages)
        print(result.x)
        print("拟合身高：")
        print(fitted_heights)
        print("实测身高：")
        print(heights)
        print("差值：")
        print(fitted_heights - heights)
    return result

if __name__ == "__main__":
    chn2005_ages = [4.0,4.5,5.0,5.5,6.0,6.5,7.0,7.5,8.0,8.5,9.0,9.5,10.0,10.5,11.0,11.5,12.0,12.5,13.0,13.5,14.0,14.5,15.0,15.5,16.0,16.5,17.0,17.5,18.0]
    chn2005_heights = [104.1,107.7,111.3,114.7,117.7,120.7,124.0,127.1,130.0,132.7,135.4,137.9,140.2,142.6,145.3,148.4,151.9,155.6,159.5,163.0,165.9,168.2,169.8,171.0,171.6,172.1,172.3,172.5,172.7]
    chn2005_rectangle = [6.5, 17.5, 120.7, 172.5]

    jpn_ages = np.arange(6.5,18,1)
    jpn_heights = [116.62,122.44,128.33,133.50,138.80,145.53,152.81,160.75,165.96,168.37,169.59,170.46]

    qingdao2014urban_ages = np.arange(7.5,18,1)
    qingdao2014urban_heights = [130.0,136.4,140.6,145.4,151.4,159.9,167.2,173.5,175.6,176.2,177.0]
    qingdao2014urban_N = [99,144,100,99,99,109,102,100,100,102,112]
    qingdao2014urban_sample_std_deviation = [5.3,5.7,5.3,5.3,7.6,8.1,8.2,6.2,5.9,5.9,6.2]
    qingdao2014urban_std_deviation = qingdao2014urban_sample_std_deviation / np.sqrt(qingdao2014urban_N)

    WHO_ages = np.arange(7,17.5,1)
    WHO_heights = [121.7,127.3,132.6,137.8,143.1,149.1,156.0,163.2,169.0,172.9,175.2]

    #qingdao_ages = jpn_ages
    #qingdao_heights = jpn_heights

    def chn2005_curve(age):
        return np.interp(age, chn2005_ages, chn2005_heights)

    #result_jpn = fit(jpn_ages, jpn_heights,6, chn2005_curve, chn2005_rectangle, show=True)
    '''result_qingdao = fit(qingdao2014urban_ages, qingdao2014urban_heights, 6,
                         chn2005_curve, chn2005_rectangle, 
                         show=True)'''
    result_qingdao = fit(qingdao2014urban_ages, qingdao2014urban_heights, qingdao2014urban_std_deviation,
                         chn2005_curve, chn2005_rectangle, 
                         show=True)

    result_WHO = fit(WHO_ages, WHO_heights, 1,
                     chn2005_curve, chn2005_rectangle, 
                     show=True)
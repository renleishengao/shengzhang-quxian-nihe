#!/usr/bin/env
# -*- coding: UTF-8 -*-

import numpy as np
from scipy import optimize

class Data:
    def __init__(self, x_array, y_array, std_deviations):
        self.x_array = x_array
        self.y_array = y_array
        self.std_deviations = std_deviations
        self.linear_interpolate()

    def linear_interpolate(self):
        def func(x):
            return np.interp(x, self.x_array, self.y_array)
        self.linear_interpolation = func

    def truncate(self, n):
        x_array_truncated = np.delete(self.x_array, n)
        y_array_truncated = np.delete(self.y_array, n)
        std_deviations_truncated = np.delete(self.std_deviations, n)
        return Data(x_array_truncated, y_array_truncated, std_deviations_truncated)

def rescale(func, x, rectangle_old, rectangle_new):
    # 想象一个矩形 rectangle_old 把 func 的正好框住，
    # 现在通过线性变换把 rectangle_old 变成 rectangle_new
    # 返回线性变换后的函数
    alpha = (x - rectangle_new[0])/(rectangle_new[1] - rectangle_new[0])
    y = func((1-alpha) * rectangle_old[0] + alpha * rectangle_old[1])
    beta = (y - rectangle_old[2])/(rectangle_old[3] - rectangle_old[2])
    y_new = (1-beta) * rectangle_new[2] + beta * rectangle_new[3]
    return y_new

def log_likelihood(data, ref):
    vref = np.vectorize(ref)
    ref_y_array = vref(data.x_array)
    return np.sum(((data.y_array - ref_y_array)/data.std_deviations)**2)

def get_full_rectangle(incomplete_rectangle, std_rectangle, fix_scaling):
    if (fix_scaling == None):
        return incomplete_rectangle
    elif (fix_scaling == 'x'):
        return np.array([incomplete_rectangle[0], incomplete_rectangle[0] + std_rectangle[1] - std_rectangle[0],
                         incomplete_rectangle[1], incomplete_rectangle[2]])
    elif (fix_scaling == 'y'):
        return np.array([incomplete_rectangle[0], incomplete_rectangle[1],
                         incomplete_rectangle[2], incomplete_rectangle[2] + std_rectangle[3] - std_rectangle[2]])
    elif (fix_scaling == 'xy' or fix_scaling == 'yx'):
        return np.array([incomplete_rectangle[0], incomplete_rectangle[0] + std_rectangle[1] - std_rectangle[0],
                         incomplete_rectangle[1], incomplete_rectangle[1] + std_rectangle[3] - std_rectangle[2]])
    else:
        raise ValueError('A very specific bad thing happened.')

def get_incomplete_rectangle(full_rectangle, fix_scaling):
    if (fix_scaling == None):
        return full_rectangle
    elif (fix_scaling == 'x'):
        return np.delete(full_rectangle, 1)
    elif (fix_scaling == 'y'):
        return np.delete(full_rectangle, 3)
    elif (fix_scaling == 'xy' or fix_scaling == 'yx'):
        return np.delete(full_rectangle, [1,3])
    else:
        raise ValueError('A very specific bad thing happened.')


def fit(data, std_curve, std_rectangle, fix_scaling=None):
    def obj_func(incomplete_rectangle):
        rectangle = get_full_rectangle(incomplete_rectangle, std_rectangle, fix_scaling)
        def rescaled_func(var):
            return rescale(std_curve, var, std_rectangle, rectangle)
        return log_likelihood(data, rescaled_func)
    incomplete_std_rectangle = get_incomplete_rectangle(std_rectangle, fix_scaling)
    result = optimize.minimize(obj_func, incomplete_std_rectangle)
    full_result_rectangle = get_full_rectangle(result.x, std_rectangle, fix_scaling)
    def fitted_curve(var):
        return rescale(std_curve, var, std_rectangle, full_result_rectangle)
    vfitted_curve = np.vectorize(fitted_curve)
    return full_result_rectangle, vfitted_curve, obj_func(result.x)
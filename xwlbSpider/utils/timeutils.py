# -*- coding:utf-8 -*-

import time

def get_now_second():
    """
    :return: 获取精确到秒当期时间戳，10位
    """
    return int(time.time())


def get_now_millisecond():
    """
    :return: 获取精确毫秒当期时间戳,13位
    """
    millis = int(round(time.time() * 1000))
    return millis


def get_second(_time, format):
    """获取10位时间戳"""
    return int(time.mktime(time.strptime(_time, format)))


def get_millisecond(_time, format):
    """获取13位时间戳"""
    return int(round(time.mktime(time.strptime(_time, format)) * 1000))


def get_delta(t1,t2):
    """
    :param t1: 13位时间戳
    :param t2: 13位时间戳
    :return: 两个时间戳相减，返回秒数
    """
    res=int((t2 - t1)/1000)
    return res


def millisecond_to_time(millis):
    """13位时间戳转换为日期格式字符串"""
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(millis/1000))


def millisecond_to_time_fromat(millis, format):
    """13位时间戳转换为指定格式字符串"""
    return time.strftime(format, time.localtime(millis/1000))
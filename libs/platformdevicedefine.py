#!/usr/bin/env python
# -*- coding:utf-8 -*-

""":mod:`platformdevicedefine` -- 平台设备定义
"""

import const

# 结点设备类型
"""
结点设备类型定义:
    传感器代码       数据区[2 字节]           备注
    环境温度        0x01                    低位在前,高位在后; 单位:0.1 度 最高位:符号位 0 正,1 负
    环境湿度        0x02                    第一字节有效:精度 1%; 第二字节备用
    CO2             0x03
    土壤水分        0x04                    低位在前,高位在后; 单位:0.1 度
    光照度          0x05
    土壤温度        0x06                    低位在前,高位在后; 单位:0.1度; 最高位:符号位 0 正,1 负。
    土壤湿度        0x07                    第一字节有效:精度 1%; 第二字节备用
    温度            0xa1                    低位在前,高位在后; 单位:0.1 度 最高位:符号位 0 正,1 负
    湿度            0xa2                    第一字节有效:精度 1%; 第二字节备用
"""
const.DEVICE_TYPE_SENSOR_NONE           = 0         # 空数据
const.DEVICE_TYPE_SENSOR_TA             = 305       # Temperature Ambient 空气温度
const.DEVICE_TYPE_SENSOR_AH             = 306       # ambient humidity 空气湿度
const.DEVICE_TYPE_SENSOR_CO2            = 403       # CO2传感器
const.DEVICE_TYPE_SENSOR_SH             = 103       # soil humidity 土壤水分
const.DEVICE_TYPE_SENSOR_LU             = 307       # illuminance 光照度 luminous flux 光通量
const.DEVICE_TYPE_SENSOR_ST             = 101       # soil temperature 土壤温度 简称“土温”
const.DEVICE_TYPE_SENSOR_SMO            = 102       # Soil Moisture 土壤湿度

# 控制器类型
const.DEVICE_TYPE_DELAY_CTRL            = 1101      # relay 继电器

# 其他传感器
const.DEVICE_TYPE_ACCELERATION_X        = 10001     # 加速度，X轴
const.DEVICE_TYPE_ACCELERATION_Y        = 10002     # 加速度，Y轴
const.DEVICE_TYPE_ACCELERATION_Z        = 10003     # 加速度，Z轴
const.DEVICE_TYPE_ACCELERATION          = 10004     # 加速度，综合
const.DEVICE_TYPE_INFRARED              = 10005     # 人体红外
const.DEVICE_TYPE_PROXIMITY_SWITCH      = 10006     # 接近开关
const.DEVICE_TYPE_SMOKE_TRANSDUCER      = 10007     # 烟雾
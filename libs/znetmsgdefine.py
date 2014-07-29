#!/usr/bin/env python
# -*- coding:utf-8 -*-

""":mod:`znetmessagedefine` -- 消息常量定义
"""

import const

# 日期格式定义
const.COMPACTTIMEFORMAT = '%Y%m%d%H%M%S'       #例:20090313102835
const.ISOTIMEFORMAT     = '%Y-%m-%dT%X'        #例:2009-03-13T10:28:35

# 解码进度
const.DECODE_FRAME_BEGIN            = 'DF10'
const.DECODE_FRAME_HEAD_BEGIN       = 'DF20'
const.DECODE_FRAME_HEAD_END         = 'DF30'
const.DECODE_FRAME_BODY_BEGIN       = 'DF40'
const.DECODE_FRAME_BODY_END         = 'DF50'
const.DECODE_FRAME_TAIL_BEGIN       = 'DF60'
const.DECODE_FRAME_TAIL_END         = 'DF70'
const.DECODE_FRAME_END              = 'DF80'

const.DECODE_READER_BEGIN           = 'DR10'
const.DECODE_READER_END             = 'DR20'


const.DECODE_ZIGBEE_BEGIN           = 'DZ10'
const.DECODE_ZIGBEE_END             = 'DZ20'

# 编码进度
const.ENCODE_FRAME_BEGIN            = 'EF10'
const.ENCODE_FRAME_HEAD_BEGIN       = 'EF20'
const.ENCODE_FRAME_HEAD_END         = 'EF30'
const.ENCODE_FRAME_BODY_BEGIN       = 'EF40'
const.ENCODE_FRAME_BODY_END         = 'EF50'
const.ENCODE_FRAME_END              = 'EF60'

const.ENCODE_READER_BEGIN           = 'ET10'
const.ENCODE_READER_END             = 'ET20'


const.ENCODE_ZIGBEE_BEGIN           = 'EZ10'
const.ENCODE_ZIGBEE_END             = 'EZ20'


#  ----------常量定义----------

# 帧头 FH ( frame header )
const.FH_READER     = 'WS'                          # 读卡器帧格式
const.FH_ZIGBEE     = 'CO_'                         # Zigbee帧格式
const.FH_MAINFRAME  = 'XF'                          # 新版本Zigbee帧格式

# 帧类型
const.FRAME_TYPE_READER             = 0x01
const.FRAME_TYPE_ZIGBEE             = 0x02
const.FRAME_TYPE_ZIGBEE_V1          = 0x03

# 帧尾 FE (frame end)
const.FE_END                        = 'N'

# 标签数据类型标志
const.DATA_TYPE_NORMAL_CHK          = 0x2F          # 正常标签数据（A类），数据类型字段高四位为0x2，低四位补0xF
const.DATA_TYPE_EXCEPTION_CHK       = 0xFF          # 异常标签数据，数据类型字段高四位为0xF，低四位补0xF，用于或运算
const.DATA_TYPE_SET_PARAM_CHK       = 'SET_WTH'     # 设置读卡器参数
const.DATA_TYPE_READ_PARAM_CHK      = 'SET_RED'     # 读取读卡器参数
const.DATA_TYPE_RELAY_CTRL_CHK      = 'SET_RES'     # 继电器控制
const.DATA_TYPE_MSG_PASS_THROUGH    = 'SET_UAT'     # 继电器控制
const.DATA_TYPE_MSG_SENSOR_DATA_CHK = 0xB0          # 采集传感器器数据包
const.DATA_TYPE_MSG_SUBNET_PARAM_CHK       = 0xC0   # 中继与子网网关参数数据包
const.DATA_TYPE_MSG_SUBNET_CO_CHK   = 0xE0          # 中继与子网网关联动功能

# 标签组数，数据类型字段低四位，高四位补0x0，通过与运算获得低四位，通过或运算获得高四位
const.DATA_TYPE_TAG_NUM_OPER        = 0x0F

# 标签数据类型命令字
const.TAG_DATA_TYPE_NORMAL          = 0x01          # 正常标签数据（A类），数据类型字段高四位为0x2，低四位补0xF
const.TAG_DATA_TYPE_EXCEPTION       = 0x02          # 异常标签数据，数据类型字段高四位为0xF，低四位补0xF，用于或运算
const.TAG_DATA_TYPE_SET_PARAM       = 0x03          # 设置读卡器参数
const.TAG_DATA_TYPE_READ_PARAM      = 0x04          # 读取读卡器参数
const.TAG_DATA_TYPE_RELAY_CTRL      = 0x05          # 继电器控制

const.TAG_DATA_TYPE_SENSOR_DATA     = 0x06          # 采集传感器器数据包
const.TAG_DATA_TYPE_SUBNET_PARAM    = 0x07          # 中继与子网网关参数数据包
const.TAG_DATA_TYPE_SUBNET_COOP     = 0x08          # 中继与子网网关联动功能

# 起始时间字段
const.TAG_FIRST_TAG_TIME_COUNT_LEN  = 1             # 起始时间字段长度
const.TAG_FIRST_TAG_TIME_UINIT      = 0.5           # 第一组的超始时间 *0.5s

# 标签内容
const.TAG_CONT_TOTAL_LENGTH         = 20            # 单个标签内容总长度
const.TAG_CONT_SERIAL_LENGTH        = 3             # 序列号[标签物理地址]字段长度
const.TAG_CONT_COLLECT_FREQ_LENGTH  = 1             # 采集频率字段长度
const.TAG_CONT_TAG_TYPE_LENGTH      = 1             # 标签类型字段长度
const.TAG_CONT_SENSOR_MAX_NUM       = 4             # 单个标签支持的传感器最大数量
const.TAG_CONT_SENSOR_TYPE_LENGTH   = 1             # 传感器种类字段长度
const.TAG_CONT_SERSOR_DATA_LENGTH   = 2             # 传感器数据区字段长度
const.TAG_CONT_BATTERY_LEVEL_LENGTH = 1             # 电池电量[0.1v为单位]字段长度
const.TAG_CONT_RSSI_LENGTH          = 1             # RSSI字段长度
const.TAG_CONT_BACKUP_LENGTH        = 1             # 备用字段长度

# 读卡器物理地址
const.TAG_CONT_READER_ADDR_LENGTH   = 3

# 读卡器状态
const.TAG_CONT_READER_STATUS_LENGTH = 1

# 备用
const.TAG_CONT_BACKUP_BYTES_LENGTH  = 1

# 校验碼
const.TAG_CONT_CHECK_CODE_LENGTH    = 1

# 数据监控报警上下限
const.TAG_CONT_TEMP_UP_ALARM_LENGTH             = 2
const.TAG_CONT_TEMP_DOWN_ALARM_LENGTH           = 2
const.TAG_CONT_HUMIDITY_UP_ALARM_LENGTH         = 1
const.TAG_CONT_HUMIDITY_DOWN_ALARM_LENGTH       = 1

# 异常标签数据区字段长度定义
const.TAG_CONT_EXCEPTION_TYPE_LENGTH            = 1
const.TAG_CONT_EXCEPTION_BACKUP_BYTES_LENGTH    = 25

# 自动控制模式
const.TAG_CONT_AUTOCTRL_MODE_LENGTH             = 1

# 报警模式
const.TAG_CONT_ALARM_MODE_LENGTH                = 1

# 继电器控制寄存器
const.TAG_CONT_RELAY_MEMORY_LENGTH              = 3

"""
数据计算
字节最高位表示符号位， 0-正， 1-负
"""
const.NUMBER_BYTE_SIGN_BIT              = 0b10000000
const.NUMBER_BYTE_NEGATIVE_SIGN         = 0x8000

"""
设备状态
位0: 温度设备
位1: 湿度设备
位2: --
位3: -- 上面位：1 -> 打开设备 0 -> 关闭设备
位4-7: 控制模式
    0x1: 加热除湿 [默认]
    0x2: 加热加湿
    0x4: 降热除湿
    0x8: 降热加湿
    0xf: 禁用
"""
const.DEVICE_STATUS_TEMP                = 0b10000000
const.DEVICE_STATUS_HUMIDITY            = 0b01000000
const.DEVICE_STATUS_CTRL_MODE           = 0x0F      # 通过与运算获取控制模式

"""
继电器状态字
位7~0: 代表继电器7~0
"""
const.DEVICE_RELAY_NO_0                 = 0b10000000
const.DEVICE_RELAY_NO_1                 = 0b01000000
const.DEVICE_RELAY_NO_2                 = 0b00100000
const.DEVICE_RELAY_NO_3                 = 0b00010000
const.DEVICE_RELAY_NO_4                 = 0b00001000
const.DEVICE_RELAY_NO_5                 = 0b00000100
const.DEVICE_RELAY_NO_6                 = 0b00000010
const.DEVICE_RELAY_NO_7                 = 0b00000001

"""
继电器控制寄存器
    第 1 字节:继电器控制字
    第 2-3 字节:继电器延时时间; 单位:0.5s
"""
const.DEVICE_RELAY_CMD_LENGTH           = 1
const.DEVICE_RELAY_DELAY_TIME_LENGTH    = 2

"""
异常种类
    位 0: 传感器 1超上限
    位 1: 传感器 1低于下限
    位 2: 传感器 2超上限
    位 3: 传感器 2低于下限
    位 4: 传感器 3超上限
    位 5: 传感器 3低于下限
    位 6: 传感器 4超上限
    位 7: 传感器 4低于下限
与运算
"""
const.SENSOR_NO_1_EXCEPTION_UP          = 0b10000000
const.SENSOR_NO_1_EXCEPTION_DOWN        = 0b01000000
const.SENSOR_NO_2_EXCEPTION_UP          = 0b00100000
const.SENSOR_NO_2_EXCEPTION_DOWN        = 0b00010000
const.SENSOR_NO_3_EXCEPTION_UP          = 0b00001000
const.SENSOR_NO_3_EXCEPTION_DOWN        = 0b00000100
const.SENSOR_NO_4_EXCEPTION_UP          = 0b00000010
const.SENSOR_NO_4_EXCEPTION_DOWN        = 0b00000001

const.EXCEPTION_NO                      = 0x00
const.EXCEPTION_UP                      = 0x01
const.EXCEPTION_DOWN                    = 0x02

# 消息类型定义
const.MESSAGE_TYPE_NORMAL               = 0x01
const.MESSAGE_TYPE_EXCEPTION            = 0x02
const.MESSAGE_TYPE_SET_PARAM            = 0x03
const.MESSAGE_TYPE_READ_PARAM           = 0x04
const.MESSAGE_TYPE_RELAY_CTRL           = 0x05
const.MESSAGE_TYPE_MSG_PASS_THROUGH     = 0x06


"""
标签类型
    代码    | 标签类型                   ｜ 备注
    0x01    A 型人员快速定位专用
    0x02    双温湿度标签                  两组温湿度
    0x03    粮仓温度标签                  16 组温度
    0x04    环境监测                      一组温湿度 +  一组光照度
    0x05    土壤监测 1                    一组土壤水分 + 一组土壤温度
    0x06    CO2                           1组co2
    0x07    土壤监测 2                    土壤水分 + 土壤温湿度
    0x08    环境检测 2                    1组温度 ＋ 1组湿度 ＋ 1组光照度
    0x10    土壤水分监测                  4 只土壤水分传感器
    0x80    烟草综合标签 1[测温杆专用]    采集传感器一样,只是种类做区分。 已方便用户在用途上区分
    0x81    烟草综合标签 2[环境专用]      采集传感器一样,只是种类做区分。 已方便用户在用途上区分
"""
const.TAG_TYPE_PERSONNEL_LOCATION       = 0x01
const.TAG_TYPE_DOUBLE_TEMP_HUMIDIY      = 0x02
const.TAG_TYPE_GRANARY_TEMP             = 0x03
const.TAG_TYPE_ENV_MONITOR              = 0x04
const.TAG_TYPE_SOIL_MONITOR_1           = 0x05
const.TAG_TYPE_CO2_MONITOR              = 0x06
const.TAG_TYPE_SOIL_MONITOR_2           = 0x07
const.TAG_TYPE_SOIL_MOISTURE            = 0x10
const.TAG_TYPE_TOBACCO_SYNTHESIS_1      = 0x80
const.TAG_TYPE_TOBACCO_SYNTHESIS_2      = 0x81

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
const.ZNET_DEVICE_TYPE_SENSOR_NONE           = 0x00      # 空数据
const.ZNET_DEVICE_TYPE_SENSOR_TA             = 0x01      # Temperature Ambient 环境温度
const.ZNET_DEVICE_TYPE_SENSOR_AH             = 0x02      # ambient humidity 环境湿度
const.ZNET_DEVICE_TYPE_SENSOR_CO2            = 0X03      # CO2传感器
const.ZNET_DEVICE_TYPE_SENSOR_SH             = 0x04      # soil humidity 土壤水分
const.ZNET_DEVICE_TYPE_SENSOR_LU             = 0x05      # illuminance 光照度 luminous flux 光通量
const.ZNET_DEVICE_TYPE_SENSOR_ST             = 0x06      # soil temperature 土壤温度 简称“土温”
const.ZNET_DEVICE_TYPE_SENSOR_SMO            = 0x07      # Soil Moisture 土壤湿度
const.ZNET_DEVICE_TYPE_SENSOR_T              = 0xa1      # temperature 温度
const.ZNET_DEVICE_TYPE_SENSOR_H              = 0xa2      # humidity 湿度
const.ZNET_DEVICE_TYPE_ACCELERATION_X        = 0xa3      # Acceleration 加速度 X轴
const.ZNET_DEVICE_TYPE_ACCELERATION_Y        = 0xa4      # Acceleration 加速度 Y轴
const.ZNET_DEVICE_TYPE_ACCELERATION_Z        = 0xa5      # Acceleration 加速度 Z轴
const.ZNET_DEVICE_TYPE_INFRARED              = 0xa6      # Infrared Sensor 人体红外
const.ZNET_DEVICE_TYPE_PROXIMITY_SWITCH      = 0xa7      # Proximity switch 接近开关
const.ZNET_DEVICE_TYPE_SMOKE_TRANSDUCER      = 0xa8      # Smoke Transducer 烟雾传感器

# 控制器类型
const.ZNET_DEVICE_TYPE_DELAY_CTRL            = 0xf1      # relay 继电器

"""
采集频率
    0x00: 表示 10s
    0x01: 表示 1 分钟
    0x02: 表示 10 分钟
    0x03: 表示 30 分钟
    0x04: 表示 1 小时
"""
const.READER_COLLETECT_FREQ_TYPE_10S    = 0x00
const.READER_COLLETECT_FREQ_TYPE_1M     = 0x01
const.READER_COLLETECT_FREQ_TYPE_10M    = 0x02
const.READER_COLLETECT_FREQ_TYPE_30M    = 0x03
const.READER_COLLETECT_FREQ_TYPE_1H     = 0x04

"""
设备状态
位0: 温度设备
位1: 湿度设备
位2: --
位3: -- 上面位：1 -> 打开设备 0 -> 关闭设备
位4-7: 控制模式
    0x1: 加热除湿 [默认]
    0x2: 加热加湿
    0x4: 降热除湿
    0x8: 降热加湿
    0xf: 禁用

通过与运算获得具体模式
"""
const.DEVICE_STATUS_CTRL_MODE_UHDM      = 0x01      # UHDM:UP HEAT DOWN HUMIDITY
const.DEVICE_STATUS_CTRL_MODE_UHUM      = 0x02      # UHUM:UP HEAT UP HUMIDITY
const.DEVICE_STATUS_CTRL_MODE_DHDM      = 0x04      # DHDM:DOWN HEAT DOWN HUMIDITY
const.DEVICE_STATUS_CTRL_MODE_DHUM      = 0x08      # DHUM:DOWN HEAT UP HUMIDITY
const.DEVICE_STATUS_CTRL_MODE_FORBID    = 0x0F      # FORBIDDEN 禁用

"""
报警模式
    0x01: 启动
    0xff: 禁用
"""
const.DEVICE_ALARM_MODE_OPEN            = 0x01
const.DEVICE_ALARM_MODE_SHUTDOWN        = 0xFF

"""
继电器状态字
用位来表示 位7~0: 代表继电器7~0
0: 关 1: 开
"""
const.DEVICE_RELAY_STATUS_NONE          = 0xff
const.DEVICE_RELAY_STATUS_OPEN          = 0x01
const.DEVICE_RELAY_STATUS_CLOSE         = 0x00

"""
继电器控制字
    0x1a: 常开
    0x2b: ’开启后定时关断’模式
    其它: 关
"""
const.DEVICE_RELAY_CMD_NORMALLY_OPEN    = 0x1a
const.DEVICE_RELAY_CMD_OPEN_DELAY_CLOSE = 0x2b
# 当控制字为其他时，则处理成0xff
const.DEVICE_RELAY_CMD_CLOSE            = 0xff

# 节点类型
const.NODE_TYPE_NODE                    = 0x01              # 普通节点类型
const.NODE_TYPE_ROUTER                  = 0x02              # 中继器节点，可以挂载设备，同时可以进行一些处理
const.NODE_TYPE_COORDINATOR             = 0x03              # 协调器，一般不挂载设备


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
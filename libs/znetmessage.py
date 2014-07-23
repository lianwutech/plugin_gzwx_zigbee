#!/usr/bin/env python
# -*- coding:utf-8 -*-

""":mod:`znetmessage` -- 消息类封装
"""

import znetmessageengine as MsgEngine
import logging

# 初始化日志
interface_logger = logging.getLogger('interface')


def get_frame_header_pos(data_buff):
    """
    查找帧头的位置
    :param data_buff:
    :return: <0 :未找到，>=0 位置
    """
    data_buff_len = len(data_buff)
    header_pos = -1
    cur_pos = 0
    if data_buff_len > 0:
        while cur_pos < data_buff_len:
            try:
                # 确认W的位置
                w_pos = data_buff[cur_pos:].index('W') + cur_pos
                # 确认S位置
                if data_buff[w_pos + 1] == 'S':
                    # 找到位置
                    header_pos = w_pos
                    break
                else:
                    # 进入下一个循环
                    cur_pos = w_pos + 1
            except Exception, e:
                break
    return header_pos


def get_package_len(data_buff):
    """
    获取包长度
    :param data_buff:
    :return:
    """
    msg_engine = MsgEngine.MessageEngine()
    if len(data_buff) > 3:
        (data_pack_length,) = msg_engine.unpack_from_bin("!B", data_buff, 2)
        return data_pack_length + 4
    else:
        return 0


class GZXXZigbeeNetMessage(object):
    """
    消息帧：
        帧头(2 字节)
        数据包长度
        数据包
        帧尾(一个字节)
    帧内容解析到msg字典中，帧数据内容解析到msg['tag_data']中。
    """
    def __init__(self):
        self.msg_engine = MsgEngine.MessageEngine()
        self.msg = dict()
        self.msg['frame_type']          = 0
        self.msg['data_packet_len']     = 0
        self.msg['data_packet']         = None
        self.msg['frame_tail']          = None

        # 存放二进制帧数据BUF
        self.msg['frame_buff']          = None
        # 存放二进制帧数据长度
        self.msg['frame_buff_len']      = 0

        # 数据内容类型
        self.msg['tag_data_type']       = 0

        # 存放数据内容的字典
        self.msg['tag_data']            = {}

        # 存放标签数据的buff
        self.msg['frame_data_buff']       = None

        # 解包状态
        self.msg['DF_STAT']             = None

    def __del__(self):
        del self.msg

    def __repr__(self):
        str_print = ''
        if self.msg['frame_type'] == self.msg_engine.msg_def.const.FRAME_TYPE_READER:
            if self.msg['tag_data_type'] == self.msg_engine.msg_def.const.TAG_DATA_TYPE_NORMAL:
                str_print += "frame_type: %d \n" % self.msg['frame_type']
                str_print += "data_packet_len: %d \n" % self.msg['data_packet_len']
                str_print += "tag_data_type: %d \n" % self.msg['tag_data_type']
                str_print += "tag_data.tag_num: %d \n" % self.msg['tag_data']['tag_num']
                for i in range(len(self.msg['tag_data']['data_list'])):
                    str_print += "tag_data_%d \n" % i
                    tag_data_item = self.msg['tag_data']['data_list'][i]
                    str_print += "tag_data_%d.tag_type: %d \n" % (i, tag_data_item['tag_type'])
                    str_print += "tag_data_%d.tag_addr: %s \n" % (i, tag_data_item['tag_addr'])
                    str_print += "tag_data_%d.collect_freq: %d \n" % (i, tag_data_item['collect_freq'])
                    for j in range(4):
                        sensor_data = tag_data_item["sensors_data_list"][j]
                        str_print += "tag_data_%d.sensor_data_%d \n" % (i, j)
                        str_print += "tag_data_%d.sensor_data_%d.sensor_type: %d \n" % (i, j, sensor_data["sensor_type"])
                        str_print += "tag_data_%d.sensor_data_%d.sensor_data: %s \n" % (i, j, sensor_data["sensor_data"])
                    str_print += "tag_data_%d.battery_level: %d \n" % (i, tag_data_item['battery_level'])
                    str_print += "tag_data_%d.rssi: %s \n" % (i, tag_data_item['rssi'])
                    str_print += "tag_data_%d.collect_freq: %d \n" % (i, tag_data_item['collect_freq'])

                str_print += "router_addr: %s \n" % self.msg['tag_data']['router_addr']
                str_print += "devices 1 status: %d \n" % self.msg['tag_data']['delay_status_list'][0]
                str_print += "devices 2 status: %d \n" % self.msg['tag_data']['delay_status_list'][1]
                str_print += "controll_mode: %s \n" % self.msg['tag_data']['controll_mode']

        return str_print

    def __str__(self):
        return self.__repr__()

    def __unpack_frame_struct(self, frame_buff):
        '''解码帧结构'''
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_FRAME_HEAD_BEGIN
        # 帧头2字节
        offset_ = 0
        (str_frame_header,) = self.msg_engine.unpack_from_bin("!2s", frame_buff, offset_)
        if str_frame_header == self.msg_engine.msg_def.const.FH_READER:
            self.msg['frame_type'] = self.msg_engine.msg_def.const.FRAME_TYPE_READER
        else:
            raise self.msg_engine.msg_err.MsgErr_InvalidFrameHeader, \
                "The Frame Header In Frame Head!\n \
                \tThe Real Header:[%s]\n " % str_frame_header

        # 数据包长度
        offset_ += 2
        (data_pack_length,) = self.msg_engine.unpack_from_bin("!B", frame_buff, offset_)
        self.msg['data_packet_len'] = data_pack_length
        real_data_pack_length = len(frame_buff) - 4      # 帧头＋数据包长度＋ 帧尾
        if real_data_pack_length > self.msg['data_packet_len']:
            except_msg = "The Frame length is error!\n \
                \tThe length is :[%d/%d]\n " % (real_data_pack_length, self.msg['data_packet_len'])
            raise self.msg_engine.msg_err.MsgErr_InvalidFrameLength(self.msg['data_packet_len'], real_data_pack_length, except_msg)

        elif real_data_pack_length < self.msg['data_packet_len']:
            raise self.msg_engine.msg_err.MsgErr_FrameNotIntegrity, \
                "The Frame is not integrity.!\n \
                \tThe length is :[%d/%d]\n " % (real_data_pack_length, self.msg['data_packet_len'])
        else:
            offset_ += 1
            self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_FRAME_HEAD_END

            # 帧尾 'N'
            self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_FRAME_TAIL_BEGIN
            (frame_end,) = self.msg_engine.unpack_from_bin("!s", frame_buff, real_data_pack_length + 3)
            if frame_end != self.msg_engine.msg_def.const.FE_END:
                raise self.msg_engine.msg_err.MsgErr_InvalidFrameTail, \
                    "The Tail Wrong! \n \
                    \t The Real Tail:[%s]" \
                    % (frame_end)
            self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_FRAME_TAIL_END
            return offset_


    def __unpack_frame_reader_normal(self, offset=1, frame_data_buff=None):
        """
        解析正常标签数据
        :param offset:
        :return:
        """
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_READER_BEGIN

        # 设置数据类型
        self.msg['tag_data_type'] = self.msg_engine.msg_def.const.TAG_DATA_TYPE_NORMAL

        # 标签组数
        offset_ = 0
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['tag_num'] = data_1_byte & 0x0000000F

        # 根据“标签组数”校验长度校验
        expect_data_length = 1 + 1 + 20 * self.msg['tag_data']['tag_num'] + 3 + 1 + 1 + 1 + 1
        if len(frame_data_buff) != expect_data_length:
            "如果长度校验不过，则上报异常"
            raise self.msg_engine.msg_err.MsgErr_InvalidTagDataLength, \
                "The Tag Data Length Wrong! \n \
                \tThe Real Data Length:[%d]\n \
                \tThe Expect Data Length In Frame:[%d]" \
                % (len(frame_data_buff), expect_data_length)

        # 初始化标签数据数组
        self.msg['tag_data']['data_list'] = []
        self.msg['tag_data']['delay_status_list'] = []

        # 起始时间
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['start_time'] = data_1_byte * self.msg_engine.msg_def.const.TAG_FIRST_TAG_TIME_UINIT

        # 标签内容解析
        for i in range(self.msg['tag_data']['tag_num']):
            tag_data_item = {}
            # 序列号 + 采集频率
            (data_4_byte, ) = self.msg_engine.unpack_from_bin("!I", frame_data_buff, offset_)
            offset_ += 4
            # 序列号［标签物理地址］,按照16进制字符串存储，编码的时候再转换回来
            tag_data_item['tag_addr'] = ("%08X" % data_4_byte)[0:6]
            # 采集频率
            tag_data_item['collect_freq'] = data_4_byte & 0x000000FF

            # 标签类型
            (data_1_byte, ) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
            # offset_不步进，方便后续传感器数据的处理
            # offset_ += 1
            tag_data_item['tag_type'] = data_1_byte

            # 初始化传感器数据列表
            tag_data_item['sensors_data_list'] = []

            for j in range(0, 4):
                # 传感器种类 + 传感器数据区(2个字节)
                (data_4_byte, ) = self.msg_engine.unpack_from_bin("!I", frame_data_buff, offset_)
                sensor_data = dict()
                sensor_data['sensor_type'] = (data_4_byte & 0x00FF0000) >> 16
                sensor_data_buff = data_4_byte & 0x0000FFFF
                if sensor_data_buff == 0xffff or sensor_data['sensor_type'] == 0xff or sensor_data['sensor_type'] == 0x00:
                    sensor_data["sensor_type"] = self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_NONE
                    sensor_data['sensor_data'] = str(0xffff)
                else:
                    # 数据处理
                    if sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_TA:
                        '环境温度 0x01  低位在前,高位在后; 单位:0.1 度 最高位:符号位 0 正,1 负'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SENSOR_TA
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2int_hex(sensor_data_buff) * 0.1)
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_AH:
                        '环境湿度 0x02 第一字节有效:精度 1%; 第二字节备用'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SENSOR_AH
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2num1byte_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_CO2:
                        'CO2 0x03 低位在前,高位在后'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SENSOR_CO2
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2num_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_SH:
                        '土壤水分 0x04 低位在前,高位在后; 单位:0.1 度'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SENSOR_SH
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2int_hex(sensor_data_buff) * 0.1)
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_LU:
                        '光照度 0x05 低位在前,高位在后'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SENSOR_LU
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2num_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_ST:
                        '土壤温度 0x06 低位在前,高位在后; 单位:0.1度; 最高位:符号位 0 正,1 负。'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SENSOR_ST
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2int_hex(sensor_data_buff) * 0.1)
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_SMO:
                        '土壤湿度 0x07 第一字节有效:精度 1%; 第二字节备用'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SENSOR_SMO
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2num1byte_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_T:
                        '温度 0xa1 低位在前,高位在后; 单位:0.1 度 最高位:符号位 0 正,1 负'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SENSOR_TA
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2int_hex(sensor_data_buff) * 0.1)
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_H:
                        '湿度 0xa2 第一字节有效:精度 1%; 第二字节备用'
                        sensor_data['sensor_type'] = const.ZNET_DEVICE_TYPE_SENSOR_AH
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2num1byte_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_ACCELERATION_X:
                        '加速度 0xa3 X轴2字节：低位在前，高位在后;'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_ACCELERATION_X
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2int_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_ACCELERATION_Y:
                        '加速度 0xa3 Y轴2字节：低位在前，高位在后;'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_ACCELERATION_Y
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2int_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_ACCELERATION_Z:
                        '加速度 0xa3 Z轴2字节：低位在前，高位在后'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_ACCELERATION_Z
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2int_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_INFRARED:
                        '人体红外	0xa4	0x1: 监测到有效信号 0x2: 未测到'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_INFRARED
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2num1byte_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_PROXIMITY_SWITCH:
                        '接近开关	0xa5	0x1: 监测到有效信号 0x2: 未测到'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_PROXIMITY_SWITCH
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2num1byte_hex(sensor_data_buff))
                    elif sensor_data['sensor_type'] == self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SMOKE_TRANSDUCER:
                        '烟雾	0xa6;第1字节： 0x1: 监测到有效信号 0x2: 未测到 其它：无效 第2字节： 脉宽周期，单位mS'
                        sensor_data['sensor_type'] = const.DEVICE_TYPE_SMOKE_TRANSDUCER
                        sensor_data['sensor_data'] = str(self.msg_engine.bin2num1byte_hex(sensor_data_buff))
                    else:
                        interface_logger.error("错误的传感器类型：%d" % sensor_data['sensor_type'])
                        sensor_data["sensor_type"] = self.msg_engine.msg_def.const.ZNET_DEVICE_TYPE_SENSOR_NONE
                        sensor_data['sensor_data'] = str(0xffff)

                tag_data_item['sensors_data_list'].append(sensor_data)

                offset_ += 3

            # 补进一个字节
            offset_ += 1

            # 电池容量
            (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
            tag_data_item['battery_level'] = data_1_byte
            offset_ += 1

            # RSSI
            (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
            tag_data_item['rssi'] = data_1_byte
            offset_ += 1

            # 备用字段
            offset_ += 1

            # 追加到数据列表
            self.msg['tag_data']['data_list'].append(tag_data_item)

        # 读卡器物理地址 3字节
        (data_4_byte, ) = self.msg_engine.unpack_from_bin("!I", frame_data_buff, offset_)
        offset_ += 3
        self.msg['tag_data']['router_addr'] = ("%08X" % data_4_byte)[0:6]

        # 中继设备状态
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['delay_status_list'].append(data_1_byte & 0b1)
        self.msg['tag_data']['delay_status_list'].append((data_1_byte & 0b1 << 1) >> 1)

        # 控制模式
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['controll_mode'] = data_1_byte

        # 控制数据模式
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['data_controll_mode'] = data_1_byte

        # 和校验
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['check_code'] = data_1_byte
        # 进行校验－以后增加

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_READER_END

    def __unpack_frame_reader_get_param_resp(self, offset = 7, frame_data_buff = None):
        """
        解析读取读卡器参数
        :param offset:
        :return:
        """
        offset_ = offset
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_READER_BEGIN

        # 数据类型
        self.msg['tag_data_type'] = self.msg_engine.msg_def.const.MESSAGE_TYPE_READ_PARAM

        # 序列号(读卡器地址) 3字节
        (data_4_byte, ) = self.msg_engine.unpack_from_bin("!I", frame_data_buff, offset_)
        offset_ += 3
        # 序列号［标签物理地址］,按照16进制字符串存储，编码的时候再转换回来
        self.msg['tag_data']['tag_addr'] = ("%08X" % data_4_byte)[0:6]

        # 控制状态切换 1个字节
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['control_mode_switch'] = data_1_byte

        # 取温度报警设定数据
        (data_4_byte, ) = self.msg_engine.unpack_from_bin("!I", frame_data_buff, offset_)
        offset_ += 4
        # 温度报警上限 2个字节
        self.msg['tag_data']['tmp_alert_up'] = self.msg_engine.bin2int_hex(data_4_byte >> 16) * 0.1
        # 温度报警下限 2个字节
        self.msg['tag_data']['tmp_alert_down'] = self.msg_engine.bin2int_hex(data_4_byte & 0x00FF) * 0.1

        # 取湿度报警设定数据 + 自动控制模式 + 报警模式
        (data_4_byte, ) = self.msg_engine.unpack_from_bin("!I", frame_data_buff, offset_)
        offset_ += 4
        # 湿度报警上限 1个字节
        self.msg['tag_data']['humidity_alert_up'] = (data_4_byte & 0xFF000000) >> 24
        # 湿度报警下限 1个字节
        self.msg['tag_data']['humidity_alert_down'] = (data_4_byte & 0x00FF0000) >> 16
        # 控制模式 1个字节
        self.msg['tag_data']['controll_mode'] = (data_4_byte & 0x0000FF00) >> 8
        # 控制数据模式 1个字节
        self.msg['tag_data']['data_controll_mode'] = (data_4_byte & 0x000000FF)

        # 报警模式 1个字节
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['alert_mode'] = data_1_byte

        # 监测异常传感器类型 1个字节
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['monitor_exception_sensor_type'] = data_1_byte

        # 继电器状态字 1个字节
        (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        offset_ += 1
        self.msg['tag_data']['delay_status_list'] = []
        for i in range(0, 2):       # 当前版本的设备只使用前两个状态位
            self.msg['tag_data']['delay_status_list'].append((data_1_byte & (0b1 << i)) >> i)

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_READER_END


    # def __unpack_frame_reader_message_passthrough(self, offset = 7, frame_data_buff = None):
    #     """
    #     解析继电器控制指令
    #     :param offset:
    #     :return:
    #     """
    #     offset_ = offset
    #     self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_READER_BEGIN
    #
    #     # 数据类型
    #     self.msg['tag_data_type'] = self.msg_engine.msg_def.const.MESSAGE_TYPE_MSG_PASS_THROUGH
    #
    #     # 序列号(读卡器地址) 3字节
    #     (data_4_byte, ) = self.msg_engine.unpack_from_bin("!I", frame_data_buff, offset_)
    #     offset_ += 3
    #     # 序列号［标签物理地址］,按照16进制字符串存储，编码的时候再转换回来
    #     self.msg['tag_data']['tag_addr'] =  ("%08X" % data_4_byte)[0:6]
    #     self.msg['tag_data']['delay_ctrl_reg'] = []
    #
    #     # 输出端口
    #     (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
    #     offset_ += 1
    #     self.msg['tag_data']['output_port'] = data_1_byte
    #
    #     # 透传内容长度
    #     (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
    #     offset_ += 1
    #     self.msg['tag_data']['message_length'] = data_1_byte
    #     self.msg['tag_data']['message'] = []
    #
    #     # 透传内容
    #     for i in range(0, self.msg['tag_data']['message_length']):
    #         (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
    #         offset_ += 1
    #         self.msg['tag_data']['message'].append(data_1_byte)
    #
    #     # 和校验
    #     (data_1_byte,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
    #     offset_ += 1
    #     self.msg['tag_data']['check_code'] = data_1_byte
    #     # 进行校验－以后增加
    #
    #     self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_READER_END

    def __unpack_frame_reader(self, frame_data_buff = None):
        """
        解析读卡器通讯协议
        :param :
        :return:
        """
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_READER_BEGIN

        # 解析读卡器帧数据中的数据类型
        # 顺序为：正常标签数据、异常标签数据、设置读卡器参数、读取读卡器参数、继电器控制
        offset_ = 0
        (tag_type_and_tag_num,) = self.msg_engine.unpack_from_bin("!B", frame_data_buff, offset_)
        (str_tag_type,) = self.msg_engine.unpack_from_bin("!7s", frame_data_buff, offset_)
        tag_data_type = (tag_type_and_tag_num & 0x000000F0) | 0x0F
        if tag_data_type == self.msg_engine.msg_def.const.DATA_TYPE_NORMAL_CHK:
            # 正常标签数据
            offset_ += 1
            self.__unpack_frame_reader_normal(offset_, frame_data_buff)
        else:
            if str_tag_type == self.msg_engine.msg_def.const.DATA_TYPE_READ_PARAM_CHK:
                # 读取读卡器参数
                offset_ += 7
                self.__unpack_frame_reader_get_param_resp(offset_, frame_data_buff)
            else:
                # 错误标签数据类型指令
                raise self.msg_engine.msg_err.MsgDataErr_InvalidDataRange, \
                    "The tag data type is error!\n \
                    \tThe tag data type: [%d]" % tag_data_type

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_READER_END
        pass

    def unpack(self, frame_buf):
        """
        解包Frame消息，返回解包后的一个字典
        首先解析包头，再解析具体包体
        解码BUF，输出解码后的实例
        """
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_FRAME_BEGIN
        self.msg['frame_buff'] = frame_buf

        # 解析帧结构
        offset = self.__unpack_frame_struct(self.msg['frame_buff'])
        # 如果数据异常，通过异常的方式反馈给调用者

        # 提取标签数据
        self.msg['frame_data_buff'] = self.msg['frame_buff'][offset: offset + self.msg['data_packet_len']]
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_FRAME_BODY_BEGIN
        # 根据帧头做相应的处理
        if self.msg['frame_type'] == self.msg_engine.msg_def.const.FRAME_TYPE_READER:
            # 解析读卡器通讯协议
            self.__unpack_frame_reader(self.msg['frame_data_buff'])
        else:
            # 错误帧类型指令
            raise self.msg_engine.msg_err.MsgDataErr_InvalidDataRange, \
                "The frame type is error!\n \
                \tThe frame type: [%d]" % self.msg['frame_type']

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_FRAME_BODY_END
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.DECODE_FRAME_END

    def __pack_frame_reader_get_param_req(self):
        """读取读卡器参数帧打包"""
        interface_logger.debug("读取读卡器参数帧打包")

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_FRAME_BODY_BEGIN
        pack_buff = ""

        # 帧头
        pack_buff += self.msg_engine.pack_data2bin("!2s", self.msg_engine.msg_def.const.FH_READER)

        # 帧长度
        pack_length = 10
        pack_buff += self.msg_engine.pack_data2bin("!B", (pack_length & 0x00FF))

        # 数据类型
        pack_buff += self.msg_engine.pack_data2bin("!7s", self.msg_engine.msg_def.const.DATA_TYPE_READ_PARAM_CHK)

        # 读卡器地址3字节，当前只支持广播模式，即读卡器地址为0xffffff
        pack_buff += self.msg_engine.ascii2bin_hex("ffffff")

        # 帧尾
        pack_buff += self.msg_engine.pack_data2bin("!1s", self.msg_engine.msg_def.const.FE_END)

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_FRAME_BODY_END
        interface_logger.debug("__pack_frame_reader_get_param_req打包内容:%s" % pack_buff.encode("hex"))
        return pack_buff

    def __pack_frame_reader_relay_ctrl(self):
        """继电器节点控制帧打包"""
        interface_logger.debug("继电器节点控制帧打包")

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_FRAME_BODY_BEGIN
        pack_buff = ""

        # 帧头
        pack_buff += self.msg_engine.pack_data2bin("!2s", self.msg_engine.msg_def.const.FH_READER)

        # 帧长度
        pack_length = 36
        pack_buff += self.msg_engine.pack_data2bin("!B", (pack_length & 0x00FF))

        # 数据类型
        pack_buff += self.msg_engine.pack_data2bin("!7s", self.msg_engine.msg_def.const.DATA_TYPE_RELAY_CTRL_CHK)

        # 读卡器地址3字节
        interface_logger.debug("tag_addr编码结果: %s" %
                               self.msg_engine.ascii2bin_hex(self.msg['tag_data']['tag_addr']).encode("hex"))
        pack_buff += self.msg_engine.ascii2bin_hex(self.msg['tag_data']['tag_addr'])

        # 手动控制／自动控制 1个字节
        pack_buff += self.msg_engine.pack_data2bin("!B", (self.msg['tag_data']['control_mode_switch'] & 0x00FF))

        # 8个继电器控制寄存器，每个继电器3个字节
        for i in range(0, len(self.msg['tag_data']['delay_ctrl_reg'])):
            # 继电器控制寄存器 3字节
            # 控制字 1个字节 0x1a 常开 ；0x2b 延时模式；其他 关闭
            # 继电器延时时间 2个字节 单位0.5S
            pack_buff += self.msg_engine.pack_data2bin(
                "!BH",
                (self.msg['tag_data']['delay_ctrl_reg'][i]['ctrl_cmd'] & 0x00FF),
                (self.msg['tag_data']['delay_ctrl_reg'][i]['ctrl_delay_time'] & 0xFFFF))

        # 和校验
        pack_buff += self.msg_engine.pack_data2bin("!B", 0x00)

        # 帧尾
        pack_buff += self.msg_engine.pack_data2bin("!1s", self.msg_engine.msg_def.const.FE_END)

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_FRAME_BODY_END
        interface_logger.debug("__pack_frame_reader_relay_ctrl打包内容:%s" % pack_buff.encode("hex"))
        return pack_buff
        #
    # def __pack_frame_reader_message_passthrough(self):
    #     """消息透传打包"""
    #
    #     self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_FRAME_BODY_BEGIN
    #     pack_buff = ""
    #
    #     # 帧头
    #     pack_buff += self.msg_engine.pack_data2bin("!2s", self.msg_engine.const.FH_READER)
    #
    #     # 帧长度
    #     pack_length = 2 + 1 + 5 + self.msg['tag_data']['message_length'] + 1
    #     pack_buff += self.msg_engine.pack_data2bin("!B", (pack_length & 0x00FF))
    #
    #     # 数据类型
    #     pack_buff += self.msg_engine.pack_data2bin("!7s", self.msg_engine.const.DATA_TYPE_MSG_PASS_THROUGH)
    #
    #     # 读卡器地址3字节
    #     pack_buff += self.msg_engine.ascii2bin_hex(self.msg['tag_data']['tag_addr'])
    #
    #     # 输出端口 1个字节
    #     pack_buff += self.msg_engine.pack_data2bin("!B", (self.msg['tag_data']['output_port'] & 0x00FF))
    #
    #     # 透传内容长度 1个字节
    #     pack_buff += self.msg_engine.pack_data2bin("!B", (self.msg['tag_data']['message_length'] & 0x00FF))
    #
    #     # 透传内容
    #     for i in range(0, self.msg['tag_data']['message_length']):
    #         pack_buff += self.msg_engine.pack_data2bin("!B", (self.msg['tag_data']['message'][i] & 0x00FF))
    #
    #     # 帧尾
    #     pack_buff += self.msg_engine.pack_data2bin("!1s", self.msg_engine.const.FE_END)
    #
    #     self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_FRAME_BODY_END
    #     return pack_buff


    def __pack_frame_reader(self):
        """读卡器消息帧打包"""
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_READER_BEGIN

        # 根据消息类型组装标签数据
        if self.msg['tag_data_type'] == self.msg_engine.msg_def.const.MESSAGE_TYPE_READ_PARAM:
            # 读取参数请求
            interface_logger.debug("__pack_frame_reader调用函数__pack_frame_reader_get_param_req")
            self.msg['frame_data_buff'] = self.__pack_frame_reader_get_param_req()
            pass
        elif self.msg['tag_data_type'] == self.msg_engine.msg_def.const.MESSAGE_TYPE_RELAY_CTRL:
            # 继电器节点控制
            interface_logger.debug("__pack_frame_reader调用函数__pack_frame_reader_relay_ctrl")
            self.msg['frame_data_buff'] = self.__pack_frame_reader_relay_ctrl()
            pass
        else:
            # 错误指令
            # 错误标签数据类型
            raise self.msg_engine.msg_err.MsgDataErr_InvalidDataRange, \
                "The tag data type is error!\n \
                \tThe tag data type: [%d]" % self.msg['tag_data_type']

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_READER_END
        return self.msg['frame_buff']

    def pack(self):
        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_FRAME_BEGIN

        # 根据帧类型组装帧
        if self.msg['frame_type'] == self.msg_engine.msg_def.const.FH_READER:
            # 读卡器消息帧
            interface_logger.debug("pack调用函数__pack_frame_reader")
            self.__pack_frame_reader()
            pass
        else:
            # 错误帧类型
            raise self.msg_engine.msg_err.MsgDataErr_InvalidDataRange, \
                "The frame type is error!\n \
                \tThe frame type: [%d]" % self.msg['frame_type']

        self.msg['decode_frame_status'] = self.msg_engine.msg_def.const.ENCODE_FRAME_END
        return self.msg['frame_buff']


#!/usr/bin/env python
# -*- coding:utf-8 -*-

""":mod:`znetmessageengine` -- 消息处理引擎
功能包括：
    1、串口设备管理
    2、消息编解码入口和消息内容处理
    3、zigbee网络管理
    4、数据上传
"""

from time import strftime, strptime, mktime, localtime
from codecs import getencoder, getdecoder
from struct import pack, unpack_from, calcsize
from binascii import b2a_hex, a2b_hex

import znetmessageerror as MSG_ERR
import znetmsgdefine as MSG_DEF


class MessageEngine(object):
    "协议解码、编码引擎"
    def __init__(self):
        '引擎初始化'
        self.msg_err = MSG_ERR
        self.msg_def = MSG_DEF

        self.TIMEFORMAT=self.msg_def.const.COMPACTTIMEFORMAT
        self.seconds_between_1900_and_1970 = ((70*365)+17)*86400

    def __del__(self):
        del self.msg_err
        del self.msg_def
        del self.TIMEFORMAT
        del self.seconds_between_1900_and_1970

    def NTPStamp2Time(self, stamp):
        '将NTP时间戳转换为年月日的时间格式'
        #stamp = float(repr(stamp))
        myUTCTime = stamp - self.seconds_between_1900_and_1970
        return strftime(self.TIMEFORMAT, localtime(myUTCTime))

    def UTCStamp2Time(self, stamp):
        '将UTC时间戳转换为年月日的时间格式'
        return strftime(self.TIMEFORMAT, localtime(stamp))

    def UTCStamp2ISOTime(self, stamp):
        '将UTC时间戳转换为年月日的时间格式'
        return strftime(self.dcc_def.const.ISOTIMEFORMAT, localtime(stamp))

    def Time2NTPStamp(self, time_str):
        '将年月日的时间格式转换为NTP时间戳,'
        # TIMEFORMAT = '2009-03-13 10:28:35'
        if len(time_str) == 19:
            myFormat = strptime(time_str, self.dcc_def.const.ISOTIMEFORMAT)
            outStamp = mktime(myFormat)
            outStamp = outStamp + self.seconds_between_1900_and_1970
            return outStamp
        # TIMEFORMAT = '20090313102835'
        elif len(time_str) == 14:
            myFormat = strptime(time_str, self.dcc_def.const.COMPACTTIMEFORMAT)
            outStamp = mktime(myFormat)
            outStamp = outStamp + self.seconds_between_1900_and_1970
            return outStamp
        else:
            raise MSG_ERR.MsgDataErr_InvalidInitParam, \
                "The Time Format Error:\nfmt=%s, input=%s" % (self.TIMEFORMAT, time_str)

    def Time2TUCStamp(self, time_str):
        '将年月日的时间格式转换为UTC时间戳'
        # TIMEFORMAT = '2009-03-13 10:28:35'
        if len(time_str) == 19:
            myFormat = strptime(time_str, self.dcc_def.const.ISOTIMEFORMAT)
            return mktime(myFormat)
        # TIMEFORMAT = '20090313102835'
        elif len(time_str) == 14:
            myFormat = strptime(time_str, self.dcc_def.const.COMPACTTIMEFORMAT)
            return mktime(myFormat)
        else:
            raise MSG_ERR.MsgDataErr_InvalidInitParam, \
                "The Time Format Error:\nfmt=%s, input=%s" % (self.TIMEFORMAT, time_str)

    def utf8encoder(self, nonu8str):
        '将unicode编码为UTF8格式'
        u8encoder = getencoder("utf_8")
        return u8encoder(nonu8str)[0]

    def utf8decoder(self, u8str):
        '将UTF8编码为unicode格式'
        u8decoder = getdecoder("utf_8")
        return u8decoder(u8str)[0]

    def pack_data2bin(self, fmt, *pack_data):
        '重载struct.pack函数'
        return pack(fmt, *pack_data)

    def unpack_from_bin(self, fmt, buf, offset=0):
        '重载struct.unpack_from函数'
        return unpack_from(fmt, buf, offset)

    def calc_pack_size(self, fmt):
        return calcsize(fmt)

    def bin2ascii_hex(self, bin_buf):
        '重载binascii.b2a_hex函数'
        return b2a_hex(bin_buf)

    def ascii2bin_hex(self, ascii_buf):
        '重载binascii.a2b_hex函数'
        return a2b_hex(ascii_buf)

    def bin2int_hex(self,data_2_byte):
        """
        2字节数据转换成整型，其中低位在前,高位在后; 最高位:符号位 0 正,1 负
        :param data_2_byte 使用整型存储的2字节数据:
        :return 结果数据:
        """
        data_value = ((data_2_byte & 0x0000FF00) >> 8) + ((data_2_byte & 0x000000FF) * 0x100)
        if data_value > 0x8000:
            data_value = (-1) * (data_value - 0x8000)

        return data_value

    def bin2num_hex(self, data_2_byte):
        """
        2字节数据转换成无符号整型，其中低位在前,高位在后
        :param data_2_byte 使用整型存储的2字节数据:
        :return 结果数据:
        """
        return ((data_2_byte & 0x0000FF00) >> 8) + ((data_2_byte & 0x000000FF) * 0x100)

    def bin2num1byte_hex(self, data_2_byte):
        """
        将2字节数据中的高位字节转换成无符号整型数据
        :param data_2_byte 使用整型存储的2字节数据:
        :return 结果数据:
        """
        return (data_2_byte & 0x0000FF00) >> 8

    def int2bin_hex(self, data_value):
        """
        将整型转成2字节数据，其中低位在前,高位在后; 最高位:符号位 0 正,1 负
        :param data_value:
        :return: 2进制数据
        """
        data_ = 0
        if data_value < 0 :
            # 负数 data_value = -1 * 0xFF11，则data_ = 0xFF91
            data_ = (((data_value * (-1)) + 0x8000) >> 8) + (((data_value * (-1)) & 0x00FF) << 8)
        else:
            # 正数 data_value = 0xFF11，则data_ = 0xFF11
            data_ = (data_value  >> 8) + ((data_value & 0x00FF) << 8)

        return self.pack_data2bin('!H', data_)


    def num2bin_hex(self, data_value):
        """
        无符号整型转换成2字节数据，其中低位在前,高位在后
        :param data_value:
        :return:2进制数据
        """
        data_ = (data_value  >> 8) + ((data_value & 0x00FF) << 8)
        return self.pack_data2bin('!H', data_)

    def num1byte2bin_hex(self, data_value):
        """
        将无符号整型数据转换成2字节数据中的高位字节
        :param data_value:
        :return:
        """
        data_ = (data_value & 0x00FF) << 8
        return self.pack_data2bin('!H', data_)

    def catch_cmd_code(self, cmd_code_str):
        '根据传入的CMD_CODE描述串，获取系统自定义的常量'
        if cmd_code_str == 'CCR':
            return self.dcc_def.const.CREDIT_CONTROL_REQUEST
        elif cmd_code_str == 'CCA':
            return self.dcc_def.const.CREDIT_CONTROL_ANSWER
        elif cmd_code_str == 'RAR':
            return self.dcc_def.const.RE_AUTH_REQUEST
        elif cmd_code_str == 'RAA':
            return self.dcc_def.const.RE_AUTH_ANSWER
        elif cmd_code_str == 'ASR':
            return self.dcc_def.const.ABORT_SESSION_REQUEST
        elif cmd_code_str == 'ASA':
            return self.dcc_def.const.ABORT_SESSION_ANSWER
        elif cmd_code_str == 'DWR':
            return self.dcc_def.const.DEVICE_WATCHDOG_REQUEST
        elif cmd_code_str == 'DWA':
            return self.dcc_def.const.DEVICE_WATCHDOG_ANSWER
        elif cmd_code_str == 'DPR':
            return self.dcc_def.const.DISCONNECT_PEER_REQUEST
        elif cmd_code_str == 'DPA':
            return self.dcc_def.const.DISCONNECT_PEER_ANSWER
        elif cmd_code_str == 'CER':
            return self.dcc_def.const.CAPABILITIES_EXCHANGE_REQUEST
        elif cmd_code_str == 'CEA':
            return self.dcc_def.const.CAPABILITIES_EXCHANGE_ANSWER
        else:
            raise self.MSG_ERR.MsgErr_InvalidMsgType, \
                "The CMD_CODE Error:%s" % cmd_code_str

    def bin(self, num):
        '将数据转为二进制表示'
        b = lambda n : (n > 0) and (b(n/2) + str(n%2)) or ''

        out_str = "%8s" % b(num)
        out_str = out_str.replace(' ', '0')

        return out_str


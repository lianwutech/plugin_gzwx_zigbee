#!/usr/bin/env python
# -*- coding:utf-8 -*-

""":mod:`znetmessageerror` -- 消息错误类
"""

class MessageException(Exception):
    '''消息处理 异常基类
    '''
    def __init__(self, msg=None):
        Exception.__init__(self)
        self.msg = msg

    def __name__(self):
        return "MessageException"

    def __repr__(self):
        return repr(self.msg)

    def __str__(self):
        return str(self.msg)

class MsgErr_InvalidFrameHeader(MessageException):
    '''帧头错误'''
    def __init__(self, msg=None):
        MessageException.__init__(self, msg)
    def __name__(self):
        return "MsgErr_InvalidFrameHeader"

class MsgErr_InvalidFrameLength(MessageException):
    '''帧长度错误'''
    def __init__(self, desired_length, real_length, msg=None):
        MessageException.__init__(self, msg)
        self.desired_length = desired_length
        self.real_length = real_length
    def __name__(self):
        return "MsgErr_InvalidFrameLength"

class MsgErr_InvalidFrameTail(MessageException):
    '''帧尾错误'''
    def __init__(self, msg=None):
        MessageException.__init__(self, msg)
    def __name__(self):
        return "MsgErr_InvalidFrameTail"

class MsgErr_FrameNotIntegrity(MessageException):
    '''帧不完整，需继续接收数据'''
    def __init__(self, msg=None):
        MessageException.__init__(self, msg)
    def __name__(self):
        return "MsgErr_FrameNotIntegrity"

class MsgErr_InvalidMsgType(MessageException):
    '''消息数据类型错误'''
    def __init__(self, msg=None):
        MessageException.__init__(self, msg)
    def __name__(self):
        return "MsgErr_InvalidMsgType"

class MsgDataException(MessageException):
    '''
    数据内容错误基类,继承自MessageException
    '''
    def __init__(self, msg=None):
        MessageException.__init__(self, msg)
    def __name__(self):
        return "MsgDataException"

class MsgDataErr_InvalidDataType(MsgDataException):
    '''数据类型错误'''
    def __init__(self, msg=None):
        MsgDataException.__init__(self, msg)
    def __name__(self):
        return "MsgDataErr_InvalidDataType"

class MsgDataErr_InvalidDataRange(MsgDataException):
    '''数据范围错误'''
    def __init__(self, msg=None):
        MsgDataException.__init__(self, msg)
    def __name__(self):
        return "MsgDataErr_InvalidDataRange"

class MsgDataErr_DecodDataError(MsgDataException):
    '''解析数据错误'''
    def __init__(self, msg=None):
        MsgDataException.__init__(self, msg)
    def __name__(self):
        return "MsgDataErr_DecodDataError"

class MsgDataErr_InvalidInitParam(MsgDataException):
    '''错误的初始化参数'''
    def __init__(self, msg=None):
        MsgDataException.__init__(self, msg)
    def __name__(self):
        return "MsgDataErr_InvalidInitParam"

class MsgErr_InvalidTagDataLength(MsgDataException):
    '''错误的标签数据长度'''
    def __init__(self, msg=None):
        MsgDataException.__init__(self, msg)
    def __name__(self):
        return "MsgErr_InvalidTagDataLength"

class MsgErr_TagDataCheckFail(MsgDataException):
    '''标签数据校验失败'''
    def __init__(self, msg=None):
        MsgDataException.__init__(self, msg)
    def __name__(self):
        return "MsgErr_TagDataCheckFail"
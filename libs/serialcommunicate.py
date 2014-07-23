#!/usr/bin/env python
# -*- coding:utf-8 -*-

""":mod:`serialcommunicate` -- 串口通讯模块
"""

#-*- coding: utf-8 -*-
from time import sleep
from serial import Serial


class SerialCommunicate():
    def __init__(self):
        self.__terminate = False
        self.serial = Serial()

    def open(self, settings):
        try:
            self.serial = Serial(settings["port"], settings["baund"], settings["bytesize"],
                                 settings["parity"], settings["stopbits"], settings["timeout"])
            self.serial.flushInput()
            self.serial.flushOutput()
        except Exception, msg:
            return False, msg.message.decode("gbk")

        return True, "success"

    def reset(self):
        self.serial.setDTR(0)
        sleep(0.1)
        self.serial.setDTR(1)

    def terminate(self):
        self.__terminate = True

    def send(self, data):
        self.serial.write(data)

    def recv(self):
        data = ''
        be_quit = False
        while 1:
            if self.__terminate:
                break
            data = self.serial.read(1)
            if data == '':
                break;

            sleep(0.02)
            while 1:
                n = self.serial.inWaiting()
                if n > 0:
                    data += self.serial.read(n)
                    # print "%r" % data
                    sleep(0.02) # data is this interval will be merged
                else:
                    be_quit = True
                    break
            if be_quit:
                break

        # print "get msg: %s" % data.encode("hex")
        return data

    def close(self):
        if self.serial.isOpen():
            self.serial.close()

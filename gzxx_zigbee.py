#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
    感知无限公司
    1、device_id的组成方式为ip_port
    2、设备类型为0，未知
    3、通过全局变量来管理每个介入设备，信息包括device_id，thread对象，handler对象
    4、设备数据传输格式：
        对于内置传感器：字符串不变；整形转成字符串；二进制转成16进制字符串
        对于透传数据：data为数据的16进制字符串
    5、设备指令传输格式：
        对于继电器控制，device_cmd内容为json字符串，ctrl_cmd："0x1a"／"0x2a"／"0x3b",ctrl_param:整形字符串如"10"
        对于透传指令，device_cmd为透传的指令
    6、devices_info_dict需要持久化设备信息，启动时加载，变化时写入
"""
import sys
import os
import time
import paho.mqtt.client as mqtt
import threading
import logging
import ConfigParser
import serial
try:
    import paho.mqtt.publish as publish
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.publish"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.publish as publish
from json import loads, dumps

from libs.utils import *
from libs.znetmsgdefine import *
from libs.znetmessage import *
from libs.serialcommunicate import *

# 全局变量
# 设备信息字典
devices_info_dict = dict()
# 设备运行字典，device_id、运行对象
devices_dict = dict()
cooperator_serial = SerialCommunicate()

# 切换工作目录
# 程序运行路径
procedure_path = cur_file_dir()
# 工作目录修改为python脚本所在地址，后续成为守护进程后会被修改为'/'
os.chdir(procedure_path)

# 日志对象
logger = logging.getLogger('tcpserver')
hdlr = logging.FileHandler('./tcpserver.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.WARNING)

# 加载配置项
config = ConfigParser.ConfigParser()
config.read("./tcpserver.cfg")
serial_port = int(config.get('serial', 'port'))
serial_baund = int(config.get('serial', 'baund'))
mqtt_server_ip = config.get('mqtt', 'ip')
mqtt_server_port = int(config.get('mqtt', 'port'))
gateway_topic= config.get('gateway', 'topic')


# 加载设备信息字典
devices_info_file = "./devices.txt"
def load_devices_dict():
    devices_file = open(devices_info_file, "r+")
    if os.path.exists(devices_info_file):
        content = devices_file.read()
        devices_file.close()
        try:
            devices_info_dict = loads(content)
        except Exception, e:
            logger.error("devices.txt内容格式不正确")


# 新增设备
def check_device(device_id, device_type, device_addr, device_port):
    # 如果设备不存在则设备字典新增设备并写文件
    if device_id not in devices_info_dict:
        # 新增设备到字典中
        devices_info_dict[device_id] = {
            "device_id": device_id,
            "device_type": device_type,
            "device_addr": device_addr,
            "device_port": device_port
        }
        #写文件
        devices_file = open(devices_info_file, "r+")
        devices_file.write(dumps(devices_info_dict))
        devices_file.close()

def publish_device_data(device_id, device_type, device_addr, device_port, device_data):
    # device_data: 16进制字符串
    # 组包
    device_msg = {
        "device_id": device_id,
        "device_type": device_type,
        "device_addr": device_addr,
        "device_port": device_port,
        "device_data": device_data
    }

    # MQTT发布
    publish.single(topic=gateway_topic,
                   payload=device_msg,
                   hostname=mqtt_server_ip,
                   port=mqtt_server_port)
    logger.info("向Topic(%s)发布消息：%r" % (gateway_topic, device_msg))


def process_zigbee_msg(zigbee_msg):
    """
    对解码后的zigbee消息进行处理
    :param data_sender: 数据发送队列
    :param zigbee_msg: 解析后的zigbee消息
    :return:
    """
    # 计算时间戳
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    # 记录解析后的消息内容
    # logger.info("%s收到消息：%r" % (timestamp, zigbee_msg))
    logger.debug("%s收到消息：%s" % (timestamp, dumps(zigbee_msg.msg['tag_data'])))
    data_msg = dict()

    # 判断解析结果
    if zigbee_msg.msg['decode_frame_status'] == zigbee_msg.msg_engine.msg_def.const.DECODE_FRAME_END :
        # 消息正常解析，将每个传感器的数据分别发布并更新设备字典；
        # 判断通信协议
        if zigbee_msg.msg['frame_type'] == zigbee_msg.msg_engine.msg_def.const.FRAME_TYPE_READER:
            # 读卡器通讯协议
            if zigbee_msg.msg['tag_data_type'] == zigbee_msg.msg_engine.msg_def.const.TAG_DATA_TYPE_NORMAL:
                # 正常标签数据
                logger.debug("消息为正常标签数据消息")
                router_id = zigbee_msg.msg['tag_data']['router_addr']
                # 传感器数据处理
                for i in range(zigbee_msg.msg['tag_data']['tag_num']):
                    tag_item = zigbee_msg.msg['tag_data']['data_list'][i]
                    node_id = tag_item["tag_addr"]
                    logger.debug("处理标签数据，数据下标：%d" % i)
                    for j in range(0, len(tag_item['sensors_data_list'])):
                        logger.debug("处理传感器数据，数据下标：%d" % j)
                        sensor_data = tag_item['sensors_data_list'][j]
                        if sensor_data["sensor_type"] != const.DEVICE_TYPE_SENSOR_NONE:
                            device_id = "%s_%s_%d" % (router_id, node_id, j + 1)
                            device_addr = node_id
                            device_port = j + 1
                            device_type = sensor_data["sensor_type"]
                            device_data = sensor_data["sensor_data"]
                            check_device(device_id, device_type, device_addr, device_port)
                            publish_device_data(device_id, device_type, device_addr, device_port, device_data)
                logger.debug("zigbee_msg.msg['tag_data']['delay_status_list'] = %r" % zigbee_msg.msg['tag_data']['delay_status_list'])

                # 中继器设备状态数据
                for k in range(0, len(zigbee_msg.msg['tag_data']['delay_status_list'])):
                    logger.debug("处理状态数据，数据下标：%d" % k)
                    device_id = "%s_%d" % (router_id, k + 1)
                    device_addr = router_id
                    device_port = k + 1
                    device_type = const.DEVICE_TYPE_DELAY_CTRL
                    device_data = int2hex(int(zigbee_msg.msg['tag_data']['delay_status_list'][k]))
                    check_device(device_id, device_type, device_addr, device_port)
                    publish_device_data(device_id, device_type, device_addr, device_port, device_data)

            elif zigbee_msg.msg['tag_data_type'] == zigbee_msg.msg_engine.msg_def.const.MESSAGE_TYPE_READ_PARAM:
                # 读取读卡器参数响应消息
                # 中继器地址
                logger.debug("消息为读取读卡器参数响应消息")
                router_id = zigbee_msg.msg['tag_data']['tag_addr']
                for i in range(0, len(zigbee_msg.msg['tag_data']['delay_status_list'])):
                    logger.debug("处理状态数据，数据下标：%d" % i)
                    device_id = "%s_%d" % (router_id, i + 1)
                    device_addr = router_id
                    device_port = i + 1
                    device_type = const.DEVICE_TYPE_DELAY_CTRL
                    device_data = int2hex(int(zigbee_msg.msg['tag_data']['delay_status_list'][i]))
                    check_device(device_id, device_type, device_addr, device_port)
                    publish_device_data(device_id, device_type, device_addr, device_port, device_data)

            else:
                # 异常消息
                logger.error("错误消息类型：%d" % zigbee_msg.msg['tag_data_type'])
        else:
            # 异常
            logger.error("错误帧类型：%d" % zigbee_msg.msg['frame_type'])


def process_zigbee_serial_data(cur_package_buff):
    """
    串口数据处理
    :param data_sender:
    :param serial_data:
    :return:
    """
    zigbee_msg = GZXXZigbeeNetMessage()
    try:
        zigbee_msg.unpack(cur_package_buff)
        process_zigbee_msg(zigbee_msg)
    except Exception, e:
        logger.error(e)


# 串口数据读取线程
def process_mqtt(device_id):
    """
    :param device_id 设备地址
    :return:
    """
    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, rc):
        logger.info("Connected with result code " + str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(device_id)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        logger.info("收到数据消息" + msg.topic + " " + str(msg.payload))
        # 消息只包含device_cmd，为json字符串
        device_cmd = loads(msg.payload)
        zigbee_ctrl_msg = GZXXZigbeeNetMessage()

        device_info = devices_info_dict["device_id"]
        node_port = device_info["device_port"]
        # 指令消息处理对象
        if len(device_info["device_addr"]) == 0:
            zigbee_ctrl_msg.msg['tag_data']['tag_addr'] = "FFFFFF"
        else:
            # 根据协议，读卡器地址前两个字节为网络地址，第三个字节统一为0xef
            zigbee_ctrl_msg.msg['tag_data']['tag_addr'] = device_info["device_addr"]

        zigbee_ctrl_msg.msg['frame_type'] = zigbee_ctrl_msg.msg_engine.msg_def.const.FH_READER
        zigbee_ctrl_msg.msg['tag_data_type'] = zigbee_ctrl_msg.msg_engine.msg_def.const.MESSAGE_TYPE_RELAY_CTRL
        # 0x2切换到手动状态
        zigbee_ctrl_msg.msg['tag_data']['control_mode_switch'] = 2

        _delay_ctrl_reg = []
        for i in range(0, 8):
            ctrl_reg = dict()
            if i == node_port - 1:
                ctrl_reg["ctrl_cmd"] = int(device_cmd["ctrl_cmd"], 16)
                ctrl_reg["ctrl_delay_time"] = int(device_cmd["ctrl_delay_time"])
            else:
                ctrl_reg["ctrl_cmd"] = 0xff
                ctrl_reg["ctrl_delay_time"] = 0xffff
            interface_logger.debug("%d delay_ctrl_reg: %s" % (i, ctrl_reg))
            _delay_ctrl_reg.append(ctrl_reg)
        zigbee_ctrl_msg.msg['tag_data']['delay_ctrl_reg'] = _delay_ctrl_reg

        # 消息打包
        try:
            # interface_logger.debug("zigbee_msg: %s" % dumps(zigbee_ctrl_msg.msg['tag_data']))
            zigbee_ctrl_msg.pack()
            interface_logger.debug("打包后结果:%r" % zigbee_ctrl_msg.msg['frame_data_buff'])
            # 指令下发
            cooperator_serial.send(zigbee_ctrl_msg.msg['frame_data_buff'])
        except Exception, e:
            interface_logger.error("消息打包错误，错误内容：%s" % e)

    client = mqtt.Client(client_id=gateway_topic)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(mqtt_server_ip, mqtt_server_port, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

# mqtt监听线程函数
def process_manage_mqtt():
    while True:
        for device_info in  devices_info_dict:
            if device_info["device_type"] == const.DEVICE_TYPE_DELAY_CTRL or \
                            device_info["device_type"] == const.ZNET_DEVICE_TYPE_SENSOR_NONE:
                if device_info["device_id"] in devices_dict:
                    # 检查线程状态
                    if not devices_dict["device_id"]["thread"].is_alive():
                        devices_dict["device_id"]["thread"].start()
                else:
                    # 新建线程
                    # 创建线程接受消息
                    process_thread = threading.Thread(target=process_mqtt, args=(device_info["device_id"]))
                    process_thread.start()
                    devices_dict[device_info["device_id"]] = {"thread": process_thread}
        # 休息5s
        sleep(5)

if __name__ == "__main__":

    # 初始化mqtt管理线程
    manage_mqtt_thread = threading.Thread(target=process_manage_mqtt)
    manage_mqtt_thread.start()

    # 初始化串口
    serial_settings = {
        'port': serial_port,
        'baund': serial_baund,
        'bytesize': serial.EIGHTBITS,
        'parity': serial.PARITY_NONE,
        'stopbits': serial.STOPBITS_ONE,
        'timeout': 1}

    data_buff = ""
    while True:

        # 如果线程停止则创建
        if not manage_mqtt_thread.is_alive():
            manage_mqtt_thread = threading.Thread(target=process_manage_mqtt)
            manage_mqtt_thread.start()

        # 读取串口数据并解析
        serial_data = None

        # 串口数据读取
        logger.debug("串口数据读取")
        try:
            serial_data = cooperator_serial.recv()
        except Exception, e:
            serial_data = None
            logger.error(e)
            logger.info("重新打开串口")
            result, error_info = cooperator_serial.open(serial_settings)
            if result:
                logger.error("重新打开串口成功")
            else:
                logger.error("重新打开串口失败")

        # 解析串口数据
        if serial_data:
            logger.debug("串口数据: %r" % serial_data)
            logger.debug("16进制串口数据: %s" % serial_data.encode("hex"))
            logger.debug("串口数据长度: %d" % (len(serial_data)))

            # 内存拼接
            data_buff = data_buff + serial_data
            logger.debug("16进制待处理数据: %s" % data_buff.encode("hex"))
            logger.debug("待处理数据长度: %d" % (len(data_buff)))

            if len(data_buff) > 0:
                # 找到报文头
                frame_header_pos = get_frame_header_pos(data_buff)
                logger.debug("报文头内存下标: %d" % frame_header_pos)
                if frame_header_pos < 0:
                    # 没有找到报文头，则丢弃
                    data_buff = None
                    logger.debug("丢弃串口数据: %s" % serial_data.encode("hex"))
                else:
                    data_buff = data_buff[frame_header_pos:]
                    data_buff_len = len(data_buff)
                    while data_buff_len > 0:
                        # 获取当前包长度
                        logger.debug("待处理数据包长度:%d,数据内容：%s" % (data_buff_len, data_buff.encode("hex")))
                        cur_package_len = get_package_len(data_buff)
                        if cur_package_len == 0:
                            logger.debug("获取长度异常。")
                            break
                            # 缓存切割
                        cur_package_buff = data_buff[0:cur_package_len]
                        logger.debug("当前数据包长度:%d, 数据内容：%s" % (cur_package_len, cur_package_buff.encode("hex")))
                        data_buff = data_buff[cur_package_len:]
                        data_buff_len = len(data_buff)
                        logger.debug("剩余数据包长度:%d, 数据内容：%s" % (cur_package_len, cur_package_buff.encode("hex")))

                        # 消息解码
                        process_zigbee_serial_data(cur_package_buff)

        else:
            logger.debug("处理完成，休眠0.1秒")
            time.sleep(0.1)


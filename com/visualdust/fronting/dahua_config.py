from com.dahua.MVSDK import *


def set_brightness(camera, value):
    """
    设置亮度
    """
    Node = pointer(GENICAM_IntNode())
    NodeInfo = GENICAM_IntNodeInfo()
    NodeInfo.pCamera = pointer(camera)
    NodeInfo.attrName = b"Brightness"
    GENICAM_createIntNode(byref(NodeInfo), byref(Node))
    nRet = Node.contents.setValue(Node, c_longlong(value))
    if nRet != 0:
        print("设置亮度 %d 失败！" % value)
    else:
        print("设置亮度 %d 成功！" % value)

    # 释放节点资源
    Node.contents.release(Node)


def set_balance_white_auto(camera):
    """
    设置自动白平衡
    """
    Node = get_analog_control_node(camera)
    enum_node = Node.contents.balanceWhiteAuto(Node)
    nRet = enum_node.setValueBySymbol(enum_node, b"Continuous")
    if nRet != 0:
        print("设置自动白平衡失败！")
    else:
        print("设置自动白平衡成功！")

    # 释放节点资源
    enum_node.release(enum_node)
    Node.contents.release(Node)


def set_black_level_auto(camera):
    """
    设置自动灰阶
    """
    Node = get_analog_control_node(camera)
    enum_node = Node.contents.blackLevelAuto(Node)
    nRet = enum_node.setValueBySymbol(enum_node, b"Continuous")
    if nRet != 0:
        print("设置自动灰阶失败！")
    else:
        print("设置自动灰阶成功！")

    # 释放节点资源
    enum_node.release(enum_node)
    Node.contents.release(Node)


def set_gain_auto(camera):
    """
    设置自动增益
    """
    Node = get_analog_control_node(camera)
    enum_node = Node.contents.gainAuto(Node)
    nRet = enum_node.setValueBySymbol(enum_node, b"Continuous")
    if nRet != 0:
        print("设置自动增益失败！")
    else:
        print("设置自动增益失败！")

    # 释放节点资源
    enum_node.release(enum_node)
    Node.contents.release(Node)


def get_analog_control_node(camera):
    """
    获得相机analog属性节点
    """
    Node = pointer(GENICAM_AnalogControl())
    NodeInfo = GENICAM_AnalogControlInfo()
    NodeInfo.pCamera = pointer(camera)
    nRet = GENICAM_createAnalogControl(byref(NodeInfo), byref(Node))
    if nRet != 0:
        print("create Analog Node fail!")
        Node.contents.release(Node)
        return None
    return Node


def get_acquisition_control_node(camera):
    """
    获得相机acquisition属性节点
    """
    Node = pointer(GENICAM_AcquisitionControl())
    NodeInfo = GENICAM_AcquisitionControlInfo()
    NodeInfo.pCamera = pointer(camera)
    nRet = GENICAM_createAcquisitionControl(byref(NodeInfo), byref(Node))
    if nRet != 0:
        print("create Analog Node fail!")
        Node.contents.release(Node)
        return None
    return Node


def set_gain(camera, value):
    """
    设置gain
    """
    Node = get_analog_control_node(camera)
    double_node = Node.contents.gainRaw(Node)
    nRet = double_node.setValue(double_node, c_double(value))
    if nRet != 0:
        print("设置gain %f 失败！" % value)
    else:
        print("设置gain %f 成功！" % value)

    # 释放节点资源
    double_node.release(double_node)
    Node.contents.release(Node)


def set_gamma(camera, value):
    """
    设置gamma
    """
    # 通用属性设置:设置曝光 --根据属性类型，直接构造属性节点。如曝光是 double类型，构造doubleNode节点
    Node = pointer(GENICAM_DoubleNode())
    NodeInfo = GENICAM_DoubleNodeInfo()
    NodeInfo.pCamera = pointer(camera)
    NodeInfo.attrName = b"Gamma"
    GENICAM_createDoubleNode(byref(NodeInfo), byref(Node))
    nRet = Node.contents.setValue(Node, c_double(value))
    if nRet != 0:
        print("设置gamma %f 失败！" % value)
    else:
        print("设置gamma %f 成功！" % value)

    # 释放节点资源
    Node.contents.release(Node)


def set_exposure_time_mode_off(camera):
    """
    关闭相机自动曝光
    """
    node = get_acquisition_control_node(camera)
    enum_node = node.contents.exposureAuto(node)
    nRet = enum_node.setValueBySymbol(enum_node, b"Off")
    if nRet != 0:
        print("关闭自动曝光失败！")
    else:
        print("关闭自动曝光成功！")

    # 释放节点资源
    enum_node.release(enum_node)
    node.contents.release(node)


def set_exposure_time_mode_continuous(camera):
    """
    打开相机自动曝光
    """
    node = get_acquisition_control_node(camera)
    enum_node = node.contents.exposureAuto(node)
    nRet = enum_node.setValueBySymbol(enum_node, b"Continuous")
    if nRet != 0:
        print("设置自动曝光失败！")
    else:
        print("设置自动曝光成功！")

    # 释放节点资源
    enum_node.release(enum_node)
    node.contents.release(node)

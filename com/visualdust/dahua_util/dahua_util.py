#!/usr/bin/env python
# coding: utf-8
'''
Created on 2017-10-25

@author: 
'''

import cv2
import numpy

from com.dahua.ImageConvert import *
from .dahua_config import *

g_cameraStatusUserInfo = b"statusInfo"


# 相机连接状态回调函数
def deviceLinkNotify(connectArg, linkInfo):
    if (EVType.offLine == connectArg.contents.m_event):
        print("camera has off line, userInfo [%s]" % (c_char_p(linkInfo).value))
    elif (EVType.onLine == connectArg.contents.m_event):
        print("camera has on line, userInfo [%s]" % (c_char_p(linkInfo).value))


connectCallBackFuncEx = connectCallBackEx(deviceLinkNotify)


# 注册相机连接状态回调
def subscribeCameraStatus(camera):
    # 注册上下线通知
    # subscribe connection status notify
    eventSubscribe = pointer(GENICAM_EventSubscribe())
    eventSubscribeInfo = GENICAM_EventSubscribeInfo()
    eventSubscribeInfo.pCamera = pointer(camera)
    nRet = GENICAM_createEventSubscribe(byref(eventSubscribeInfo), byref(eventSubscribe))
    if (nRet != 0):
        print("create eventSubscribe fail!")
        return -1

    nRet = eventSubscribe.contents.subscribeConnectArgsEx(eventSubscribe, connectCallBackFuncEx, g_cameraStatusUserInfo)
    if (nRet != 0):
        print("subscribeConnectArgsEx fail!")
        # 释放相关资源
        eventSubscribe.contents.release(eventSubscribe)
        return -1

        # 不再使用时，需释放相关资源
    eventSubscribe.contents.release(eventSubscribe)
    return 0


# 反注册相机连接状态回调
def unsubscribeCameraStatus(camera):
    # 反注册上下线通知
    eventSubscribe = pointer(GENICAM_EventSubscribe())
    eventSubscribeInfo = GENICAM_EventSubscribeInfo()
    eventSubscribeInfo.pCamera = pointer(camera)
    nRet = GENICAM_createEventSubscribe(byref(eventSubscribeInfo), byref(eventSubscribe))
    if (nRet != 0):
        print("create eventSubscribe fail!")
        return -1

    nRet = eventSubscribe.contents.unsubscribeConnectArgsEx(eventSubscribe, connectCallBackFuncEx,
                                                            g_cameraStatusUserInfo)
    if (nRet != 0):
        print("unsubscribeConnectArgsEx fail!")
        # 释放相关资源
        eventSubscribe.contents.release(eventSubscribe)
        return -1

    # 不再使用时，需释放相关资源
    eventSubscribe.contents.release(eventSubscribe)
    return 0


# 设置软触发
def setSoftTriggerConf(camera):
    # 创建AcquisitionControl节点
    acqCtrlInfo = GENICAM_AcquisitionControlInfo()
    acqCtrlInfo.pCamera = pointer(camera)
    acqCtrl = pointer(GENICAM_AcquisitionControl())
    nRet = GENICAM_createAcquisitionControl(pointer(acqCtrlInfo), byref(acqCtrl))
    if (nRet != 0):
        print("create AcquisitionControl fail!")
        return -1

    # 设置触发源为软触发
    trigSourceEnumNode = acqCtrl.contents.triggerSource(acqCtrl)
    nRet = trigSourceEnumNode.setValueBySymbol(byref(trigSourceEnumNode), b"Software")
    if (nRet != 0):
        print("set TriggerSource value [Software] fail!")
        # 释放相关资源
        trigSourceEnumNode.release(byref(trigSourceEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1

    # 需要释放Node资源
    trigSourceEnumNode.release(byref(trigSourceEnumNode))

    # 设置触发方式
    trigSelectorEnumNode = acqCtrl.contents.triggerSelector(acqCtrl)
    nRet = trigSelectorEnumNode.setValueBySymbol(byref(trigSelectorEnumNode), b"FrameStart")
    if (nRet != 0):
        print("set TriggerSelector value [FrameStart] fail!")
        # 释放相关资源
        # release node resource before return
        trigSelectorEnumNode.release(byref(trigSelectorEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1

    # 需要释放Node资源
    trigSelectorEnumNode.release(byref(trigSelectorEnumNode))

    # 打开触发模式
    trigModeEnumNode = acqCtrl.contents.triggerMode(acqCtrl)
    nRet = trigModeEnumNode.setValueBySymbol(byref(trigModeEnumNode), b"On")
    if (nRet != 0):
        print("set TriggerMode value [On] fail!")
        # 释放相关资源
        trigModeEnumNode.release(byref(trigModeEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1

    # 需要释放相关资源
    trigModeEnumNode.release(byref(trigModeEnumNode))
    acqCtrl.contents.release(acqCtrl)

    return 0


# 设置外触发
def setLineTriggerConf(camera):
    # 创建AcquisitionControl节点
    acqCtrlInfo = GENICAM_AcquisitionControlInfo()
    acqCtrlInfo.pCamera = pointer(camera)
    acqCtrl = pointer(GENICAM_AcquisitionControl())
    nRet = GENICAM_createAcquisitionControl(pointer(acqCtrlInfo), byref(acqCtrl))
    if (nRet != 0):
        print("create AcquisitionControl fail!")
        return -1

    # 设置触发源为外触发Line1
    trigSourceEnumNode = acqCtrl.contents.triggerSource(acqCtrl)
    nRet = trigSourceEnumNode.setValueBySymbol(byref(trigSourceEnumNode), b"Line1")
    if (nRet != 0):
        print("set TriggerSource value [Line1] fail!")
        # 释放相关资源
        trigSourceEnumNode.release(byref(trigSourceEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1

    # 需要释放Node资源
    trigSourceEnumNode.release(byref(trigSourceEnumNode))

    # 设置触发方式
    trigSelectorEnumNode = acqCtrl.contents.triggerSelector(acqCtrl)
    nRet = trigSelectorEnumNode.setValueBySymbol(byref(trigSelectorEnumNode), b"FrameStart")
    if (nRet != 0):
        print("set TriggerSelector value [FrameStart] fail!")
        # 释放相关资源
        trigSelectorEnumNode.release(byref(trigSelectorEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1

    # 需要释放Node资源
    trigSelectorEnumNode.release(byref(trigSelectorEnumNode))

    # 打开触发模式
    trigModeEnumNode = acqCtrl.contents.triggerMode(acqCtrl)
    nRet = trigModeEnumNode.setValueBySymbol(byref(trigModeEnumNode), b"On")
    if (nRet != 0):
        print("set TriggerMode value [On] fail!")
        # 释放相关资源
        trigModeEnumNode.release(byref(trigModeEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1

    # 需要释放Node资源
    trigModeEnumNode.release(byref(trigModeEnumNode))

    # 设置触发沿
    trigActivationEnumNode = acqCtrl.contents.triggerActivation(acqCtrl)
    nRet = trigActivationEnumNode.setValueBySymbol(byref(trigActivationEnumNode), b"RisingEdge")
    if (nRet != 0):
        print("set TriggerActivation value [RisingEdge] fail!")
        # 释放相关资源
        trigActivationEnumNode.release(byref(trigActivationEnumNode))
        acqCtrl.contents.release(acqCtrl)
        return -1

    # 需要释放Node资源
    trigActivationEnumNode.release(byref(trigActivationEnumNode))
    acqCtrl.contents.release(acqCtrl)
    return 0


# 打开相机
def openCamera(camera):
    # 连接相机
    nRet = camera.connect(camera, c_int(GENICAM_ECameraAccessPermission.accessPermissionControl))
    if (nRet != 0):
        print("camera connect fail!")
        return -1
    else:
        print("camera connect success.")

    # 注册相机连接状态回调
    nRet = subscribeCameraStatus(camera)
    if (nRet != 0):
        print("subscribeCameraStatus fail!")
        return -1

    return 0


# 关闭相机
def closeCamera(camera):
    # 反注册相机连接状态回调
    nRet = unsubscribeCameraStatus(camera)
    if (nRet != 0):
        print("unsubscribeCameraStatus fail!")
        return -1

    # 断开相机
    nRet = camera.disConnect(byref(camera))
    if (nRet != 0):
        print("disConnect camera fail!")
        return -1

    return 0


# 设置曝光
def setExposureTime(camera, dVal, mode=False):
    """
    设置曝光时间，如果mode为True则在原来的曝光时间基础上改变
    """
    # 通用属性设置:设置曝光 --根据属性类型，直接构造属性节点。如曝光是 double类型，构造doubleNode节点
    exposureTimeNode = pointer(GENICAM_DoubleNode())
    exposureTimeNodeInfo = GENICAM_DoubleNodeInfo()
    exposureTimeNodeInfo.pCamera = pointer(camera)
    exposureTimeNodeInfo.attrName = b"ExposureTime"
    nRet = GENICAM_createDoubleNode(byref(exposureTimeNodeInfo), byref(exposureTimeNode))

    exposure_time = c_double()

    if mode:
        exposureTimeNode.contents.getValue(exposureTimeNode, exposure_time)
        exposure_time = c_double(exposure_time.value + dVal)
    else:
        exposure_time.value = dVal

    # 判断设置值是否超过上下限
    if exposure_time.value < 1:
        exposure_time.value = 1
    if exposure_time.value > 10000:
        exposure_time.value = 10000

    nRet = exposureTimeNode.contents.setValue(exposureTimeNode, exposure_time)
    if nRet != 0:
        print("设置曝光时间 %f 失败！" % exposure_time.value)
    else:
        print("设置曝光时间 %f 成功！" % exposure_time.value)

    # 释放节点资源
    exposureTimeNode.contents.release(exposureTimeNode)
    return 0


# 枚举相机
def enumCameras():
    # 获取系统单例
    system = pointer(GENICAM_System())
    nRet = GENICAM_getSystemInstance(byref(system))
    if (nRet != 0):
        print("getSystemInstance fail!")
        return None, None

    # 发现相机
    cameraList = pointer(GENICAM_Camera())
    cameraCnt = c_uint()
    nRet = system.contents.discovery(system, byref(cameraList), byref(cameraCnt), c_int(GENICAM_EProtocolType.typeAll));
    if (nRet != 0):
        print("discovery fail!")
        return None, None
    elif cameraCnt.value < 1:
        print("discovery no camera!")
        return None, None
    else:
        print("cameraCnt: " + str(cameraCnt.value))
        return cameraCnt.value, cameraList


def grabOne(camera):
    # 创建流对象
    streamSourceInfo = GENICAM_StreamSourceInfo()
    streamSourceInfo.channelId = 0
    streamSourceInfo.pCamera = pointer(camera)

    streamSource = pointer(GENICAM_StreamSource())
    nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))
    if (nRet != 0):
        print("create StreamSource fail!")
        return -1

    # 创建AcquisitionControl节点
    acqCtrlInfo = GENICAM_AcquisitionControlInfo()
    acqCtrlInfo.pCamera = pointer(camera)
    acqCtrl = pointer(GENICAM_AcquisitionControl())
    nRet = GENICAM_createAcquisitionControl(pointer(acqCtrlInfo), byref(acqCtrl))
    if (nRet != 0):
        print("create AcquisitionControl fail!")
        # 释放相关资源
        streamSource.contents.release(streamSource)
        return -1

    # 执行一次软触发
    trigSoftwareCmdNode = acqCtrl.contents.triggerSoftware(acqCtrl)
    nRet = trigSoftwareCmdNode.execute(byref(trigSoftwareCmdNode))
    if (nRet != 0):
        print("Execute triggerSoftware fail!")
        # 释放相关资源
        trigSoftwareCmdNode.release(byref(trigSoftwareCmdNode))
        acqCtrl.contents.release(acqCtrl)
        streamSource.contents.release(streamSource)
        return -1

        # 释放相关资源

    trigSoftwareCmdNode.release(byref(trigSoftwareCmdNode))
    acqCtrl.contents.release(acqCtrl)
    streamSource.contents.release(streamSource)

    return 0


# 设置感兴趣区域  --- 感兴趣区域的宽高 和 xy方向的偏移量  入参值应符合对应相机的递增规则
def setROI(camera, OffsetX, OffsetY, nWidth, nHeight):
    # 获取原始的宽度
    # get the max width of image
    widthMaxNode = pointer(GENICAM_IntNode())
    widthMaxNodeInfo = GENICAM_IntNodeInfo()
    widthMaxNodeInfo.pCamera = pointer(camera)
    widthMaxNodeInfo.attrName = b"WidthMax"
    nRet = GENICAM_createIntNode(byref(widthMaxNodeInfo), byref(widthMaxNode))
    if (nRet != 0):
        print("create WidthMax Node fail!")
        return -1

    oriWidth = c_longlong()
    nRet = widthMaxNode.contents.getValue(widthMaxNode, byref(oriWidth))
    if (nRet != 0):
        print("widthMaxNode getValue fail!")
        # 释放相关资源
        widthMaxNode.contents.release(widthMaxNode)
        return -1

        # 释放相关资源

    widthMaxNode.contents.release(widthMaxNode)

    # 获取原始的高度
    heightMaxNode = pointer(GENICAM_IntNode())
    heightMaxNodeInfo = GENICAM_IntNodeInfo()
    heightMaxNodeInfo.pCamera = pointer(camera)
    heightMaxNodeInfo.attrName = b"HeightMax"
    nRet = GENICAM_createIntNode(byref(heightMaxNodeInfo), byref(heightMaxNode))
    if (nRet != 0):
        print("create HeightMax Node fail!")
        return -1

    oriHeight = c_longlong()
    nRet = heightMaxNode.contents.getValue(heightMaxNode, byref(oriHeight))
    if (nRet != 0):
        print("heightMaxNode getValue fail!")
        # 释放相关资源
        heightMaxNode.contents.release(heightMaxNode)
        return -1

    # 释放相关资源
    heightMaxNode.contents.release(heightMaxNode)

    # 检验参数
    if ((oriWidth.value < (OffsetX + nWidth)) or (oriHeight.value < (OffsetY + nHeight))):
        print("please check input param!")
        return -1

    # 设置宽度
    widthNode = pointer(GENICAM_IntNode())
    widthNodeInfo = GENICAM_IntNodeInfo()
    widthNodeInfo.pCamera = pointer(camera)
    widthNodeInfo.attrName = b"Width"
    nRet = GENICAM_createIntNode(byref(widthNodeInfo), byref(widthNode))
    if (nRet != 0):
        print("create Width Node fail!")
        return -1

    nRet = widthNode.contents.setValue(widthNode, c_longlong(nWidth))
    if (nRet != 0):
        print("widthNode setValue [%d] fail!" % (nWidth))
        # 释放相关资源
        # release node resource before return
        widthNode.contents.release(widthNode)
        return -1

        # 释放相关资源

    widthNode.contents.release(widthNode)

    # 设置高度
    heightNode = pointer(GENICAM_IntNode())
    heightNodeInfo = GENICAM_IntNodeInfo()
    heightNodeInfo.pCamera = pointer(camera)
    heightNodeInfo.attrName = b"Height"
    nRet = GENICAM_createIntNode(byref(heightNodeInfo), byref(heightNode))
    if (nRet != 0):
        print("create Height Node fail!")
        return -1

    nRet = heightNode.contents.setValue(heightNode, c_longlong(nHeight))
    if (nRet != 0):
        print("heightNode setValue [%d] fail!" % (nHeight))
        # 释放相关资源
        heightNode.contents.release(heightNode)
        return -1

        # 释放相关资源

    heightNode.contents.release(heightNode)

    # 设置OffsetX
    OffsetXNode = pointer(GENICAM_IntNode())
    OffsetXNodeInfo = GENICAM_IntNodeInfo()
    OffsetXNodeInfo.pCamera = pointer(camera)
    OffsetXNodeInfo.attrName = b"OffsetX"
    nRet = GENICAM_createIntNode(byref(OffsetXNodeInfo), byref(OffsetXNode))
    if (nRet != 0):
        print("create OffsetX Node fail!")
        return -1

    nRet = OffsetXNode.contents.setValue(OffsetXNode, c_longlong(OffsetX))
    if (nRet != 0):
        print("OffsetX setValue [%d] fail!" % (OffsetX))
        # 释放相关资源
        OffsetXNode.contents.release(OffsetXNode)
        return -1

        # 释放相关资源

    OffsetXNode.contents.release(OffsetXNode)

    # 设置OffsetY
    OffsetYNode = pointer(GENICAM_IntNode())
    OffsetYNodeInfo = GENICAM_IntNodeInfo()
    OffsetYNodeInfo.pCamera = pointer(camera)
    OffsetYNodeInfo.attrName = b"OffsetY"
    nRet = GENICAM_createIntNode(byref(OffsetYNodeInfo), byref(OffsetYNode))
    if (nRet != 0):
        print("create OffsetY Node fail!")
        return -1

    nRet = OffsetYNode.contents.setValue(OffsetYNode, c_longlong(OffsetY))
    if (nRet != 0):
        print("OffsetY setValue [%d] fail!" % (OffsetY))
        # 释放相关资源
        OffsetYNode.contents.release(OffsetYNode)
        return -1

        # 释放相关资源

    OffsetYNode.contents.release(OffsetYNode)
    return 0


def init_camera(cam_gain=3, cam_gamma=1, cam_brightness=70, auto_set_exposure=False):
    """
    初始化相机
    """
    # 发现相机
    cameraCnt, cameraList = enumCameras()
    if cameraCnt is None:
        return None, None
    # 显示相机信息
    for index in range(0, cameraCnt):
        camera = cameraList[index]
        print("\nCamera Id = " + str(index))
        print("Key           = " + str(camera.getKey(camera)))
        print("vendor name   = " + str(camera.getVendorName(camera)))
        print("Model  name   = " + str(camera.getModelName(camera)))
        print("Serial number = " + str(camera.getSerialNumber(camera)))

    camera = cameraList[0]

    # 打开相机
    nRet = openCamera(camera)
    if nRet != 0:
        return None, None

    # 创建流对象
    streamSourceInfo = GENICAM_StreamSourceInfo()
    streamSourceInfo.channelId = 0
    streamSourceInfo.pCamera = pointer(camera)

    streamSource = pointer(GENICAM_StreamSource())
    nRet = GENICAM_createStreamSource(pointer(streamSourceInfo), byref(streamSource))
    if nRet != 0:
        return None, None

    # 通用属性设置:设置触发模式为off --根据属性类型，直接构造属性节点。如触发模式是 enumNode，构造enumNode节点
    # 自由拉流：TriggerMode 需为 off
    trigModeEnumNode = pointer(GENICAM_EnumNode())
    trigModeEnumNodeInfo = GENICAM_EnumNodeInfo()
    trigModeEnumNodeInfo.pCamera = pointer(camera)
    trigModeEnumNodeInfo.attrName = b"TriggerMode"

    nRet = GENICAM_createEnumNode(byref(trigModeEnumNodeInfo), byref(trigModeEnumNode))
    if nRet != 0:
        streamSource.contents.release(streamSource)
        return None, None

    nRet = trigModeEnumNode.contents.setValueBySymbol(trigModeEnumNode, b"Off")
    if nRet != 0:
        trigModeEnumNode.contents.release(trigModeEnumNode)
        streamSource.contents.release(streamSource)
        return None, None

    # 需要释放Node资源
    trigModeEnumNode.contents.release(trigModeEnumNode)
    set_gain(cam_gain)
    set_gamma(camera, cam_gamma)
    set_brightness(camera, cam_brightness)
    set_balance_white_auto(camera)
    set_black_level_auto(camera)
    if auto_set_exposure:
        set_exposure_time_mode_off(camera)
    else:
        set_exposure_time_mode_continuous(camera)
    # set_gain_auto(camera)
    # 开始拉流
    nRet = streamSource.contents.startGrabbing(streamSource, c_ulonglong(0),
                                               c_int(GENICAM_EGrabStrategy.grabStrartegySequential))
    if nRet != 0:
        streamSource.contents.release(streamSource)
        return None, None

    return streamSource, camera


def get_frame(stream_source):
    """
    获取一帧图像
    """
    # 主动取图
    frame = pointer(GENICAM_Frame())
    stream_source.contents.getFrame(stream_source, byref(frame), c_uint(1000))

    frame.contents.valid(frame)
    # 给转码所需的参数赋值
    imageParams = IMGCNV_SOpenParam()
    imageParams.dataSize = frame.contents.getImageSize(frame)
    imageParams.height = frame.contents.getImageHeight(frame)
    imageParams.width = frame.contents.getImageWidth(frame)
    imageParams.paddingX = frame.contents.getImagePaddingX(frame)
    imageParams.paddingY = frame.contents.getImagePaddingY(frame)
    imageParams.pixelForamt = frame.contents.getImagePixelFormat(frame)

    # 将裸数据图像拷出
    imageBuff = frame.contents.getImage(frame)
    userBuff = c_buffer(b'\0', imageParams.dataSize)
    memmove(userBuff, c_char_p(imageBuff), imageParams.dataSize)

    # 释放驱动图像缓存
    frame.contents.release(frame)

    # 如果图像格式是 Mono8 直接使用
    if imageParams.pixelForamt == EPixelType.gvspPixelMono8:
        grayByteArray = bytearray(userBuff)
        cvImage = numpy.array(grayByteArray).reshape(imageParams.height, imageParams.width)
    else:
        # 转码 => BGR24
        rgbSize = c_int()
        rgbBuff = c_buffer(b'\0', imageParams.height * imageParams.width * 3)

        IMGCNV_ConvertToBGR24(cast(userBuff, c_void_p), byref(imageParams), cast(rgbBuff, c_void_p),
                              byref(rgbSize))

        colorByteArray = bytearray(rgbBuff)
        cvImage = numpy.array(colorByteArray).reshape(imageParams.height, imageParams.width, 3)

    return cvImage


def close_camera(stream_source, camera):
    """
    关闭相机资源
    """
    # 停止拉流
    stream_source.contents.stopGrabbing(stream_source)
    # 关闭相机
    closeCamera(camera)
    # 释放相关资源
    stream_source.contents.release(stream_source)
    print("Close camera success!")


def auto_set_exposure_time(camera, image, gray_average=18, offset=1):
    src = numpy.copy(image)
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)

    # 计算图像平均灰度
    gray_aver = numpy.mean(src[:, :])

    if gray_aver > gray_average * 2.5:
        setExposureTime(camera, -200, mode=True)
    elif gray_aver > (gray_average + offset):
        setExposureTime(camera, -50, mode=True)
    elif gray_aver < (gray_average - offset):
        setExposureTime(camera, 50, mode=True)

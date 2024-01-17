from ctypes import *
from time import sleep
from TmsPyApi import *

LINMasterIndex = 0
LINSlaveIndex = 1
DevHandles = (c_uint * 20)()
LINOutMsg = LIN_EX_MSG()
LINMsg = LIN_EX_MSG()


# ERROR_TYPE = [
#     "函数执行成功",
#     "适配器不支持该函数",
#     "USB写数据失败",
#     "USB读数据失败",
#     "命令执行失败",
#     "该通道未初始化",
#     "LIN读数据失败"
# ]


def tmsInit() -> bool:
    return False if (USB_ScanDevice(byref(DevHandles)) and USB_OpenDevice(DevHandles[0])) == 0 else True


def tmsLinMasterInit():
    return False if LIN_EX_Init(DevHandles[0], LINMasterIndex, 19200, LIN_EX_MASTER) else True


def tmsBreak():
    LINMsg.MsgType = LIN_EX_MSG_TYPE_BK  
    LINMsg.Timestamp = 10  
    ret = LIN_EX_MasterSync(
        DevHandles[0], LINMasterIndex, byref(LINMsg), byref(LINOutMsg), 1)
    sleep(0.01)
    return False if ret != 1 else True


def tmsMasterSend(frameId: int, data: list):
    data_buffer = (c_byte * len(data))(*data)
    LINMsg.MsgType = LIN_EX_MSG_TYPE_MW  
    LINMsg.Timestamp = 0  
    LINMsg.PID = frameId  
    LINMsg.CheckType = LIN_EX_CHECK_EXT if frameId != 0x3c else LIN_EX_CHECK_STD 
    LINMsg.DataLen = 8
    for i in range(0, LINMsg.DataLen):
        LINMsg.Data[i] = data_buffer[i]
    ret = LIN_EX_MasterSync(DevHandles[0], LINMasterIndex, byref(LINMsg), byref(LINOutMsg), 1)
    if ret != 1:
        print("LIN ID[0x%02X] 发送失败!" % LINMsg.PID)
        exit()
    else:
        print("M2S", "[0x%02X] " % LINOutMsg.PID, end='')
        for i in range(LINOutMsg.DataLen):
            print("0x%02X " % LINOutMsg.Data[i], end='')
        print("")
    sleep(0.01)


def tmsMasterRead(frameId: int):
    LINMsg.MsgType = LIN_EX_MSG_TYPE_MR  
    LINMsg.Timestamp = 0  
    LINMsg.PID = frameId  
    ret = LIN_EX_MasterSync(
        DevHandles[0], LINMasterIndex, byref(LINMsg), byref(LINOutMsg), 1)
    if ret != 1:
        print("读取失败!")
        exit()
    else:
        print("S2M", "[0x%02X] " % LINOutMsg.PID, end='')
        for i in range(LINOutMsg.DataLen):
            print("0x%02X " % LINOutMsg.Data[i], end='')
        print("")


if __name__ == "__main__":
    print(tmsInit())
    print(tmsLinMasterInit())
    print(tmsBreak())

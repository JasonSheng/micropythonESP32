import time
from array import array

class MICROROBOT:
    i2c = []

    #motor set parama define
    BRAKE=20000
    FREE=0
    BIT_14=14    #speed rate 14 bits rate -16384~+16384
    BIT_13=13
    BIT_12=12
    BIT_11=11
    BIT_10=10
    BIT_9=9
    BIT_8=8     #default speed rate:-255~+255

    #motor IIC address define
    MOTORPRO_ADDR1=0x6F
    MOTORPRO_ADDR2=0x6D
    MOTORPRO_ADDR3=0x6E
    MOTORPRO_ADDR4=0x6C

    motorMode=0


    ##############################################################
    '''
      ratio=array('i', [60, 60, 60, 60])
      resolution=bytearray(4)
      resolution[0]=12
      resolution[1]=12
      resolution[2]=12
      resolution[3]=12
    '''
    ########################################################
    
    Multiple=bytearray(4)
    MotorAddress=bytearray(4)
    MotorAddress[0]=MOTORPRO_ADDR1
    MotorAddress[1]=MOTORPRO_ADDR2
    MotorAddress[2]=MOTORPRO_ADDR3
    MotorAddress[3]=MOTORPRO_ADDR4

    #motor mode define
    MODE_OPEN=0x00
    MODE_SPEED=0x01
    MODE_POSITION=0x02
    MODE_DIR_OPEN=0x10
    MODE_DIR_SPEED=0x11
    MODE_DIR_POSITION=0x12


    #motor iic protocal register address define
    ADDR8_VERSION=0
    ADDR16_REAL_SPEED=2
    ADDR16_REAL_POSITION=3
    ADDR16_SET_SPEED=4
    ADDR16_SET_POSITION=5
    ADDR8_MODE=12
    ADDR8_RESET=13
    ADDR8_FAULT=14
    ADDR8_RESERVED=15
    ADDR32_SPD_KP=4
    ADDR32_SPD_KI=5
    ADDR32_SPD_KD=6
    ADDR32_PST_KP=7
    ADDR32_PST_KI=8
    ADDR32_PST_KD=9
    
    modeSpeed = {
        0x40: 255,
        0x20: 511,
        0x10: 1023,
        0x08: 2047,
        0x04: 4095,
        0x02: 8191,
        0x01: 16383,
    }


    def __init__(self, _i2c):
        self.i2c = _i2c

    def robotScan(self):
        address=self.i2c.scan()
        for addr in address:
            print ("Hex = 0x%2x" % (addr))
        time.sleep(0.1)

    # def getVersion(self):
    #     uint8_t version = 0
    #     I2Cdev::readByte(I2C_ADDR_PMU, ADDR8_VERSION, &version)
    #     return version

    # def begin(self):
    #     return getVersion()

    def constrain(self, val, min_val, max_val):
        if val < min_val:
            return min_val
        if val > max_val:
            return max_val
        return val

    def write8(self, index, addr, data, len):
        motorAddr=self.MotorAddress[index - 1]

        b = bytearray(1)
        b[0] = data

        self.i2c.writeto_mem(motorAddr, addr, b)
#         self.i2c.writeto(motorAddr, add)
#         time.sleep(0.1)


    def write16(self, index, addr, data, len):
        motorAddr=self.MotorAddress[index - 1]

        b = bytearray(2)
        b[0] = data >> 8
        b[1] = data & 0xFF

        self.i2c.writeto_mem(motorAddr, addr*2, b)
#         self.i2c.writeto(motorAddr, add)
#         time.sleep(0.1)


    def setMode(self, index, _mode):
        if ((index < 1) or (index > 4)):
            return
        self.motorMode = _mode
        self.write8(index, self.ADDR8_MODE, _mode, 1)

    def reset(self, index, _reset=1):
        if (index < 1) or (index > 4):
            return
        self.write8(index, self.ADDR8_RESET, _reset, 1)

    def motorInit(self, index, _bit=BIT_8):
        boolFlag=True
        _bit = self.constrain(_bit, 8, 14)
        self.Multiple[index - 1] = 0x4000 >> _bit
        # # Wire.beginTransmission(MotorAddress[index - 1])
        # # boolFlag = Wire.endTransmission()
        self.reset(index,2)
        return boolFlag


    def setSpeed(self, index, speed):
        if ((index < 1) or (index > 4)):
            return
        speedBuf=0
        if (speed == self.BRAKE):
            speedBuf = speed
        else:
            if ((self.motorMode == self.MODE_OPEN) or (self.motorMode == self.MODE_DIR_OPEN)):
                option=self.Multiple[index - 1]

                switchSpeed=self.modeSpeed.get(option,255)
                speed=self.constrain(speed,-switchSpeed,switchSpeed)
                speedBuf = speed * self.Multiple[index-1]

            elif ((self.motorMode == self.MODE_SPEED) or (self.motorMode == self.MODE_DIR_SPEED)):
                _speedBuf = (speed / 100.0)
                speedBuf = self.ratio[index - 1] * self.resolution[index - 1] * _speedBuf
        self.write16(index, self.ADDR16_SET_SPEED, int(speedBuf), 1)




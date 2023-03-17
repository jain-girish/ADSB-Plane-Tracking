import pyModeS as pms
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import random


# def alterFunction(msg):

#8776.273348399, 8777.139490452

def rand_key(p):
    st = ""
    for i in range(p):
        temp = str(random.randint(0, 1))
        st += temp 
    return(st)

def rebuild_parity(msg):
    # print(msg)
    new_message= msg[0:22]
    new_message= new_message+"000000"
    calculated_parity=  pms.crc(new_message)
    calculated_parity_hex= format(calculated_parity, 'X')
    n=6-len(calculated_parity_hex)
    temp= "0"*n
    msg= msg[0:22]
    msg= msg+temp+calculated_parity_hex
    return msg

def alterSpeed_and_trackAngle(msg):
    binaryMessage= pms.hex2bin(msg) 
    # print((binaryMessage))
    alt_bits= binaryMessage[45:67]
    random_bits= rand_key(22)
    ret_str= binaryMessage[0:45]+random_bits+binaryMessage[67:112]
    hex_str= pms.bin2hex(ret_str)
    # print(hex_str)
    hex_str= rebuild_parity(hex_str)
    # print(hex_str)
    return (hex_str)

def alterAltitude(msg):
    binaryMessage= pms.hex2bin(msg) 
    # print((binaryMessage))
    alt_bits= binaryMessage[40:52]
    random_bits= rand_key(12)
    str = random_bits[:7] + '0' + random_bits[8:12]
    # print(len(str))
    ret_str= binaryMessage[0:40]+str+binaryMessage[52:112]
    hex_str= pms.bin2hex(ret_str)
    # print(len(hex_str))
    hex_str= rebuild_parity(hex_str)
    # print(hex_str)
    return (hex_str)

def positionAlter(msg):
    binaryMessage= pms.hex2bin(msg) 
    # print((binaryMessage))
    alt_bits= binaryMessage[54:88]
    random_bits= rand_key(34)
    # print(len(str))
    ret_str= binaryMessage[0:54]+random_bits+binaryMessage[88:112]
    hex_str= pms.bin2hex(ret_str)
    # print(len(hex_str))
    hex_str= rebuild_parity(hex_str)
    # print(hex_str)
    return (hex_str)



# print(alterAltitude("8D800D2DF82300030049B88D1C87"))
from re import T
import pyModeS as pms
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt
import main_check,alter
import random
import json

temp= True
true_positive=0
true_negative=0
false_negative=0
false_positive=0
mal_icao= []
validity = {}

def check_line(line):
    global true_positive, true_negative, false_negative, false_positive
    x = line.split()
    if len(x)<2 or len(x[1])!=30 or pms.df(x[1][1:29])!=17:
        h=1
    else:
        x[1]=(x[1][1:29])
        timing=float(x[0])
        message=x[1]
        tc= pms.adsb.typecode(message)
        msg_corrupt= False
        icao= pms.adsb.icao(message)
        if tc==11 and timing>8779.273348399 and timing<8783.139490452 :
            random_n= random.randint(0,9)
            if random_n>=6:
                msg_corrupt=True
                # altered_msg_count=altered_msg_count+1

                if temp==True:
                    print("error:expected, position alter", timing)
                    message=alter.positionAlter(message)
                    temp=False
                else:
                    print("error:expected, altitude alter", timing)
                    message=alter.alterAltitude(message)
                    temp=True
                
        if tc==19 and timing>8779.273348399 and timing<8783.139490452:
            random_n= random.randint(0,9)
            
            if random_n>=6:
                print("error:expected, speed and track angle alter", timing)
                msg_corrupt=True
                message= alter.alterSpeed_and_trackAngle(message)
        
    
        full_msg= x[0]+"    "+"*"+message+";"
        line= full_msg
        rr= main_check.main_check_function(line)
        #if (icao in validity and validity[icao][0]==False):
        #    pass
        #else:
        validity[icao] = rr
        if(rr[0]==False):
            if icao not in mal_icao:
                mal_icao.append(icao)
            if(msg_corrupt==False):
                false_negative=false_negative+1
            else:
                true_negative=true_negative+1
            #print("false")
            #print(timing)
        if(rr[0]==True):
            if(msg_corrupt==False):
                true_positive=true_positive+1
            else:
                false_positive=false_positive+1

# false_positive_rate=0
# true_negative_rate=0
# false_negative_rate=0
# true_positive_rate=0
# if(false_positive+true_negative!=0):
#     false_positive_rate= (false_positive/(false_positive+true_negative))*100
#     true_negative_rate= (true_negative/(true_negative+false_positive))*100
# if(false_negative+true_positive!=0):
#     false_negative_rate= (false_negative/(false_negative+true_positive))*100
#     true_positive_rate= (true_positive/(true_positive+false_negative))*100


def writedata():
    location = {}
    filter_validity = {}
    icaos = main_check.icaos[:]
    icaos_first_location = {}
    # icaos_previous_location = {}  use when implementing showing path covered by flight
    for i in icaos:
        if(i in main_check.pos_detail.keys() and len(main_check.pos_detail[i])>0):
            location[i] = main_check.pos_detail[i][-1]
            if (i not in icaos_first_location.keys()):
                icaos_first_location[i]=main_check.pos_detail[i][0]
                # icaos_previous_location[i] = main_check.pos_detail[i][0] if len(main_check.pos_detail[i])==1 else main_check.pos_detail[i][-2]
        if(i in validity):
            filter_validity[i] = validity[i]
    obj = {
        "icaos": icaos,
        "validity": filter_validity,
        "location": location,
        "icaos_first_location": icaos_first_location,
        # "icaos_previous_location": icaos_previous_location
    }
    with open("./data.json", 'w') as f:
        jsonobj = json.dumps(obj)
        f.write(jsonobj)

# print(main_check.pos_detail)
# print("Results:")
# print("False Positive : "+ str(false_positive))
# print("False Negative : "+ str(false_negative))
# print("True Positive : "+ str(true_positive))
# print("True Negative : "+ str(true_negative))
# print(".....................")
# print("False Positive Rate: "+ str(false_positive_rate)+"%")
# print("False Negative Rate: "+ str(false_negative_rate)+"%")
# print("True Positive Rate: "+ str(true_positive_rate)+"%")
# print("True Negative Rate: "+ str(true_negative_rate)+"%")


# print(icao)




    # x = line.split()
    # if len(x)<2:
    
    #     continue
    # if (len(x[1])!=30):
   
    #     continue
    # x[1]=(x[1][1:29])

    # if pms.df(x[1])!=17:
        
    #     continue
    # # print(x[1])
    # timing=float(x[0])
    # message=x[1]
    # icao= pms.adsb.icao(message)
    # tc= pms.adsb.typecode(message)
    # res= (True,None)
    # if tc==11:
    #     file2.write(line)

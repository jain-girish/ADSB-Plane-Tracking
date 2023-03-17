import pyModeS as pms
import matplotlib.pyplot as plt
from math import radians, cos, sin, asin, sqrt

def distance(lat1, lat2, lon1, lon2):
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers. Use 3956 for miles
    r = 6371
    # calculate the result
    # *1000 for metres
    return(c*r*1000)

icaos=[]
#altitudes
alt= dict()
alt_time=dict()
#speeds
speed= dict()
v_speed= dict()
h_speed= dict()
track_angle=dict()
speed_time=dict()
#position
pos= dict()
pos_time=dict()
pos_detail=dict()
pos_timing= dict()
countt=0
rest=0
def main_check_function(msg):
    x = msg.split()
    if len(x)<2:
        return True
    if (len(x[1])!=30):
        return True
    x[1]=(x[1][1:29])
    if pms.df(x[1])!=17:
        return True
    # print(x[1])
    timing=float(x[0])
    message=x[1]
    icao= pms.adsb.icao(message)
    if icao not in icaos:
        icaos.append(icao)
    tc= pms.adsb.typecode(message)
    res= (True,None)
    if tc==11:
        alt_sanity_bool=altitudeSanityCheck(message,icao,timing)
        alt_differential_bool= altitudeDifferentailCheck(message,icao,timing)
        pos_sanity_bool=positionSanityCheck(message,icao,timing)
        pos_differential_bool= positionDifferentialCheck(message,icao,timing)
        # positionDifferentialCheck(message,icao,timing)
        if alt_sanity_bool==False and pos_sanity_bool==False:
            res= (False,"Altitude and position sanity check both failed")
        elif alt_sanity_bool==False:
            res= (False,"Altitude Sanity Check Failed")
            # print("alt")
        elif pos_sanity_bool==False:
            res= (False,"Position Sanity Check Failed")
        elif alt_differential_bool==False:
            res= (False,"altitiude differential check failed")
        elif pos_differential_bool==False:
            res= (False,"position differential check failed")
        
        
            
        if alt_sanity_bool==False or pos_sanity_bool==False or alt_differential_bool==False or pos_differential_bool==False:
            # print(icao)
            if(icao in pos_detail and len(pos_detail[icao])>0):
                pos_detail[icao].pop()
                pos_timing[icao].pop()
                pos[icao].pop()
                pos_time[icao].pop()
        


    elif tc==19:
        # print(icao)
        speed_sanity_bool=speedAndTrackAngleSanityCheck(message,icao,timing)
        speed_differential_bool= speedAndTrackAngleDifferentialCheck(message,icao,timing)
        if  speed_sanity_bool==False:
            res=(False,"speed and track angle sanity check failed")
        elif speed_differential_bool==False:
            res=(False,"speed and track angle differential check failed")
        if speed_sanity_bool==False or speed_differential_bool==False:
            #print(icao)
            speed[icao].pop()
            h_speed[icao].pop()
            v_speed[icao].pop()
            track_angle[icao].pop()
            speed_time[icao].pop()
               
    return res


def positionSanityCheck(msg,icao,t):
    msg_even= None
    msg_odd= None
    res=True
    if icao in pos:
        last_msg= pos[icao][-1]
        if last_msg!=msg:
            last_bit= (pms.hex2bin(last_msg))[53]
            cur_bit= (pms.hex2bin(msg))[53]
            bb= False
            if last_bit=='0' and cur_bit=='1':
                bb=True
                msg_even= last_msg
                msg_odd=  msg

            elif last_bit=='1' and cur_bit=='0':
                bb=True
                msg_even= msg
                msg_odd= last_msg
            if bb==True:
                coord=None
                if msg_even==last_msg:
                    coord= pms.adsb.position(msg_even, msg_odd, 1, 0, lat_ref=None, lon_ref=None)
                else:
                    coord= pms.adsb.position(msg_even, msg_odd, 0, 1, lat_ref=None, lon_ref=None)
                if coord!=None:
                    latitude= coord[0]
                    longitude= coord[1]
                    if latitude<-90 or latitude>90 or longitude<-180 or longitude>180:
                        #print(coord)
                        res= False
                else:
                    res=False
                        
                if icao in pos_detail:
                    pos_detail[icao].append(coord)
                    pos_timing[icao].append(t)
                else:
                    pos_detail[icao]= [coord]
                    pos_timing[icao]=[t]
        pos[icao].append(msg)
        pos_time[icao].append(t)
    else:
        pos[icao]= [msg]
        pos_time[icao]=[t]
    return res


def positionDifferentialCheck(msg,icao,t):
    res=True
    msg_even= None
    msg_odd= None
    if icao in pos:
        if len(pos[icao])>=2:
            msg= pos[icao][-1]
            last_msg= pos[icao][-2]
            if last_msg!=msg:
                last_bit= (pms.hex2bin(last_msg))[53]
                cur_bit= (pms.hex2bin(msg))[53]
                bb= False
                if last_bit=='0' and cur_bit=='1':
                    bb=True
                    msg_even= last_msg
                    msg_odd=  msg
                elif last_bit=='1' and cur_bit=='0':
                    bb=True
                    msg_even= msg
                    msg_odd= last_msg
                if bb==True:
                    if (len(pos_detail[icao])>=2):

                        cur_corrd= pos_detail[icao][-1]
                        #print(len(pos_detail[icao]))
                        if (cur_corrd!=None):
                            latitude= cur_corrd[0]
                            longitude= cur_corrd[1]
                            last_coord_det= pos_detail[icao][-2]
                            last_latitude= last_coord_det[0]
                            last_longitude= last_coord_det[1]
                            last_coord_time= pos_timing[icao][-2]
                            dis= distance(last_latitude,latitude,last_longitude,longitude)
                            t= float(t)-float(last_coord_time)
                            temp= abs(dis)/abs(t)
                            # print(temp)
                            if temp>1200 or temp<50:
                                #print("long_dist", temp)
                                res= False
                               
                            # else: print(".")

                        else:
                            res=False
    return res



def altitudeSanityCheck(msg,icao,t):
    altitude= pms.adsb.altitude(msg)
    # print(altitude)
    res= True
    if altitude==None or altitude<-10 or altitude>65000:
        res= False
    if icao in alt:
        alt[icao].append(altitude)
        alt_time[icao].append(t)
    else:
        alt[icao]= [altitude]
        alt_time[icao]=[t]
    return res

def altitudeDifferentailCheck(msg,icao,t):
    res=True
    if icao in alt and len(alt[icao])>=2:
        altitude= alt[icao][-1]
        last_altitude= alt[icao][-2]
        last_time= alt_time[icao][-2]
        if altitude==None or last_altitude==None:
            res=False
        else:
            # can be wrong
            diff= abs((altitude-last_altitude)/(t-last_time))
            if(diff>125):
                res= False
    return res



def speedAndTrackAngleSanityCheck(msg,icao,t):
    tp=pms.adsb.velocity(msg)
    hSpeed= tp[0]
    vSpeed= tp[2]
    trackAngle= tp[1]
    # print("hspeed: "+ str(hSpeed)+ " vspeed: "+str(vSpeed)+" track angle: "+str(trackAngle))
    res= True
    if tp[0]==None or tp[1]==None or tp[2]==None:
        res= False
    if hSpeed==None or vSpeed==None or trackAngle==None or hSpeed>650 or hSpeed<0 or vSpeed>6000 or vSpeed<-6000 or trackAngle<0 or trackAngle>360:
        res= False
    if icao in speed:
        tp=pms.adsb.velocity(msg)
        speed[icao].append(tp)
        h_speed[icao].append(hSpeed)
        v_speed[icao].append(vSpeed)
        track_angle[icao].append(trackAngle)
        speed_time[icao].append(t)
    else:
        tp=pms.adsb.velocity(msg)
        speed[icao]= [tp]
        h_speed[icao]=[hSpeed]
        v_speed[icao]=[vSpeed]
        track_angle[icao]=[trackAngle]
        speed_time[icao]=[t]
    # print("length",len(speed[icao]))
    return res

def speedAndTrackAngleDifferentialCheck(msg,icao,t):
    tp=pms.adsb.velocity(msg)
    hSpeed= h_speed[icao][-1]
    vSpeed= v_speed[icao][-1]
    trackAngle= track_angle[icao][-1]
    res=True
    if hSpeed==None or vSpeed==None or trackAngle==None:
        res= False
    else:
        if icao in v_speed and len(v_speed[icao])>=2:
            last_speed= h_speed[icao][-2]
            last_v_speed= v_speed[icao][-2]
            last_angle= track_angle[icao][-2]
            last_time= speed_time[icao][-2]

            changes_speed=abs((hSpeed-last_speed)/(t-last_time))
            changes_v_speed=abs((vSpeed-last_v_speed)/(t-last_time))
            diff1= abs(trackAngle-last_angle)
            diff2= 360-abs(trackAngle-last_angle)
            cc=abs((min(diff1,diff2))/(t-last_time))
            changes_angle=[cc]
            if(changes_speed>13.5 or changes_v_speed>1900 or cc>10):
                res= False
    return res
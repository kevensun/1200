#coding:utf-8
import struct
import snap7
import sys
import snap7.client
from snap7.snap7types import *
from snap7.util import *

offsets = { "Bool":2,"Int": 2,"Real":4,"DInt":4,"String":256,
            "Byte":1,"DWord":4,"LReal":8,"LInt":8,"WString":512,
            "LWord":8,"SInt": 1,"UDInt":4,"UInt": 2,"ULInt": 8,
            "USInt":1,"Word":2,}

def init():
    client = snap7.client.Client()
    return client

def plc_connect(client,ip, rack=0, slot=1):   
    try:
        client.connect(ip, rack, slot)
    except BaseException as e:
        print str(e)
        return False
        #sys.exit(1)
    else:
        return True       

def plc_con_close(client):
    client.disconnect()

def readI(client,nameStr):
    if nameStr[0]=='I' or nameStr[0]=='i':
        if nameStr[1]>='0' and nameStr[1]<='3':
            addr=int(nameStr.split('.')[0][1:])
            bit=int(nameStr.split('.')[1])
            if bit>7:
                print "I bit out of range"
                return
            m_data = client.read_area(0x81, 0, addr, 1)
            return  (struct.unpack('!B', m_data)[0]>>bit)&1
        else:
            print "input out of range"
            return
    else:
        print "input error"
        return

def readQ(client,nameStr):
    if nameStr[0]=='Q' or nameStr[0]=='q':
        if nameStr[1]>='0' and nameStr[1]<='3':
            addr=int(nameStr.split('.')[0][1:])
            bit=int(nameStr.split('.')[1])
            if bit>7:
                print "Q bit out of range"
                return
            m_data = client.read_area(0x82, 0, addr, 1)
            return  (struct.unpack('!B', m_data)[0]>>bit)&1
        else:
            print "output out of range"
            return
    else:
        print "input error"
        return 

def readM(client,nameStr):
    if nameStr[0]=='M' or nameStr[0]=='m':
        if nameStr[1]>='0' and nameStr[1]<='9':
            addr=int(nameStr.split('.')[0][1:])
            bit=int(nameStr.split('.')[1])
            if bit>7:
                print "M bit out of range"
                return
            m_data = client.read_area(0x83, 0, addr, 1)
            return  (struct.unpack('!B', m_data)[0]>>bit)&1
        elif nameStr[1]=="B" or nameStr[1]=='b':
            addr=int(nameStr[2:])
            m_data=client.read_area(0x83, 0, addr, 1)
            return struct.unpack('!b', m_data)[0]
        elif nameStr[1]=="W" or nameStr[1]=='w':
            addr=int(nameStr[2:])
            m_data=client.read_area(0x83, 0, addr, 2)
            return struct.unpack('!h', m_data)[0]
        elif nameStr[1]=="D" or nameStr[1]=='d':
            addr=int(nameStr[2:])
            m_data=client.read_area(0x83, 0, addr, 4)
            return struct.unpack('!i', m_data)[0]           
    else:
        print "input error"
        return


def DBRead(client,str_db_num,str_type,str_offset):
    if str_db_num[:2] == 'DB' or str_db_num[:2] == 'db':
        db_num=int(str_db_num[2:])
        offset = int(str_offset.split('.')[0])
        data = client.db_read(db_num,offset,offsets[str_type])
        if str_type == 'Real':
            value = get_real(data,0)
            return value
        if str_type == 'Bool':
            bit = int(str_offset.split('.')[1])
            if bit >7:
                print "bit out of range"
                sys.exit(0)
            else:
                value = get_bool(data,0,bit)
                if value:
                    return 1
                else:
                    return 0
        if str_type == 'Int':
            value = get_int(data,0)
            return value
        # if str_type == 'String':
        #     value = get_string(data, 0,256)
        #     return value
        # if str_type == 'WString':
        #     value = get_string(data, 0,512)
        #     return value    
        if str_type == 'Byte' or str_type == 'SInt':
            value=struct.unpack('!b', data)[0]
            return value
        if str_type == 'DInt' or str_type == 'DWord':
            value=struct.unpack('!i', data)[0]
            return value  
        # if str_type == 'LInt' or str_type == 'LWord':
        #     value=struct.unpack('!q', data)[0]
        #     return value 
        if str_type == 'LReal':
            value=struct.unpack('!d', data)[0]
            return value  
        if str_type == 'UDInt':
            value=struct.unpack('!I', data)[0]
            return value
        if str_type == 'UInt':
            value=struct.unpack('!H', data)[0]
            return value
        # if str_type == 'ULInt':
        #     value=struct.unpack('!Q', data)[0]
        #     return value
        if str_type == 'USInt':
            value=struct.unpack('!B', data)[0]
            return value
        if str_type == 'Word':
            value=struct.unpack('!h', data)[0]
            return value
    else:
        print "input error"
        sys.exit(0)

if __name__ == "__main__":
    client_fd=init()   
    if plc_connect(client_fd,'192.168.1.248'):   
        result=readM(client_fd,"M10.2")
        print 'M10.2=',result

        result=readM(client_fd,"MB102")
        print 'MB102=',result

        result=readI(client_fd,"i0.1")
        print 'i0.1=',result

        result=readM(client_fd,"mw220")
        print 'MW220=',result

        result=readQ(client_fd,"q0.2")
        print 'q0.2=',result

        result=readM(client_fd,"md200")
        print 'MD200=',result


        

        result=DBRead(client_fd,"db1","Bool","0.0")
        print 'a=',result
        result=DBRead(client_fd,"db1","Byte","1.0")
        print 'b=',result
        result=DBRead(client_fd,"db1","DWord","2.0")
        print 'c=',result
        result=DBRead(client_fd,"db1","DInt","6.0")
        print 'd=',result
        result=DBRead(client_fd,"DB1","Int","10.0")
        print 'e=',result
        result=DBRead(client_fd,"db1","LReal","12.0")
        print 'f=',result 
        result=DBRead(client_fd,"db1","Real","20.0")
        print 'g=',result
        result=DBRead(client_fd,"db1","SInt","24.0")
        print 'h=',result
        result=DBRead(client_fd,"db1","UDInt","26.0")
        print 'i=',result
        result=DBRead(client_fd,"db1","UInt","30.0")
        print 'j=',result
        result=DBRead(client_fd,"db1","USInt","32.0")
        print 'k=',result
        result=DBRead(client_fd,"db1","Word","34.0")
        print 'l=',result


        # result=DBRead(client_fd,"db2","Bool","0.0")
        # print 'a=',result
        # result=DBRead(client_fd,"db2","Byte","1.0")
        # print 'b=',result
        # result=DBRead(client_fd,"db2","DWord","2.0")
        # print 'c=',result
        # result=DBRead(client_fd,"db2","DInt","6.0")
        # print 'd=',result
        # result=DBRead(client_fd,"DB2","Int","10.0")
        # print 'e=',result


        plc_con_close(client_fd)
    else:
        print 'link error'
       
   
def get_file_v1(fn, lines):
   ll=[]
   f = open(fn, 'r') 
   ll = f.readlines()
   f.close()
   for i in ll:
      lines.append(i)
   return lines
   
def parse_block_v1(lines):
   start_of_block = []
   maker = 'A'
   for i in range(len(lines)):
      a = lines[i]
      if a.count('CT') == 1:
         start_of_block.append(i)          
         maker = 'V'
         
      if a.count('CS') == 1:
         start_of_block.append(i)
         maker = 'C'   
         
   return start_of_block, maker
 
def parse_time_v1(lines, start_of_block, np, data_time):
   import time
   from datetime import datetime
   import calendar
   DT = []
   DoY = []
   ET = []
   for i in range(len(start_of_block)-1):
       a = lines[start_of_block[i]]
       b = a[0:a.index('C')-1]     
       t = []
       t.append(int(b[0:4]))
       t.append(int(b[5:7]))
       t.append(int(b[8:10]))
       t.append(int(b[11:13]))
       t.append(int(b[14:16]))
       t.append(float(b[17:len(b)]))
       
       c = time.strptime(b[0:len(b)],'%Y-%m-%dT%H:%M:%S.%f')
      
       DT.append(t)
       DoY.append(float(c.tm_yday)+(float(t[3])+float(t[4]/(60))+float(t[5]/(60*60)))/24)
       ET.append(calendar.timegm(c))
       
   data_time.DT = np.array(DT)
   data_time.DoY = np.array(DoY)
   data_time.ET = np.array(ET)
   
   return data_time

def parse_line1_v1(lines, start_of_block, np, maker, data_line1):
   aa = []
   bb = []
   cc = []
   for i in range(len(start_of_block)-1):
       a = lines[start_of_block[i]]
       b = a[a.index('C'):len(a)-1] 
       if maker == 'V':
           aa.append(b[2])   #unit_no
           bb.append(b[3:5]) #software level
           cc.append(b[5])   #message
           
       if maker == 'C':
           aa.append(b[2])   #unit_no
           bb.append(b[3:6]) #software level
           cc.append(b[6:9]) #message
           
   data_line1.version = np.array(bb) 
   data_line1.message = np.array(cc) 
   data_line1.unit_ID = np.array(aa)    
   
   return data_line1   
   
def parse_line2_v1(lines, start_of_block, np, maker, data_line2):
   aa = []
   bb = []
   cc = []
   dd = []
   ee = []
   xx = []
   zz = []
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i]+1]
      b = a[a.index(' ')+1:len(a)-1]
      if maker == 'V':
         zz.append(b[0])         #detection status
         aa.append(b[3:8])       #cloudbase height 1
         bb.append(b[9:14])      #cloudbase height 2
         cc.append(b[15:20])     #cloudbase height 3
         dd.append('/////')      #cloudbase height 4 set to // as vaisala only give 3
         ee.append(b[21:len(b)]) #flag
         xx.append('/////')      #see window contam for vaisala in line3
                   
      if maker == 'C':   
         zz.append(b[0])         #detection status
         aa.append(b[7:12])      #cloudbase height 1
         bb.append(b[13:18])     #cloudbase height 2
         cc.append(b[19:24])     #cloudbase height 3
         dd.append(b[25:30])     #cloudbase height 4
         ee.append(b[31:len(b)]) #flag
         xx.append(int(str(b[3:6])))       #window transmission
                 
   data_line2.DETS = np.array(zz)
   data_line2.CBH1 = np.array(aa)
   data_line2.CBH2 = np.array(bb)
   data_line2.CBH3 = np.array(cc)
   data_line2.CBH4 = np.array(dd)
   data_line2.flag = np.array(ee)
   data_line2.WT = np.array(xx)
   
   return data_line2   

def parse_line3_v1(lines, start_of_block, np, maker, data_line3):
   aa = []
   bb = []
   cc = []
   dd = []
   ee = []
   ff = []
   gg = []
   for i in range(len(start_of_block)-1):
      a = lines[start_of_block[i]+2]
      b = a[a.index(' ')+1:len(a)-1]
      if maker == 'V':     
         aa.append(int(str(b[6:9])))       #laser pulse energy
         bb.append(int(str(b[10:13])))     #laser temperature drop leading sign       
         cc.append(int(str(b[19:22])))     #window contamination
         dd.append(int(str(b[23:26])))     #tilt angle
         ee.append(int(str(b[27:31])))     #background light
         ff.append('/////')                #profile length N\A for Vaisala
         gg.append('/////')                #profile resolution N\A for Vaisala
      
      if maker == 'C':
         aa.append(int(str(b[14:17])))     #laser pulse energy (%)
         bb.append(int(str(b[18:21])))     #laser temperature drop leading sign
         cc.append('/////')                #window transmission defined for campbell so set to /////
         dd.append(int(str(b[22:24])))     #tilt angle
         ee.append(int(str(b[25:29])))     #background light
         ff.append(int(str(b[9:13])))      #profile length
         gg.append(int(str(b[6:8])))       #profile resolution
      
   data_line3.laser_energy         = np.array(aa)
   data_line3.laser_temperature    = np.array(bb)
   data_line3.window_contamination = np.array(cc)
   data_line3.tilt_angle           = np.array(dd)
   data_line3.background_light     = np.array(ee)  
   data_line3.resolution           = np.array(gg) 
   data_line3.length               = np.array(ff)    
      
   return data_line3
     
def parse_line4_v1(lines, start_of_block, np, maker, data_line4, R, L):
   alt = []
   line4 = []
   for i in range(len(start_of_block)-1):
      z = []
      bb = []
      if maker == 'V':
         for ii in range(16): #16 line of data
            a = lines[start_of_block[i]+3+ii]
            b = a[a.index(' ')+1:len(a)-1]
            z1 = int(b[0:3])*100#start of line height
            c = b[3:len(b)]
            for cc in range(16): #16 range gates per line
               z.append((z1+(cc*100))*0.3048) #profile height
               temp = int(c[cc*4:((cc*4)+4)],16)#(1000.sr.km)-1
               bb.append(float(temp/1e6)) #sr-1 m-1
               
         line4.append(bb)
         alt.append(z)
         
      if maker == 'C':
         a = lines[start_of_block[i]+3]
         b = a[a.index(' ')+1:len(a)-1]
         for cc in range(L[i]):
             z.append((cc*R[i]) + R[i])
             temp = int(b[cc*5:((cc*5)+5)],16)#(1000.sr.km)-1
             bb.append(float(temp/1e6))       #sr-1 m-1

         line4.append(bb) 
         alt.append(z)
   
   data_line4.ZZ = np.array(alt)
   data_line4.BB = np.array(line4)
   
   return data_line4
   
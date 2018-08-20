def QC_setup_v1(data, np, maker, data_time, data_line1,data_line2, data_line3, data_line4):
   data.DT = data_time.DT #calenar time int32 and float64
   data.ET = data_time.ET #epoch time float64
   data.DoY = data_time.DoY #day of year float 64
   data.version = data_line1.version # software version number string
   data.message = data_line1.message # message number string
   data.unit_ID = data_line1.unit_ID # unit ID string
   data.laser_energy = data_line3.laser_energy # % int32
   data.laser_temperature = data_line3.laser_temperature #deg C int32
   data.tilt_angle = data_line3.tilt_angle # degree int32
   data.background_light = data_line3.background_light # mV int32
   if maker == 'V':
      data.window_contamination = data_line3.window_contamination #mV int32
   if maker == 'C':
      temp = []
      for ii in range (0,len(data_line2.WT)-1):
        temp.append(int(2500*(1-(data_line2.WT[ii]*0.01))))
      data.window_contamination = np.array(temp)
   data.BB = data_line4.BB
   data.BB_flag = np.ones(data.BB.shape)
   data.ZZ = data_line4.ZZ
   dur, gates = data.BB_flag.shape
   s = (dur,4)
   data.CBH = (np.ones(s))*(-1e20)      
   data.CBH_flag = np.ones(data.CBH.shape)
   
   return data

def QC_BB_v1(data, np):
    ii_0 = np.where(data.BB == 0)
    data.BB_flag[ii_0] = 2
    ii_min = np.where(data.BB <= 1e-7)
    data.BB_flag[ii_min] = 2
    ii_max = np.where(data.BB >= 10)
    data.BB_flag[ii_max] = 2
    # more gates defined than actually used
    ii_0 = np.where(data.ZZ == -1e20)
    data.BB_flag[ii_max] = 3
   
    return data
   
def QC_BB_noise_v1(data):
    dur, gates = data.BB_flag.shape
    #for each gate
    for i in range(gates-1):
        for ii in range(2,dur-3):
            if ((data.BB_flag[ii-2,i]) and (data.BB_flag[ii,i] == 1) and (data.BB_flag[ii+2,i] != 1)):
                data.BB_flag[ii,i] = 2
        for ii in range(2,dur-2):
            if ((data.BB_flag[ii-1,i]) and (data.BB_flag[ii,i] == 1) and (data.BB_flag[ii+1,i] != 1)):
                data.BB_flag[ii,i] = 2
   
    #for each time
    for i in range(dur-1):
        for ii in range(2,gates-3):
            if ((data.BB_flag[i,ii-2]) and (data.BB_flag[i,ii] == 1) and (data.BB_flag[i,ii+2] != 1)):
                data.BB_flag[i,ii] = 2
        for ii in range(2,gates-2):
            if ((data.BB_flag[i,ii-1]) and (data.BB_flag[i,ii] == 1) and (data.BB_flag[i,ii+1] != 1)):
                data.BB_flag[i,ii] = 2
                
    return data
   
def QC_CBH_v1(data, data_line2, maker, np):
    # AMF flags: 
    #1 - good data, 2 - no sig backscatter, 3 - full obfurscation no cloud base
    #4 - some obfurscation - transparent, 5 - raw data missing  6 - time stamp
   
    # vaisala flags:
    #0 - no sig backscatter, 1 - one cb, 2 - two cbs, 3 - 3 cbs,
    #4 - full obfurscation no cloud base, 5 - some obfurscation - transparent
    #/ - Raw data input to algorithm missing or suspect
    
    # campbell flags:
    #0 - no sig backscatter, 1 - one cb, 2 - two cbs, 3 - 3 cbs, 4 - 4 cbs,
    #5 - full obfurscation no cloud base, 6 - some obfurscation - transparent
    #/ - Raw data input to algorithm missing or suspect
    
    #get rid of '/////'
    for n in range(len(data.ET)):
       if data_line2.CBH1[n].find('/') == -1: # no / found
          data.CBH[n,0] = int(data_line2.CBH1[n])             
       if data_line2.CBH2[n].find('/') == -1: # no / found
          data.CBH[n,1] = int(data_line2.CBH2[n])
       if data_line2.CBH3[n].find('/') == -1: # no / found
          data.CBH[n,2] = int(data_line2.CBH3[n])
       if data_line2.CBH4[n].find('/') == -1: # no / found
          data.CBH[n,3] = int(data_line2.CBH4[n])         
    
    ii_0 = np.where(data_line2.DETS == '0') # no significant backscatter
    data.CBH_flag[ii_0,:] = 2
    
    ii_0 = np.where(data_line2.DETS == '/') # raw data missing
    data.CBH_flag[ii_0,:] = 5
    
    if maker == 'V':
       ii_0 = np.where(data_line2.DETS == '4') # full obfurscation no cloud base
       data.CBH_flag[ii_0,:] = 3
       ii_0 = np.where(data_line2.DETS == '5') # some obfurscation - transparent
       data.CBH_flag[ii_0,:] = 4
       for n in range(len(data.ET)):
          for nn in range(3):
             data.CBH[n,nn] = (float(data.CBH[n,nn]))*0.3048 # convert to m
          
    if maker == 'C':
       ii_0 = np.where(data_line2.DETS == '5') # full obfurscation no cloud base
       data.CBH_flag[ii_0,:] = 3
       ii_0 = np.where(data_line2.DETS == '6') # some obfurscation - transparent
       data.CBH_flag[ii_0,:] = 4       
     
    return data
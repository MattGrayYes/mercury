import os
import glob
import time
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
 
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'
 
def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c #, temp_f
    
while True:
    temp = read_temp()
    print(temp)  

    if temp > 34: #vhot
        print("scorching")
        os.system('aplay ./audio/up\ 5.wav')    
    
    elif temp > 30: #vhot
        print("very hot")
        os.system('aplay ./audio/up\ 4.wav')
    
    elif temp > 26: #hot
        print("hot")
        os.system('aplay ./audio/up\ 1.wav')

    
    elif 21 < temp < 26: #ok
        print("ok")
        os.system('aplay ./audio/ok\ 1.wav')
    
    elif temp > 18:
        print("cool")
        os.system('aplay ./audio/down\ 1.wav')
        
    elif temp > 13:
        print("cold")
        os.system('aplay ./audio/down\ 2.wav')

    elif temp > 5:
        print("rather cold")
        os.system('aplay ./audio/down\ 3.wav')

    elif temp <= 5:
        print("freezing")
        os.system('aplay ./audio/down\ 3.wav')


    
    else:
        print("eh?")
    
    time.sleep(5)

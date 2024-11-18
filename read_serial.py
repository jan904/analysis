import serial
import matplotlib.pyplot as plt
import time
import datetime
import os

# Open the serial port
ser = serial.Serial(port = '/dev/serial/by-id/usb-Arrow_Arrow_USB_Blaster_TEI0001_ARA27238-if01-port0', baudrate = 115200, bytesize=8)

timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
output_dec = " "
parity = 0

# Create a directory to store the output files
directory = "./" + timestamp
os.mkdir(directory)

# Use time to read for certain amount of time
runtime_mins = 1000  # mins
start_time = time.time()
runtime_secs = runtime_mins * 60

while (time.time() - start_time) < runtime_secs:   
    # Read the serial port 
    c = ser.read()
    # If the read is not empty, decode it and write it to output.txt
    if len(c) != '':
        if parity == 0:
            try:
                utf = c.decode()
                bits = ' '.join([f'{i:08b}' for i in utf.encode('utf-8')])
                channel = bits[0:2]
                overflow = bits[-1]
            except:
                c = ('0' + str(c)[3:-1])
                bits = bin(int(c, 16))
                channel = bits[0:2]
                overflow = bits[-1]
                
            partiy = 1
                
        if parity == 1:
            try:
                utf = c.decode()
                bits = ' '.join([f'{i:08b}' for i in utf.encode('utf-8')])
                output_dec = (int(bits, 2))
            except:
                c = ('0' + str(c)[3:-1])
                output_dec = int(c, 16)
                
            parity = 0

        with open(f'{timestamp}/{channel}.txt', 'w') as f:
            f.write(str(output_dec) + ',\n')

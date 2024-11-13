import serial
import matplotlib.pyplot as plt
import time

# Open the serial port
ser = serial.Serial(port = 'COM4', baudrate = 115200, bytesize=8)

output_dec : str

# Use time to read for certain amount of time
runtime_mins : int  = 1000  # mins
start_time = time.time()
runtime_secs = runtime_mins * 60

while (time.time() - start_time) < runtime_secs:   
    # Read the serial port 
    c = ser.read()
    # If the read is not empty, decode it and write it to output.txt
    if len(c) != '':
        try:
            utf = c.decode()
            bits = ' '.join([f'{i:08b}' for i in utf.encode('utf-8')])
            output_dec = (int(bits, 2))
        except:
            c = ('0' + str(c)[3:-1])
            output_dec = int(c, 16)
            if output_dec == 128:
                output_dec = 0
        with open('Telepix.txt', 'a') as f:
            f.write(str(output_dec) + ',\n')


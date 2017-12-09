

import RPi.GPIO as GPIO
import time
import spidev
import csv
from datetime import datetime

spi = spidev.SpiDev()
spi.open(0, 0)

def ReadChannel(channel):
    adc = spi.xfer2([1, (8 + channel) << 4, 0])
    data = ((adc[1] & 3) << 8) + adc[2]
    return data

data_channel = 0
threshold = 100
def main():
    print("heart is beating")
    # input data as a csv file
    csvfile = csv.writer(open('./heart.csv', 'w'))
    csvfile.writerow(['Timestamp_RPI', 'heart_beat'])
    try:
        while True:
            csvfile.writerow([datetime.now().isoformat(), ReadChannel(data_channel)])
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exception: KeyboardInterrupt")

    finally:
        GPIO.cleanup()
        # clear

# call main
if __name__ == '__main__':
   main()
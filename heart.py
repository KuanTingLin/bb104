

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

def BPM(num_of_beats):
    rate = num_of_beats / 5
    bpm = rate * 60
    return bpm

data_channel = 0
threshold = 100
def main():
    print("heart is beating")
    csvfile = csv.writer(open('./heart.csv', 'w'))
    csvfile.writerow(['Timestamp_RPI', 'heart_beat'])
    try:
        while True:
            csvfile.writerow([datetime.now().isoformat(), ReadChannel(data_channel)])
            # beat = 0
            # start_time = time.time()
            # print(ReadChannel(data_channel))
            # prev_data = ReadChannel(data_channel)
            # while time.time() - start_time < 5:
            #     current_data = ReadChannel(data_channel)
            #
            #     if current_data - prev_data > threshold:
            #         beat = beat + 1
            #     prev_data = current_data
            #
            # bpm = BPM(beat)
            # print("Beats Per Minute:{}".format(bpm))
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("Exception: KeyboardInterrupt")

    finally:
        GPIO.cleanup()

# call main
if __name__ == '__main__':
   main()